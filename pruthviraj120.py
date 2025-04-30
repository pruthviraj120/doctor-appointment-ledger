import streamlit as st
import pandas as pd
from datetime import datetime

# Title
st.title("Doctor Appointment Booking System")

# Sidebar - Admin Access
st.sidebar.header("Admin Panel")
admin_view = st.sidebar.checkbox("View Appointment Ledger")

# Form for Booking
with st.form("booking_form"):
    st.header("Book Your Appointment")

    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    doctor = st.selectbox("Select Doctor", ["Dr. Smith", "Dr. Johnson", "Dr. Emily"])
    date = st.date_input("Appointment Date")
    time = st.time_input("Appointment Time")

    submit = st.form_submit_button("Book Appointment")

# Ledger (in memory or CSV file)
def load_ledger():
    try:
        return pd.read_csv("appointments.csv")
    except FileNotFoundError:
        return pd.DataFrame(columns=["Timestamp", "Name", "Age", "Gender", "Doctor", "Date", "Time"])

def save_to_ledger(entry):
    ledger = load_ledger()
    ledger = pd.concat([ledger, pd.DataFrame([entry])], ignore_index=True)
    ledger.to_csv("appointments.csv", index=False)

# On Submit
if submit:
    if name and age and gender and doctor:
        appointment = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Doctor": doctor,
            "Date": date.strftime("%Y-%m-%d"),
            "Time": time.strftime("%H:%M"),
        }
        save_to_ledger(appointment)
        st.success("Appointment booked successfully!")
    else:
        st.error("Please fill in all fields.")

# Admin Ledger View
if admin_view:
    st.header("📋 Appointment Ledger")
    ledger_data = load_ledger()
    st.dataframe(ledger_data)
