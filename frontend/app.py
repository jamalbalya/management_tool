from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

# Models
class TestCase(BaseModel):
    id: int
    name: str
    description: str
    linked_issue: str = None

test_cases = []

# Test Case Endpoints
@app.post("/testcases/")
def create_test_case(test_case: TestCase):
    test_cases.append(test_case)
    return {"message": "Test case created successfully", "test_case": test_case}

@app.get("/testcases/")
def list_test_cases():
    return test_cases

@app.get("/testcases/{test_case_id}")
def get_test_case(test_case_id: int):
    for test in test_cases:
        if test.id == test_case_id:
            return test
    raise HTTPException(status_code=404, detail="Test case not found")

# Jira Integration
@app.post("/jira/link")
def link_test_case_to_jira(test_case_id: int, issue_id: str):
    jira_url = "https://yourcompany.atlassian.net/rest/api/3/issue"
    headers = {"Authorization": "Bearer YOUR_JIRA_API_TOKEN", "Content-Type": "application/json"}

    payload = {
        "fields": {
            "description": f"Linked to Test Case {test_case_id}",
        }
    }

    response = requests.put(f"{jira_url}/{issue_id}", json=payload, headers=headers)

    if response.status_code == 204:
        return {"message": "Test case linked to Jira issue successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
