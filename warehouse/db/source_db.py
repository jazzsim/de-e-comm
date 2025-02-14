from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from dotenv import load_dotenv

import os

load_dotenv()

# Connect to PostgreSQL
DATABASE_URL = os.getenv('SOURCE_DB_URL')
engine = create_engine(DATABASE_URL)

Base = declarative_base()

def get_session() -> sessionmaker[Session]:
    Session = sessionmaker(bind=engine)
    return Session