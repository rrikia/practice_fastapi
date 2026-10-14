import time

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

load_dotenv(".env")

database_password = os.getenv("DATABASE_PASSWORD")
print("Password is not none", database_password is not None)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.DATABASE_USERNAME}:"
    f"{settings.DATABASE_PASSWORD}@"
    f"{settings.DATABASE_HOSTNAME}:"
    f"{settings.DATABASE_PORT}/"
    f"{settings.DATABASE_NAME}"
                            )

# engine responsible for sqlalchemy to connect to postgres

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# To talk to the database, use a session
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )

Base = declarative_base()

# Create a dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


database_password = os.getenv("DATABASE_PASSWORD")
print("Password is not none", database_password is not None)

# Establish a connection with the database 
# not necessary anymore, if you want to use postgresql library psycopg2 
# instead of sqlalchemy
while True:

    try:
        conn = psycopg2.connect(
            host=settings.DATABASE_HOSTNAME,
            port=settings.DATABASE_PORT, 
            dbname=settings.DATABASE_NAME, 
            user=settings.DATABASE_USERNAME, 
            password = database_password, 
            cursor_factory=RealDictCursor)
        # Open a cursor to perform database operations
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(2)