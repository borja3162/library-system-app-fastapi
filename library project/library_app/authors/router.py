

from fastapi import APIRouter, HTTPException
import json
from starlette import status
from typing import Optional


from library_app.authors.author_service import search_authors_by_name_service
from library_app.db.session import db_dependency
from library_app.external.cache import cache_dependency , EMPTY_CACHE_VAL
from library_app.models import Author
from library_app.schemas.authors import AuthorResponse


router = APIRouter(prefix="/authors", tags=["authors"])

@router.get("/{id}" , status_code=status.HTTP_200_OK ,  response_model=Optional[AuthorResponse])
async def get_author_by_id(db: db_dependency , cache: cache_dependency, id: int  ):
    key = f"author:id:{id}"

    cached_result = await cache.get(key)
    if cached_result:
        if cached_result == EMPTY_CACHE_VAL:
            raise HTTPException(status_code=404, detail="Author not found")
        return json.loads(cached_result)


    result = db.query(Author).filter(Author.id == id).first()
    if result:
        result_resp = AuthorResponse.model_validate(result)
        await cache.set(key, result_resp.model_dump_json())
        return result_resp
    else:
        await cache.set(key, EMPTY_CACHE_VAL)
        raise HTTPException(status_code=404, detail="Author not found")








@router.get("/", status_code=status.HTTP_200_OK, response_model=list[AuthorResponse])
async def get_authors_by_name( db: db_dependency, cache: cache_dependency,
        first_name: str | None = None,
        last_name: str | None = None ):


    if(first_name == ""):
        first_name = None
    if (last_name == ""):
        last_name = None
    if( not first_name and not last_name ):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="At least one nonempty field is needed")


    #handles None cases too
    key = f"authors:name:{str(first_name)}__{str(last_name)}"
    cached_result = await cache.get_pydantic_list(key, AuthorResponse)
    if cached_result is not None:
        return cached_result

    results = search_authors_by_name_service(db,first_name,last_name)
    results_resp = [AuthorResponse.model_validate(result) for result in results]
    await cache.set_pydantic_list(key, results_resp)

    return results_resp

