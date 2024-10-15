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

# Fetch doctors data
def fetch_doctors():
    conn = get_connection()
    query = "SELECT * FROM doctors;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch staff data
def fetch_staff():
    conn = get_connection()
    query = "SELECT * FROM staff;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Add doctor function
def add_doctor(first_name, last_name, specialization, department, phone_number, email, availability, consultation_fees):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO doctors (first_name, last_name, specialization, department, phone_number, email, availability, consultation_fees)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (first_name, last_name, specialization, department, phone_number, email, availability, consultation_fees))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Doctor added successfully!")

# Add staff function
def add_staff(first_name, last_name, role, department, phone_number, email, shift_schedule):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO staff (first_name, last_name, role, department, phone_number, email, shift_schedule)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (first_name, last_name, role, department, phone_number, email, shift_schedule))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Staff added successfully!")

# Main function to run the application
def main():
    st.title("Doctors and Medical Staff")

    # Doctors section
    st.subheader("View Doctors")
    doctors_data = fetch_doctors()
    st.dataframe(doctors_data)

    st.subheader("Add New Doctor")
    with st.form(key='add_doctor_form'):
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        specialization = st.text_input("Specialization")
        department = st.text_input("Department")
        phone_number = st.text_input("Phone Number")
        email = st.text_input("Email")
        availability = st.text_input("Availability")
        consultation_fees = st.number_input("Consultation Fees", min_value=0.0, format="%.2f")
        submit_doctor_button = st.form_submit_button("Add Doctor")

        if submit_doctor_button:
            add_doctor(first_name, last_name, specialization, department, phone_number, email, availability, consultation_fees)

    # Staff section
    st.subheader("View Staff")
    staff_data = fetch_staff()
    st.dataframe(staff_data)

    st.subheader("Add New Staff")
    with st.form(key='add_staff_form'):
        staff_first_name = st.text_input("First Name", key='staff_first_name')
        staff_last_name = st.text_input("Last Name", key='staff_last_name')
        role = st.text_input("Role")
        staff_department = st.text_input("Department")
        staff_phone_number = st.text_input("Phone Number")
        staff_email = st.text_input("Email")
        shift_schedule = st.text_input("Shift Schedule")
        submit_staff_button = st.form_submit_button("Add Staff")

        if submit_staff_button:
            add_staff(staff_first_name, staff_last_name, role, staff_department, staff_phone_number, staff_email, shift_schedule)

# Run the main function
if __name__ == "__main__":
    main()
