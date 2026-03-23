from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import joblib
import pandas as pd
import numpy as np
import models
import schemas
import crud
import shap
from sklearn.model_selection import train_test_split
import lightgbm as lgb
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from database import engine, SessionLocal
from feature_eng import feature_engineering, normalization

# DataBase
models.Base.metadata.create_all(bind=engine)

# Load the model
model = joblib.load("D:/end-to-end-projects/Loan_app_pred_app/GBM_Reg_Best_Model.pkl")

# API instance
app = FastAPI()

## Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get users with optional search
@app.get("/loan_data/", response_model=list[schemas.UserResponse])
def get_users_endpoint(search: str = None, db: Session = Depends(get_db)):
    return crud.get_users(db=db, search=search)

# Shap 
explainer = shap.TreeExplainer(model)

# Model predictions
@app.post("/predict")
def predict_loan(data: schemas.ModelInput):
    # Convert input to DataFrame
    # Convert dict → DataFrame
    df = pd.DataFrame([data.dict()])
    
    # Feature engineering
    df_feat = feature_engineering(df)

    # Optional: normalization (if used in training)
    df_norm = normalization(df_feat)
    # 🔥 SHAP VALUES
    shap_values = explainer.shap_values(df_norm)

    # Convert to dictionary (JSON serializable)
    shap_dict = dict(zip(df_norm.columns, shap_values[0]))

    # Predict
    preds_log = model.predict(df_norm)[0]
    prediction =  np.expm1(preds_log)
    return {
        "predicted_loan_amount": float(prediction),
        "shap_values": shap_dict
    }
