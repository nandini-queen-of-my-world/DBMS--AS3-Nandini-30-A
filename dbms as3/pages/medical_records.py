import streamlit as st
import psycopg2
import pandas as pd

# Database connection function
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="hospital_management",
        user="postgres",
        password="nandini@108"
    )

# Fetch prescriptions data
def fetch_prescriptions():
    conn = get_connection()
    query = "SELECT * FROM prescriptions;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch lab tests data
def fetch_lab_tests():
    conn = get_connection()
    query = "SELECT * FROM lab_tests;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch vital signs data
def fetch_vital_signs():
    conn = get_connection()
    query = "SELECT * FROM vital_signs;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Add prescription function
def add_prescription(patient_id, doctor_id, date, medication, dosage, frequency):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO prescriptions (patient_id, doctor_id, date, medication, dosage, frequency)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (patient_id, doctor_id, date, medication, dosage, frequency))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Prescription added successfully!")

# Add lab test function
def add_lab_test(patient_id, test_name, test_date, results, doctor_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO lab_tests (patient_id, test_name, test_date, results, doctor_id)
        VALUES (%s, %s, %s, %s, %s);
    """, (patient_id, test_name, test_date, results, doctor_id))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Lab test added successfully!")

# Add vital sign function
def add_vital_sign(patient_id, date_time, blood_pressure, heart_rate, temperature):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO vital_signs (patient_id, date_time, blood_pressure, heart_rate, temperature)
        VALUES (%s, %s, %s, %s, %s);
    """, (patient_id, date_time, blood_pressure, heart_rate, temperature))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Vital sign added successfully!")

# Page content
st.title("Medical Records")

# Prescriptions section
st.subheader("View Prescriptions")
prescriptions_data = fetch_prescriptions()
st.dataframe(prescriptions_data)

st.subheader("Add New Prescription")
with st.form(key='add_prescription_form'):
    patient_id = st.number_input("Patient ID", min_value=1)
    doctor_id = st.number_input("Doctor ID", min_value=1)
    date = st.date_input("Date")
    medication = st.text_input("Medication")
    dosage = st.text_input("Dosage")
    frequency = st.text_input("Frequency")
    submit_prescription_button = st.form_submit_button("Add Prescription")

    if submit_prescription_button:
        add_prescription(patient_id, doctor_id, date, medication, dosage, frequency)

# Lab Tests section
st.subheader("View Lab Tests")
lab_tests_data = fetch_lab_tests()
st.dataframe(lab_tests_data)

st.subheader("Add New Lab Test")
with st.form(key='add_lab_test_form'):
    lab_patient_id = st.number_input("Patient ID", min_value=1, key='lab_patient_id')
    test_name = st.text_input("Test Name")
    test_date = st.date_input("Test Date")
    results = st.text_area("Results")
    lab_doctor_id = st.number_input("Doctor ID", min_value=1, key='lab_doctor_id')
    submit_lab_test_button = st.form_submit_button("Add Lab Test")

    if submit_lab_test_button:
        add_lab_test(lab_patient_id, test_name, test_date, results, lab_doctor_id)

# Vital Signs section
st.subheader("View Vital Signs")
vital_signs_data = fetch_vital_signs()
st.dataframe(vital_signs_data)

st.subheader("Add New Vital Sign")
with st.form(key='add_vital_sign_form'):
    vital_patient_id = st.number_input("Patient ID", min_value=1, key='vital_patient_id')
    date_time = st.datetime_input("Date and Time")
    blood_pressure = st.text_input("Blood Pressure")
    heart_rate = st.number_input("Heart Rate", min_value=0)
    temperature = st.number_input("Temperature", min_value=0.0, format="%.1f")
    submit_vital_sign_button = st.form_submit_button("Add Vital Sign")

    if submit_vital_sign_button:
        add_vital_sign(vital_patient_id, date_time, blood_pressure, heart_rate, temperature)
