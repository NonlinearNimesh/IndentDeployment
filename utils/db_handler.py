from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#conn_str = "mssql+pyodbc://LAPTOP-4184SVF7/medhavani_data?driver=SQL+Server+Native+Client+11.0&Trusted_Connection=yes"
conn_str = "mssql+pyodbc://LAPTOP-4184SVF7/medhavani_data?driver=SQL+Server+Native+Client+11.0&Trusted_Connection=yes"

engine = create_engine(conn_str)

Session = sessionmaker(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
