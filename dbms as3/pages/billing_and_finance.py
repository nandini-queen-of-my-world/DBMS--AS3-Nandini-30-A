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

# Fetch invoices data
def fetch_invoices():
    conn = get_connection()
    query = "SELECT * FROM invoices;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch payments data
def fetch_payments():
    conn = get_connection()
    query = "SELECT * FROM payments;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Add invoice function
def add_invoice(patient_id, appointment_id, total_amount, payment_status, payment_method):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO invoices (patient_id, appointment_id, total_amount, payment_status, payment_method) 
        VALUES (%s, %s, %s, %s, %s);
    """, (patient_id, appointment_id, total_amount, payment_status, payment_method))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Invoice added successfully!")

# Add payment function
def add_payment(invoice_id, payment_date, amount_paid, payment_method):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(""" 
        INSERT INTO payments (invoice_id, payment_date, amount_paid, payment_method) 
        VALUES (%s, %s, %s, %s);
    """, (invoice_id, payment_date, amount_paid, payment_method))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Payment added successfully!")

# Main function to run the application
def main():
    st.title("Billing and Finance")

    # Invoices section
    st.subheader("View Invoices")
    invoices_data = fetch_invoices()
    st.dataframe(invoices_data)

    st.subheader("Add New Invoice")
    with st.form(key='add_invoice_form'):
        patient_id = st.number_input("Patient ID", min_value=1)
        appointment_id = st.number_input("Appointment ID", min_value=1)
        total_amount = st.number_input("Total Amount", min_value=0.0, format="%.2f")
        payment_status = st.selectbox("Payment Status", options=["Paid", "Pending", "Cancelled"])
        payment_method = st.selectbox("Payment Method", options=["Cash", "Credit Card", "Insurance", "Online"])
        submit_invoice_button = st.form_submit_button("Add Invoice")

        if submit_invoice_button:
            add_invoice(patient_id, appointment_id, total_amount, payment_status, payment_method)

    # Payments section
    st.subheader("View Payments")
    payments_data = fetch_payments()
    st.dataframe(payments_data)

    st.subheader("Add New Payment")
    with st.form(key='add_payment_form'):
        invoice_id = st.number_input("Invoice ID", min_value=1)
        payment_date = st.date_input("Payment Date")
        amount_paid = st.number_input("Amount Paid", min_value=0.0, format="%.2f")
        payment_method = st.selectbox("Payment Method", options=["Cash", "Credit Card", "Insurance", "Online"])
        submit_payment_button = st.form_submit_button("Add Payment")

        if submit_payment_button:
            add_payment(invoice_id, payment_date, amount_paid, payment_method)

# Run the main function
if __name__ == "__main__":
    main()
