from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

# SQLALCHEMY_DATABASE_URL = (f'postgresql://{settings.DATABASE_USERNAME}'
#                            f':{settings.DATABASE_PASSWORD}'
#                            f'@{settings.DATABASE_HOSTNAME}'
#                            f':{settings.DATABASE_PORT}'
#                            f'/{settings.DATABASE_NAME}')

# SQLALCHEMY_DATABASE_URL = "sqlite://"

SQLALCHEMY_DATABASE_URL = (f'postgresql://{settings.DATABASE_USERNAME }'
                           f'@localhost'
                           f':{settings.DATABASE_PORT}'
                           f'/{settings.DATABASE_NAME}')


engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
