from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""USING PSYCOPG"""

# conninfo = 'dbname=social_media user=postgres password=admin'

# try:
#     conn = psycopg2.connect(conninfo)
#     cur = conn.cursor()
#     print("Database was succesfully connected!")

# except Exception as e:
#     print(e)+
