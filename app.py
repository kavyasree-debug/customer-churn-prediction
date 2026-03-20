import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load model and scaler
model = pickle.load(open("churn_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

st.title("Customer Churn Prediction")

st.write("Enter Customer Details")

# Inputs
tenure = st.slider("Tenure (months)", 0, 72)
monthly_charges = st.number_input("Monthly Charges", 0.0, 200.0)

gender = st.selectbox("Gender", ["Male", "Female"])
contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
paperless = st.selectbox("Paperless Billing", ["Yes", "No"])

if st.button("Predict"):

    input_data = np.zeros((1, 30))  # adjust if needed

    # numeric
    input_data[0][0] = tenure
    input_data[0][1] = monthly_charges

    # simple encoding
    if gender == "Female":
        input_data[0][2] = 1

    if contract == "One year":
        input_data[0][3] = 1
    elif contract == "Two year":
        input_data[0][4] = 1

    if paperless == "Yes":
        input_data[0][5] = 1

    # fix warning
    input_df = pd.DataFrame(input_data)
    input_data = scaler.transform(input_df)

    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.error("Customer will churn ❌")
    else:
        st.success("Customer will stay ✅")