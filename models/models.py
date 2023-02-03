from sqlalchemy import Column, Integer, String, text, Float
from utils.db_handler import Base

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