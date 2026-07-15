from fastapi import FastAPI
from contextlib import asynccontextmanager

from library_app.auth.router import router as auth_router
from library_app.authors.router import router as authors_router
from library_app.books.router import router as books_router
from library_app.borrowers.router import router as borrowers_router
from library_app.core.env_settings import EnvSettings
from library_app.external.cache import configure_redis_at_app_start
from library_app.loans.router import router as loans_router



settings = EnvSettings()
is_test_mode = settings.ENV_MODE in ["test", "testing", "debug"]



#manages code that is executed right before app starts (and right after it ends if it was needed)
@asynccontextmanager
async def lifespan(app: FastAPI):

    await configure_redis_at_app_start()
    yield



app = FastAPI(
    docs_url="/docs" if is_test_mode else None,
    redoc_url="/redoc" if is_test_mode else None,
    lifespan=lifespan

)

app.include_router(auth_router)
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(borrowers_router)
app.include_router(loans_router)


# # old style
# @app.on_event("startup")
# def startup():
#     configure_redis_at_app_start()









