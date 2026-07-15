

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import json
from sqlalchemy import select
from starlette import status


from library_app.books.book_service import get_top_5_books , check_single_book
from library_app.core.pagination import order_and_paginate_query
from library_app.db.session import db_dependency
from library_app.external.cache import cache_dependency , EMPTY_CACHE_VAL
from library_app.models import Book, Author
from library_app.schemas.books import BookResponse , BookWithAvailabilityResponse



router = APIRouter(prefix="/books", tags=["books"])


TOP5_BOOKS_CACHE_KEY = f"book:top5"
TOP5_BOOKS_LOCK_CACHE_KEY = f"book:top5:lock"



@router.get("/book/{id}" , status_code=status.HTTP_200_OK ,response_model=BookResponse)
async def get_book_by_id(db: db_dependency , cache: cache_dependency , id: int  ):


    key = f"book:id:{id}"
    cached_result = await cache.get(key)
    if cached_result:
        if cached_result == EMPTY_CACHE_VAL:
            raise HTTPException(status_code=404, detail="Book not found")
        return json.loads(cached_result)

    result = db.query(Book).filter(Book.id == id).first()

    if result is None:
        await cache.set(key, result)
        raise HTTPException(status_code=404, detail="Book not found")

    book_resp = BookResponse.model_validate(result)
    await cache.set(key, book_resp.model_dump_json())

    return book_resp




@router.get("/available/{id}" , status_code=status.HTTP_200_OK ,response_model=BookWithAvailabilityResponse)
async def get_book_availability(db: db_dependency  , id: int  ):

    book, available  = check_single_book(db, id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    book_simple_resp = BookResponse.model_validate(book)

    book_resp = BookWithAvailabilityResponse(
        **book_simple_resp.model_dump(),
        is_available = available
    )


    return book_resp







@router.get("/search_title/", status_code=status.HTTP_200_OK, response_model=list[BookResponse])
async def get_books_by_title( db: db_dependency, cache: cache_dependency, title: str , page:int):

    key = f"book:title:{title}__{str(page)}"

    cached_result = await cache.get_pydantic_list(key,BookResponse)
    if cached_result is not None:
        return cached_result

    # old API query, no need to unwrap with scalars
    results = db.query(Book).filter(Book.title.contains(title))
    results = order_and_paginate_query(results,Book.id,page)
    results_resp = [BookResponse.model_validate(result) for result in results.all()]

    await cache.set_pydantic_list(key, results_resp)

    return results_resp





@router.get("/search_author/", status_code=status.HTTP_200_OK ,response_model= list[BookResponse])
async def get_books_by_author(db: db_dependency, cache: cache_dependency,
                            author_id : int):


    key = f"book:author:{author_id}"
    cached_result = await cache.get_pydantic_list(key,BookResponse)
    if cached_result is not None:
        return cached_result

    stmt = select(Book).where(

        Book.writers.any(Author.id == author_id)
    )

    results = db.execute(stmt)

    # query returns rows with one column. Scalars extract that column
    results_resp = [BookResponse.model_validate(result) for result in results.scalars().all()]

    await cache.set_pydantic_list(key, results_resp)

    return results_resp





@router.get("/top5", status_code=status.HTTP_200_OK , response_model= list[BookResponse])
async def get_top5_recent_books(db: db_dependency, cache: cache_dependency):

    # will be used to block access to resources if cache has to be updated
    lock =  cache.get_lock(TOP5_BOOKS_LOCK_CACHE_KEY , 10)

    #attempt to read value from reddis
    key = TOP5_BOOKS_CACHE_KEY
    cached_result = await cache.get_pydantic_list(key, BookResponse)
    if cached_result is not None:
        return cached_result


    if lock is None:
        results = get_top_5_books(db, 7)
        results_resp = [BookResponse.model_validate(result) for result in results]
        return  results_resp



    got_lock = lock.acquire(blocking=False)
    if got_lock:
        try:

            #already a list
            results = get_top_5_books(db, 7)
            results_resp = [BookResponse.model_validate(result) for result in results]
            await cache.set_pydantic_list(key, results_resp, ex=24 * 60 * 60)

            return results_resp

        finally:
            # even if there is a return above, this should be executed
            lock.release()





    return JSONResponse(status_code=status.HTTP_202_ACCEPTED ,    content={"status": "processing", "message": "Please try again later."}
                    #, headers={"Retry-After": "3"}
                        )



