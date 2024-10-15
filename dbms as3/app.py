import streamlit as st

# Set the page title
st.set_page_config(page_title="Hospital Management System", layout="wide")

# Sidebar for navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", [
    "Patient Information",
    "Appointments",
    "Doctors and Medical Staff",
    "Medical Records",
    "Billing and Finance",
    "Pharmacy",
    "Departments",
    "Room and Bed Management",
    "Reports",
    "Administration"
])

# Dynamic import of pages based on selection
if selection == "Patient Information":
    import pages.patient_information as page
elif selection == "Appointments":
    import pages.appointments as page
elif selection == "Doctors and Medical Staff":
    import pages.doctors_and_medical_staff as page
elif selection == "Medical Records":
    import pages.medical_records as page
elif selection == "Billing and Finance":
    import pages.billing_and_finance as page
elif selection == "Pharmacy":
    import pages.pharmacy as page
elif selection == "Departments":
    import pages.departments as page
elif selection == "Room and Bed Management":
    import pages.room_and_bed_management as page
elif selection == "Reports":
    import pages.reports as page
elif selection == "Administration":
    import pages.administration as page

# Check if the page has a main function and call it
if hasattr(page, 'main'):
    page.main()
else:
    st.error("The selected page does not have a main function.")
