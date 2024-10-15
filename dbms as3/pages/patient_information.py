import streamlit as st
import pandas as pd
import psycopg2

# Database connection function
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="hospital_management",
        user="postgres",
        password="nandini@108"
    )

# Fetch patient data
def fetch_patients():
    conn = get_connection()
    query = "SELECT * FROM patients;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Add patient function
def add_patient(first_name, last_name, date_of_birth, gender, address, phone_number, email, emergency_contact, insurance_details, blood_group):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO patients (first_name, last_name, date_of_birth, gender, address, phone_number, email, emergency_contact, insurance_details, blood_group)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (first_name, last_name, date_of_birth, gender, address, phone_number, email, emergency_contact, insurance_details, blood_group))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Patient added successfully!")

# Main function for the page
def main():
    st.title("Patient Information")
    st.subheader("View Patients")
    patients_data = fetch_patients()
    st.dataframe(patients_data)

    st.subheader("Add New Patient")
    with st.form(key='add_patient_form'):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        date_of_birth = st.date_input("Date of Birth")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        address = st.text_area("Address")
        phone_number = st.text_input("Phone Number")
        email = st.text_input("Email")
        emergency_contact = st.text_input("Emergency Contact")
        insurance_details = st.text_area("Insurance Details")
        blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        submit_button = st.form_submit_button("Add Patient")

        if submit_button:
            add_patient(first_name, last_name, date_of_birth, gender, address, phone_number, email, emergency_contact, insurance_details, blood_group)

# Only include this if the file is run directly (not needed for imports)
if __name__ == "__main__":
    main()
