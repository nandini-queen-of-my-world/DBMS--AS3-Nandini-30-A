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

# Fetch user data
def fetch_users():
    conn = get_connection()
    query = """
        SELECT user_id, username, role, last_login 
        FROM users;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch access logs
def fetch_access_logs():
    conn = get_connection()
    query = """
        SELECT log_id, user_id, action, timestamp 
        FROM access_logs;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Add a new user
def add_user(username, password, role, staff_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO users (username, password, role, staff_id) 
            VALUES (%s, %s, %s, %s);
        """, (username, password, role, staff_id))
        conn.commit()
    conn.close()

# Main function to run the application
def main():
    st.title("Administration")

    # View Users section
    st.subheader("View Users")
    users_data = fetch_users()
    st.dataframe(users_data)

    # View Access Logs section
    st.subheader("View Access Logs")
    access_logs_data = fetch_access_logs()
    st.dataframe(access_logs_data)

    # Add User section
    st.subheader("Add New User")
    with st.form(key='add_user_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["Admin", "Doctor", "Nurse", "Staff"])
        staff_id = st.number_input("Staff ID", min_value=1)

        submit_user_button = st.form_submit_button("Add User")
        
        if submit_user_button:
            try:
                add_user(username, password, role, staff_id)
                st.success("User added successfully!")
            except Exception as e:
                st.error(f"Error adding user: {e}")

# Run the main function
if __name__ == "__main__":
    main()
