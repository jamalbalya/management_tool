import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Backend API URL
API_URL = "http://127.0.0.1:8000"

# Title
st.title("Test Management Dashboard")

# Fetch Test Cases
@st.cache
def fetch_test_cases():
    response = requests.get(f"{API_URL}/testcases/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch test cases")
        return []

# Sidebar Filters
statuses = ["All", "New", "Pass", "Fail", "Blocked"]
status_filter = st.sidebar.selectbox("Filter by Status", statuses)

# Fetch and Filter Test Cases
test_cases = fetch_test_cases()
if status_filter != "All":
    test_cases = [tc for tc in test_cases if tc["status"] == status_filter]

# Display Test Cases
st.subheader("Test Cases")
df = pd.DataFrame(test_cases)
st.dataframe(df)

# Visualization
st.subheader("Test Case Status Distribution")
if df.empty:
    st.warning("No test cases available.")
else:
    status_counts = df["status"].value_counts()
    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Test Case Status Distribution",
    )
    st.plotly_chart(fig)

# Add New Test Case
st.subheader("Add New Test Case")
with st.form("add_test_case"):
    name = st.text_input("Test Case Name")
    description = st.text_area("Test Case Description")
    status = st.selectbox("Status", ["New", "Pass", "Fail", "Blocked"])
    submitted = st.form_submit_button("Add Test Case")

    if submitted:
        payload = {"name": name, "description": description, "status": status}
        response = requests.post(f"{API_URL}/testcases/", json=payload)
        if response.status_code == 200:
            st.success("Test case added successfully!")
        else:
            st.error("Failed to add test case.")
