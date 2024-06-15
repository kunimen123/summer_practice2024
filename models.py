# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    profile_level = Column(Integer, default=1)
    sales_count = Column(Integer, default=0)
    balance = Column(Float, default=0.0)
    items = relationship('Item', back_populates='owner')

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    item_type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship('User', back_populates='items')
