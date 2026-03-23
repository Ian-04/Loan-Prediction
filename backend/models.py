from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()
class Loans(Base):
    __tablename__ = 'Loan_Request_data'
    __allow_unmapped__ = True
    
    loan_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    no_of_dependents = Column(Integer)
    education = Column(String)
    self_employed = Column(String)
    income_annum = Column(Integer)
    loan_amount = Column(Integer)
    loan_term = Column(Integer)
    cibil_score = Column(Integer)
    residential_assets_value = Column(Integer)
    commercial_assets_value = Column(Integer)
    luxury_assets_value = Column(Integer)
    bank_asset_value = Column(Integer)
    loan_status = Column(String)
