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

# Fetch departments data
def fetch_departments():
    conn = get_connection()
    query = "SELECT * FROM departments;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Add department function
def add_department(department_name, head_of_department, contact_info):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO departments (department_name, head_of_department, contact_info)
        VALUES (%s, %s, %s);
    """, (department_name, head_of_department, contact_info))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Department added successfully!")

# Main function to run the application
def main():
    st.title("Department Management")

    # View Departments section
    st.subheader("View Departments")
    departments_data = fetch_departments()
    st.dataframe(departments_data)

    # Add New Department section
    st.subheader("Add New Department")
    with st.form(key='add_department_form'):
        department_name = st.text_input("Department Name")
        head_of_department = st.text_input("Head of Department")
        contact_info = st.text_input("Contact Info")
        submit_department_button = st.form_submit_button("Add Department")

        if submit_department_button:
            add_department(department_name, head_of_department, contact_info)

# Run the main function
if __name__ == "__main__":
    main()
