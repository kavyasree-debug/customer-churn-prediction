import streamlit as st
import pickle
import numpy as np
import pandas as pd
import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Customer Retention System", page_icon="📊")

# ---------------- LOGIN SYSTEM ----------------
# Multiple users
users = {
    "kavya": "1234",
    "admin": "admin123",
    "user1": "pass1"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success(f"Welcome {username} ✅")
        else:
            st.error("Invalid username or password ❌")

# ---------------- MAIN APP ----------------
if st.session_state.logged_in:

    st.title("📊 Customer Retention Dashboard")

    # Load model
    model = pickle.load(open("churn_model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))

    st.subheader("👤 Enter Customer Details")

    # Customer ID (IMPORTANT)
    customer_id = st.text_input("Customer ID")

    col1, col2 = st.columns(2)

    with col1:
        tenure = st.slider("Tenure (months)", 0, 72)
        gender = st.selectbox("Gender", ["Male", "Female"])

    with col2:
        monthly_charges = st.number_input("Monthly Charges", 0.0, 200.0)
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])

    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])

    st.markdown("---")

    if st.button("🔍 Predict Churn"):

        if customer_id == "":
            st.warning("Please enter Customer ID")
        else:

            input_data = np.zeros((1, 30))

            # Numeric
            input_data[0][0] = tenure
            input_data[0][1] = monthly_charges

            # Encoding
            if gender == "Female":
                input_data[0][2] = 1

            if contract == "One year":
                input_data[0][3] = 1
            elif contract == "Two year":
                input_data[0][4] = 1

            if paperless == "Yes":
                input_data[0][5] = 1

            input_df = pd.DataFrame(input_data)
            input_scaled = scaler.transform(input_df)

            prediction = model.predict(input_scaled)

            st.markdown("### 📢 Prediction Result")

            # Default action
            action_taken = "No Action"

            if prediction[0] == 1:
                st.error("⚠️ Customer is at HIGH RISK of Churn!")

                st.subheader("📩 Take Retention Action")

                action = st.selectbox("Choose Action", [
                    "Send Discount Offer",
                    "Request Feedback",
                    "Schedule Support Call"
                ])

                if action == "Send Discount Offer":
                    st.info("📧 Offer Sent: 20% discount")
                    action_taken = "Discount Offer"

                elif action == "Request Feedback":
                    st.info("📩 Feedback requested")

                    feedback = st.text_area("Customer Feedback")
                    rating = st.slider("Customer Rating", 1, 5)

                    if st.button("Save Feedback"):
                        with open("feedback.txt", "a") as f:
                            f.write(f"{customer_id}: {feedback} | Rating: {rating}\n")
                        st.success("Feedback saved")
                    action_taken = "Feedback Requested"

                elif action == "Schedule Support Call":
                    st.info("📞 Support team will contact")
                    action_taken = "Support Call"

            else:
                st.success("✅ Customer is likely to stay")

            # ---------------- SAVE DATA ----------------
            record = {
                "Customer ID": customer_id,
                "Tenure": tenure,
                "Monthly Charges": monthly_charges,
                "Prediction": "Churn" if prediction[0] == 1 else "No Churn",
                "Action": action_taken,
                "Timestamp": datetime.datetime.now()
            }

            df = pd.DataFrame([record])

            try:
                existing = pd.read_csv("customer_data.csv")
                df = pd.concat([existing, df], ignore_index=True)
            except:
                pass

            df.to_csv("customer_data.csv", index=False)

            st.success("✅ Record saved successfully")

    st.markdown("---")

    # ---------------- VIEW DATA ----------------
    st.subheader("📁 Customer History")

    try:
        data = pd.read_csv("customer_data.csv")
        st.dataframe(data)
    except:
        st.info("No records yet")

    st.markdown("---")

    # ---------------- GENERAL FEEDBACK ----------------
    st.subheader("⭐ General Feedback")

    feedback = st.text_area("Write feedback")
    rating = st.slider("Rate service", 1, 5)

    if st.button("Submit Feedback"):
        with open("feedback.txt", "a") as f:
            f.write(f"General: {feedback} | Rating: {rating}\n")
        st.success("Thank you for your feedback!")

    st.markdown("---")

    # ---------------- LOGOUT ----------------
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False