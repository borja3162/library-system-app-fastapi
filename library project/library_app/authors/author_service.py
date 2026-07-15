from sqlalchemy import select

from library_app.models import  Author





def search_authors_by_name_service(
    db,
    first_name: str | None = None,
    last_name: str | None = None,
):
    stmt = select(Author)

    if first_name:
        stmt = stmt.where(Author.first_name == first_name)

    if last_name:
        stmt = stmt.where(Author.last_name == last_name)

    result = db.execute(stmt)
    return result.scalars().all()