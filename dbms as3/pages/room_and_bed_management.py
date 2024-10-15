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

# Fetch rooms data
def fetch_rooms():
    conn = get_connection()
    query = "SELECT * FROM rooms;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Fetch bed allocations data
def fetch_bed_allocations():
    conn = get_connection()
    query = "SELECT * FROM bed_allocation;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Add room function
def add_room(room_number, room_type, availability_status, rate_per_day):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO rooms (room_number, room_type, availability_status, rate_per_day)
        VALUES (%s, %s, %s, %s);
    """, (room_number, room_type, availability_status, rate_per_day))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Room added successfully!")

# Add bed allocation function
def add_bed_allocation(patient_id, room_id, date_allocated, date_released):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bed_allocation (patient_id, room_id, date_allocated, date_released)
        VALUES (%s, %s, %s, %s);
    """, (patient_id, room_id, date_allocated, date_released))
    conn.commit()
    cursor.close()
    conn.close()
    st.success("Bed allocation added successfully!")

# Page content
st.title("Room and Bed Management")

# View Rooms section
st.subheader("View Rooms")
rooms_data = fetch_rooms()
st.dataframe(rooms_data)

# View Bed Allocations section
st.subheader("View Bed Allocations")
bed_allocations_data = fetch_bed_allocations()
st.dataframe(bed_allocations_data)

# Add New Room section
st.subheader("Add New Room")
with st.form(key='add_room_form'):
    room_number = st.text_input("Room Number")
    room_type = st.selectbox("Room Type", ["Single", "Double", "Suite", "ICU"])
    availability_status = st.selectbox("Availability Status", ["Available", "Occupied"])
    rate_per_day = st.number_input("Rate Per Day", min_value=0)
    submit_room_button = st.form_submit_button("Add Room")

    if submit_room_button:
        add_room(room_number, room_type, availability_status, rate_per_day)

# Add New Bed Allocation section
st.subheader("Add New Bed Allocation")
with st.form(key='add_bed_allocation_form'):
    patient_id = st.number_input("Patient ID", min_value=1)
    room_id = st.number_input("Room ID", min_value=1)
    date_allocated = st.date_input("Date Allocated")
    date_released = st.date_input("Date Released")
    submit_bed_allocation_button = st.form_submit_button("Allocate Bed")

    if submit_bed_allocation_button:
        add_bed_allocation(patient_id, room_id, date_allocated, date_released)
