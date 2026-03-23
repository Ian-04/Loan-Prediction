import pandas as pd 
import numpy as np

# Feature engineering function
def feature_engineering(data):
    # Drop unwanted columns
    cols_to_drop = ['name', 'email', 'loan_id', 'loan_status']
    data = data.drop(columns=[col for col in cols_to_drop if col in data.columns])
    
    # Borrowing capacity Features
    #Total assests
    data["total_assets"] = (data["residential_assets_value"] + data["commercial_assets_value"] + data["luxury_assets_value"] + data["bank_asset_value"])
    # Liquid asset ratio
    data["liquid_asset_ratio"] = (data["bank_asset_value"] /(data["total_assets"] + 1))
    # Asset diversification Score
    asset_cols = [
        "residential_assets_value",
        "commercial_assets_value",
        "luxury_assets_value",
        "bank_asset_value"
    ]
    data["asset_diversification"] = data[asset_cols].gt(0).sum(axis=1)
    
    # Income Based Features
    data["asset_income_ratio"] = (data["total_assets"] / (data["income_annum"] + 1))
    #Monthly Income
    data["income_monthly"] = data["income_annum"] / 12
    # Income per dependant
    data["income_per_dependent"] = (data["income_annum"] / (data["no_of_dependents"] + 1))
    
    # Credit Risk Features
    # credit Band
    bins = [300, 550, 650, 750, 900]
    labels = ["Poor", "Average", "Good", "Excellent"]
    data["credit_band"] = pd.cut(data["cibil_score"], bins=bins, labels=labels)
    # Financial stregnth and reliability
    data["income_credit_interaction"] = (data["income_annum"] * data["cibil_score"])  
    # Asset credit Interaction
    data["asset_credit_interaction"] = (data["total_assets"] * data["cibil_score"])
    # Asset Structure Features
    # Real estate wealth
    data["real_estate_assets"] = (data["residential_assets_value"] + data["commercial_assets_value"])
    # Luxury asset
    data["luxury_asset_ratio"] = (data["luxury_assets_value"] / (data["total_assets"] + 1))
    
    # Loan Structure
    # loan incomde
    data["income_term_ratio"] = (data["income_annum"] / (data["loan_term"] + 1))
    # Asset coverage ratio
    data["asset_coverage_ratio"] = (data["total_assets"] / (data["loan_term"] + 1))
    
    # Dependant ratio
    data["dependent_burden"] = (data["no_of_dependents"] / (data["income_annum"] + 1))
    
    # Drop NAs
    data = data.dropna()
    
    features = [
        'income_annum',
        'cibil_score',
        'luxury_asset_ratio',
        'liquid_asset_ratio',
        'residential_assets_value',
        'asset_income_ratio',
        'luxury_assets_value',
        'commercial_assets_value',
        'asset_coverage_ratio',
        'income_term_ratio',
        'bank_asset_value',
        'income_per_dependent',
        'real_estate_assets',
        'income_credit_interaction',
        'asset_credit_interaction',
        'dependent_burden',
        'total_assets',
        'loan_term'
    ]
    data_sel = data[features]
        
    return data_sel

# Log Normalization
def normalization(data):
    # Identify categorical features
    # Select all object columns
    object_cols = data.select_dtypes(include=["object", "category"]).columns
    object_cols = list(object_cols)


    for col in object_cols:
        data[col] = data[col].astype("category")
        
    # Normalize numeric columns
    for col in data.columns:
        if col not in object_cols:
            data[col] = np.log1p(data[col])
        
    return data  