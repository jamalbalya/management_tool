import streamlit as st
import requests
import json

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"

# Helper function to handle errors gracefully
def handle_error(response):
    if response.status_code != 200:
        st.error(f"Error: {response.text}")
        return None
    return response.json()

# Fetch test cases from backend
def fetch_test_cases():
    response = requests.get(f"{BACKEND_URL}/testcases/")
    return handle_error(response)

# Add a new test case to the backend
def add_test_case(name, description, status):
    payload = {
        "name": name,
        "description": description,
        "status": status,
    }
    response = requests.post(f"{BACKEND_URL}/testcases/", json=payload)
    return handle_error(response)

# Streamlit UI
st.title("Test Management Dashboard")

# Fetch test cases
test_cases = fetch_test_cases()

if test_cases is not None:
    if not test_cases:
        st.write("No test cases available.")
    else:
        st.subheader("Test Cases")
        for test_case in test_cases:
            st.write(f"**{test_case['name']}**")
            st.write(f"Description: {test_case['description']}")
            st.write(f"Status: {test_case['status']}")
            st.write("---")

# Add a new test case form
st.subheader("Add New Test Case")
name = st.text_input("Test Case Name")
description = st.text_area("Test Case Description")
status = st.selectbox("Status", ["New", "In Progress", "Completed"])

if st.button("Add Test Case"):
    result = add_test_case(name, description, status)
    if result is not None:
        st.success("Test case added successfully!")
    else:
        st.error("Failed to add test case.")
