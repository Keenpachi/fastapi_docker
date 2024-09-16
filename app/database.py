from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

db_url = URL.create(
    "postgresql",
    username=os.getenv('username'),
    password=os.getenv('password'),
    host="localhost",
    database=os.getenv('database'),
)

engine = create_engine(db_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
