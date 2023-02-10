from sqlalchemy import Column, Integer, String, text, Float, DateTime
from utils.db_handler import Base
import datetime

class DataNew(Base):
    __tablename__ = 'data_new_new_new_new'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    divn = Column(String(256), index=True)
    season = Column(String(256), index=True)
    center = Column(Integer, index=True)
    center_name = Column(String(256), index=True)
    date = Column(String(256), index=True)
    indent = Column(Integer, index=True)
    purchase = Column(Float, index=True)
    reciept = Column(Float, index=True)
    predicted_indent = Column(String(256), index=True)


class Users(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    username = Column(String(255), index=True, nullable=False, unique=True)
    password = Column(String(255), index=True, nullable=False)
    email = Column(String(255), index=True, nullable=False)
    role = Column(String(255), index=True, nullable=False)
    secret_key = Column(String(100), index=True, nullable=False)
    key_expires = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    created_on = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)