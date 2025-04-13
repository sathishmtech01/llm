import streamlit as st
from log_parser import parse_logs
from analyzer import classify_severity, assign_team
from openai_agent import get_recommendation

st.set_page_config(page_title="DevOps/MLOps Buddy", layout="wide")
st.title("🚀 DevOps & MLOps Log Buddy!")

uploaded_file = st.file_uploader("Upload your log file", type=["json", "csv", "txt"])

if uploaded_file:
    logs_df = parse_logs(uploaded_file)
    st.write("Parsed Logs:", logs_df.head())

    logs_df['severity'] = logs_df.apply(lambda row: classify_severity(str(row)), axis=1)
    logs_df['team'] = logs_df.apply(lambda row: assign_team(str(row)), axis=1)

    selected_idx = st.selectbox("Select a log entry to analyze:", logs_df.index)
    selected_log = str(logs_df.loc[selected_idx].to_dict())

    if st.button("Get Recommendation from GPT 🔍"):
        with st.spinner("Thinking..."):
            result = get_recommendation(selected_log)
        st.markdown("### 🤖 GPT Recommendation")
        st.markdown(result)

    st.markdown("### 🧾 Full Logs with Severity & Routing")
    st.dataframe(logs_df)
