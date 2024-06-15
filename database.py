# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Item

DATABASE_URL = 'sqlite:///marketplace.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)
