import streamlit as st 
import pandas as pd
import numpy as np 
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# define the url
BASE_URL = "http://127.0.0.1:8000/loan_data/"

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
st.title('Loan Demand Predictor')
# --- 1. Cached data loader ---
@st.cache_data
def load_data():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    return pd.DataFrame()

# --- 2. Load Data Button ---
if st.button("📥 Load Data"):
    st.session_state.df = load_data()
    st.success("Data loaded successfully!")

# --- 4. Access data safely ---
data = st.session_state.get("df", pd.DataFrame())
data = data.drop(columns = ['loan_amount'])

# Data Score cards
if not data.empty:
    #Compute metrics ---
    total_income = data['income_annum'].sum()
    avg_loan_term = data['loan_term'].mean()
    avg_asset_value = (data["residential_assets_value"] + 
                        data["commercial_assets_value"] + 
                        data["luxury_assets_value"] + 
                        data["bank_asset_value"]).mean()

    # Count approved/rejected loans
    approved_count = (data['loan_status'] == 'Approved').sum()
    rejected_count = (data['loan_status'] == 'Rejected').sum()
    approval_rate = (approved_count / (approved_count + rejected_count)) * 100

    # --- 5. Create scorecards ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Annual Income", f"{total_income:,.0f}")
    col2.metric("Avg Loan Term (months)", f"{avg_loan_term:.1f}")
    col3.metric("Avg Asset Value", f"{avg_asset_value:,.0f}")
    col4.metric("Approval Rate", f"{approval_rate:.1f}%")
    
# Data overview
st.subheader('Data Overview')
if not data.empty:
    st.dataframe(data.head())
    
if not data.empty:
     # Create a figure
    fig, ax = plt.subplots(figsize=(8,5))  # specify size

    # Plot histogram
    sns.histplot(
        data=data,
        x='income_annum',  # just column name
        kde=True,
        bins=50,
        ax=ax  # draw on this axis
    )

    # Titles and labels
    ax.set_title('Annual Income Distribution')
    ax.set_xlabel('Annual Income')
    ax.set_ylabel('Frequency')

    # Display the plot in Streamlit
    st.pyplot(fig)

