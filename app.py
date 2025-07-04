import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="Lead Conversion Predictor")

st.title("Customer Conversion Prediction")

with st.form("prediction_form"):
    gender = st.selectbox("Gender", ['Male', 'Female'])
    location = st.selectbox("Location", ['Urban', 'Rural', 'Suburban'])
    source = st.selectbox("Source", ['Ad', 'Organic', 'Referral', 'SEO'])
    device = st.selectbox("Device", ['Mobile', 'Desktop'])
    age = st.number_input("Age", min_value=10, max_value=100)
    time_spent = st.number_input("Time Spent on Site (minutes)", min_value=0.0)
    pages_visited = st.number_input("Pages Visited", min_value=0)
    previous_purchases = st.number_input("Previous Purchases", min_value=0)
    campaign_engaged = st.selectbox("Campaign Engaged?", ['Yes', 'No'])

    submitted = st.form_submit_button("Predict Conversion")

if submitted:
    try:
        model = pickle.load(open('model.pkl', 'rb'))
        model_columns = pickle.load(open('model_columns.pkl', 'rb'))

        input_dict = {
            'age': age,
            'time_spent': time_spent,
            'pages_visited': pages_visited,
            'previous_purchases': previous_purchases,
            'campaign_engaged': 1 if campaign_engaged == 'Yes' else 0,
            'gender_Male': 1 if gender == 'Male' else 0,
            'location_Urban': 1 if location == 'Urban' else 0,
            'location_Rural': 1 if location == 'Rural' else 0,
            'source_Ad': 1 if source == 'Ad' else 0,
            'source_Organic': 1 if source == 'Organic' else 0,
            'source_Referral': 1 if source == 'Referral' else 0,
            'source_SEO': 1 if source == 'SEO' else 0,
            'device_Mobile': 1 if device == 'Mobile' else 0,
        }

        input_df = pd.DataFrame([input_dict])
        for col in model_columns:
            if col not in input_df.columns:
                input_df[col] = 0
        input_df = input_df[model_columns]

        prediction = model.predict(input_df)[0]
        st.success("User is likely to Convert!" if prediction == 1 else "User is Not likely to Convert.")
    except Exception as e:
        st.error(f"Error: {e}")
