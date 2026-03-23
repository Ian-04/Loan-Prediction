import streamlit as st 
import pandas as pd
import numpy as np 
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import requests

# Model url
MODEL_URL = "http://127.0.0.1:8000/predict"

#Setting the color
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, green, cyan);
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# Title
st.title('Predict Loan Amount')

# create drop down of names
# Access global data stored in session
if "df" in st.session_state:
    data = st.session_state.df  # use it here globally

data_model = st.session_state.get("df", pd.DataFrame())

#Drop down selection
if not data_model.empty:
    # --- Dropdown to select user ---
    selected_user = st.selectbox(
        "Select a User:",
        options=data_model["name"].unique()
    )

    # Filter data based on selection
    filtered_data = data_model[data_model["name"] == selected_user]
    
# User summary
if not filtered_data.empty:
    user_info = filtered_data[["name", "email", "education", "self_employed","no_of_dependents"]]
    asset_info = filtered_data[["residential_assets_value", "commercial_assets_value", "luxury_assets_value", "bank_asset_value"]]
    cibil_score = filtered_data[["name", "cibil_score"]]

    st.subheader("User Info")
    st.dataframe(user_info)

    st.subheader("Asset Info")
    st.dataframe(asset_info)
    
    st.subheader("CIBIL Score")
    st.dataframe(cibil_score)
    
# Predicting loan amount
if st.button("💰 Predict Loan Amount"):
    if not filtered_data.empty:
        payload = {
            "no_of_dependents": int(filtered_data["no_of_dependents"].values[0]),
            "income_annum": float(filtered_data["income_annum"].values[0]),
            "loan_term": int(filtered_data["loan_term"].values[0]),
            "cibil_score": int(filtered_data["cibil_score"].values[0]),
            "residential_assets_value": float(filtered_data["residential_assets_value"].values[0]),
            "commercial_assets_value": float(filtered_data["commercial_assets_value"].values[0]),
            "luxury_assets_value": float(filtered_data["luxury_assets_value"].values[0]),
            "bank_asset_value": float(filtered_data["bank_asset_value"].values[0]),
            'loan_term': str(filtered_data['loan_term'].values[0])
        }

        response = requests.post(MODEL_URL, json=payload)

        if response.status_code == 200:
            result = response.json()
            st.success(f"💰 Predicted Loan Amount: {result['predicted_loan_amount']:,.0f}")
            
            shap_df = pd.DataFrame({
                "feature": list(result["shap_values"].keys()),
                "impact": list((result["shap_values"].values()))
            }).sort_values(by="impact", key=abs, ascending=False)
            
            # Plot the impact
            positive = shap_df[shap_df["impact"] > 0]
            negative = shap_df[shap_df["impact"] < 0]
            
            # Positive impact
            st.write("✅ Increased Loan Amount")
            plt.figure(figsize=(12,6))
            sns.barplot(
                data= positive,
                y = 'feature',
                x = 'impact',
                palette = 'viridis'
            )
            plt.xlabel('Features')
            plt.ylabel('Impact')
                
            st.pyplot(plt, use_container_width=True)
            
            # Negative
            st.write("❌ Decreased Loan Amount")
            plt.figure(figsize=(12,6))
            sns.barplot(
                data= negative,
                y = 'feature',
                x = 'impact',
                palette = 'coolwarm'
            )
            plt.xlabel('Features')
            plt.ylabel('Impact')
                
            st.pyplot(plt, use_container_width=True)


