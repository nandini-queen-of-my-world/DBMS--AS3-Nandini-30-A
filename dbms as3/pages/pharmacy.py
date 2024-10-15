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

# Fetch medication inventory data
def fetch_medication_inventory():
    conn = get_connection()
    query = "SELECT * FROM medication_inventory;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch medication dispensation data
def fetch_medication_dispensation():
    conn = get_connection()
    query = "SELECT * FROM medication_dispensation;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Add medication function
def add_medication(name, quantity_in_stock, price, expiration_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO medication_inventory (name, quantity_in_stock, price, expiration_date)
        VALUES (%s, %s, %s, %s);
    """, (name, quantity_in_stock, price, expiration_date))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Medication added successfully!")

# Add dispensation function
def add_dispensation(patient_id, prescription_id, medication_id, quantity_dispensed, date_dispensed):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO medication_dispensation (patient_id, prescription_id, medication_id, quantity_dispensed, date_dispensed)
        VALUES (%s, %s, %s, %s, %s);
    """, (patient_id, prescription_id, medication_id, quantity_dispensed, date_dispensed))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Medication dispensed successfully!")

# Page content
st.title("Pharmacy Management")

# Medication Inventory section
st.subheader("View Medication Inventory")
medication_inventory_data = fetch_medication_inventory()
st.dataframe(medication_inventory_data)

st.subheader("Add New Medication")
with st.form(key='add_medication_form'):
    name = st.text_input("Medication Name")
    quantity_in_stock = st.number_input("Quantity in Stock", min_value=0)
    price = st.number_input("Price", min_value=0.0, format="%.2f")
    expiration_date = st.date_input("Expiration Date")
    submit_medication_button = st.form_submit_button("Add Medication")

    if submit_medication_button:
        add_medication(name, quantity_in_stock, price, expiration_date)

# Medication Dispensation section
st.subheader("View Medication Dispensation")
medication_dispensation_data = fetch_medication_dispensation()
st.dataframe(medication_dispensation_data)

st.subheader("Dispense Medication")
with st.form(key='add_dispensation_form'):
    patient_id = st.number_input("Patient ID", min_value=1)
    prescription_id = st.number_input("Prescription ID", min_value=1)
    medication_id = st.number_input("Medication ID", min_value=1)
    quantity_dispensed = st.number_input("Quantity Dispensed", min_value=1)
    date_dispensed = st.date_input("Date Dispensed")
    submit_dispensation_button = st.form_submit_button("Dispense Medication")

    if submit_dispensation_button:
        add_dispensation(patient_id, prescription_id, medication_id, quantity_dispensed, date_dispensed)
