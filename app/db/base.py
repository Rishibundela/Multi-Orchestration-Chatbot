# app/db/base.py
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Standard SQLAlchemy 2.0 base class"""
    pass