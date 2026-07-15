from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


LIBRARY_DATABASE_URL = 'sqlite:///./library.db'




# since fastAPI may use different threads, we must allow the database connections to be used by multiple threads
engine = create_engine(LIBRARY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
