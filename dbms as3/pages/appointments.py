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

# Fetch appointment data
def fetch_appointments():
    conn = get_connection()
    query = "SELECT * FROM appointments;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Main function to run the application
def main():
    st.title("Appointments")
    st.subheader("View Appointments")
    appointments_data = fetch_appointments()
    st.dataframe(appointments_data)

# Run the main function
if __name__ == "__main__":
    main()
