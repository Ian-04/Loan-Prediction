from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from urllib.parse import quote_plus

password = quote_plus("Data@254")   # your real password
db_url = f'postgresql://postgres:{password}@localhost:5432/Loan_Demand'
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)