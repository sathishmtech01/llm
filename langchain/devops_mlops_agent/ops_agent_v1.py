import openai
import pandas as pd

# --- SETUP (use your own key) ---
openai.api_key = "your-openai-api-key"

# --- Sample log DataFrame ---
# Replace with your actual log data (all belonging to a single trace_id)
df = pd.DataFrame([
    {"timestamp": "2025-06-23T10:00:00", "service": "auth", "error_level": "INFO", "message": "Auth request received"},
    {"timestamp": "2025-06-23T10:00:01", "service": "auth", "error_level": "WARN", "message": "Token is nearing expiration"},
    {"timestamp": "2025-06-23T10:00:02", "service": "user", "error_level": "ERROR", "message": "User not found"},
    {"timestamp": "2025-06-23T10:00:03", "service": "user", "error_level": "ERROR", "message": "Exception in user lookup"},
    {"timestamp": "2025-06-23T10:00:04", "service": "gateway", "error_level": "INFO", "message": "Request ended with 500"},
])

# --- Sort logs by timestamp ---
df_sorted = df.sort_values("timestamp")

# --- Generate flow summary ---
flow_summary = "\n".join([
    f"- [{row.timestamp}] [{row.service}] [{row.error_level}]: {row.message}"
    for _, row in df_sorted.iterrows()
])

# --- Few-shot examples ---
few_shot_examples = """
Example Log Flow:
- [2025-06-20T09:15:03] [gateway] [INFO]: Incoming request received
- [2025-06-20T09:15:04] [auth] [INFO]: Token validated successfully
- [2025-06-20T09:15:05] [payment] [ERROR]: Timeout while calling external billing provider
- [2025-06-20T09:15:06] [payment] [ERROR]: Retrying billing request
- [2025-06-20T09:15:07] [payment] [FATAL]: Billing provider unreachable, aborting transaction
- [2025-06-20T09:15:08] [gateway] [INFO]: Request ended with 502 Bad Gateway

🔍 Root Cause Analysis Report:

🕒 Time of incident:
2025-06-20T09:15:05 to 09:15:08

📍 Flow Summary:
See above.

🚨 Error Highlights:
- `payment`: Timeout while calling billing provider
- Multiple retries followed by fatal error
- Gateway ended with 502

📌 Suspected Root Cause:
- `payment` service failed to connect to billing provider, causing a downstream failure.

🛠 Suggested Fix or Next Steps:
- Check billing provider health and network.
- Add circuit breaker to prevent retries.
"""

# --- Final prompt with few-shot + your log flow ---
final_prompt = f"""
You are an expert observability assistant performing root cause analysis (RCA) on a single trace of execution across services.

You are given a log flow. Each line includes:
- timestamp
- service
- error_level (DEBUG, INFO, WARN, ERROR, FATAL)
- message

All logs belong to one trace_id. Reconstruct the flow, identify issues, and suggest a fix.

{few_shot_examples}

Now analyze this log flow:

📍 Flow Summary:
{flow_summary}

🔍 Root Cause Analysis Report:
"""

# --- Call OpenAI API ---
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": final_prompt}],
    temperature=0.3
)

# --- Print the response ---
print(response.choices[0].message["content"])
