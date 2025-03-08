import sys
import subprocess
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import random
import uvicorn
import getpass

openai_api_key = getpass.getpass(prompt='Openai Api Key')
openai.api_key = openai_api_key
app = FastAPI()

class StoryRequest(BaseModel):
    story: str

@app.get("/fetch_stories")
def fetch_stories():
    """Fetch Jira stories (simulated)."""
    return {"stories": ["Implement login feature", "Create user registration", "Build dashboard"]}

@app.post("/generate_code")
def generate_code(request: StoryRequest):
    """Generate code using OpenAI GPT."""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert software developer."},
            {"role": "user", "content": f"Generate Python code for: {request.story}"}
        ]
    )
    return {"code": response}

@app.post("/generate_tests")
def generate_tests(request: StoryRequest):
    """Generate unit tests using OpenAI GPT."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert software tester."},
            {"role": "user", "content": f"Generate unit tests for the following code:\n{request.story}"}
        ]
    )
    return {"test_code": response["choices"][0]["message"]["content"]}

@app.post("/run_tests")
def run_tests():
    """Simulate running tests and return results."""
    test_results = {
        "functional": "Functional tests passed",
        "security": "Security tests passed",
        "acceptance": "Acceptance tests passed",
        "coverage": f"Code coverage: {random.randint(85, 100)}%"
    }
    return test_results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)