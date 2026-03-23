from pydantic import BaseModel
import pandas as pd
from typing import Optional

# Define request schema
class LoanRequest(BaseModel):
    loan_id: int
    name: str 
    email: str
    no_of_dependents: int
    education: str
    self_employed: str
    income_annum: int
    #loan_amount: int
    loan_term: int
    cibil_score: int
    residential_assets_value: int
    commercial_assets_value: int
    luxury_assets_value: int
    bank_asset_value: int
    loan_status: str
    
class ModelInput(BaseModel):
    income_annum: int
    cibil_score: int
    no_of_dependents: int   # ✅ REQUIRED
    residential_assets_value: int
    commercial_assets_value: int
    luxury_assets_value: int
    bank_asset_value: int
    loan_term: int
    
class UserResponse(BaseModel):
    name: str 
    email: str
    no_of_dependents: int
    education: str
    self_employed: str
    income_annum: int
    loan_amount: int
    loan_term: int
    cibil_score: int
    residential_assets_value: int
    commercial_assets_value: int
    luxury_assets_value: int
    bank_asset_value: int
    loan_status: str
    
    model_config = {
        "from_attributes": True
    }