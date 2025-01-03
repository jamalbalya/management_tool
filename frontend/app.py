import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Backend API URL
API_URL = "http://127.0.0.1:8000"

# Streamlit page configuration
st.set_page_config(page_title="Test Management Dashboard", layout="wide")

# Title and Description
st.title("Test Management Dashboard")
st.markdown("""
Manage your test cases efficiently. Add, view, and analyze test cases directly from this dashboard.
""")

# Fetch test cases from the backend
@st.cache_data
def fetch_test_cases():
    try:
        response = requests.get(f"{API_URL}/testcases/")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch test cases: {e}")
        return []

# Add a new test case
def add_test_case(name, description, status):
    try:
        data = {
            "name": name,
            "description": description,
            "status": status,
        }
        response = requests.post(f"{API_URL}/testcases/", json=data)
        response.raise_for_status()
        st.success("Test case added successfully!")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to add test case: {e}")

# Display Test Cases
st.header("Test Cases")
test_cases = fetch_test_cases()

if test_cases:
    df = pd.DataFrame(test_cases)
    st.write(df)

    # Display a status distribution chart
    if "status" in df.columns:
        fig = px.pie(df, names="status", title="Test Case Status Distribution")
        st.plotly_chart(fig)
else:
    st.warning("No test cases available.")

# Add New Test Case Form
st.header("Add New Test Case")
with st.form("add_test_case_form"):
    test_case_name = st.text_input("Test Case Name", placeholder="Enter test case name")
    test_case_description = st.text_area("Test Case Description", placeholder="Enter test case description")
    test_case_status = st.selectbox("Status", options=["New", "In Progress", "Completed"])
    submit_button = st.form_submit_button("Add Test Case")

    if submit_button:
        if test_case_name and test_case_description and test_case_status:
            add_test_case(test_case_name, test_case_description, test_case_status)
        else:
            st.error("Please fill out all fields to add a test case.")
