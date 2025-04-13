from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def get_recommendation(log_entry):
    prompt = f"""
    Analyze the following log entry and give:
    1. Summary
    2. Possible root cause
    3. Recommended action

    Log Entry:
    {log_entry}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    response_dict = response.model_dump()    # <--- convert to dictionary
    response_message = response_dict["choices"][0]["message"]["content"]
    response_message

    return response_message
