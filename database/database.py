# Intialization of database
import os 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base





URL_DATABASE = os.getenv(
    "DATABASE_URL",
     "postgresql://postgres:asad123@localhost:5432/ApiForge"
)

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autoflush=False,bind=engine)

Base = declarative_base()