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

# Fetch discharge summaries data
def fetch_discharge_summaries():
    conn = get_connection()
    query = """
        SELECT ds.summary_id, p.first_name, p.last_name, ds.discharge_date, ds.diagnosis, 
               ds.treatment_provided, d.first_name AS doctor_first_name, d.last_name AS doctor_last_name 
        FROM discharge_summary ds
        JOIN patients p ON ds.patient_id = p.patient_id
        JOIN doctors d ON ds.doctor_id = d.doctor_id;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Page content
st.title("Reports")

# View Discharge Summaries section
st.subheader("View Discharge Summaries")
discharge_summaries_data = fetch_discharge_summaries()
st.dataframe(discharge_summaries_data)

# Generate Report section
st.subheader("Generate Discharge Summary Report")
with st.form(key='generate_report_form'):
    patient_id = st.number_input("Patient ID", min_value=1)
    submit_report_button = st.form_submit_button("Generate Report")

    if submit_report_button:
        # Fetch specific discharge summary
        conn = get_connection()
        query = """
            SELECT ds.summary_id, p.first_name, p.last_name, ds.discharge_date, ds.diagnosis, 
                   ds.treatment_provided, d.first_name AS doctor_first_name, d.last_name AS doctor_last_name 
            FROM discharge_summary ds
            JOIN patients p ON ds.patient_id = p.patient_id
            JOIN doctors d ON ds.doctor_id = d.doctor_id
            WHERE p.patient_id = %s;
        """
        df = pd.read_sql(query, conn, params=(patient_id,))
        conn.close()
        
        if not df.empty:
            st.write(f"Discharge Summary for Patient ID {patient_id}:")
            st.dataframe(df)
        else:
            st.warning("No discharge summary found for this patient ID.")
