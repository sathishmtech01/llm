from openai import OpenAI
import streamlit as st
from io import StringIO
st.set_page_config(page_title="Agent Chat App", layout="wide")
st.title("Testing Agent Framework!")
st.sidebar.title("Agents Sequence")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
with st.sidebar.expander("Agent 1 - Requirerments"):
    # Add file uploader in the sidebar
    requirements = st.text_area(
        "Enter the requirements or upload directly",

    )
    uploaded_file = st.file_uploader("Upload file", type=["txt"])
    # Check if a file has been uploaded
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        st.write(f"Filename: {uploaded_file.name}")
    agent1 = st.button("Execute Agent 1")
response1=""
if agent1:
    st.session_state.messages.append({"role": "user", "content": requirements})
    with st.chat_message("user"):
        st.markdown(requirements)

    with st.chat_message("assistant"):
        prompt_agent1 = " give one jira story"
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.response1 = response

    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar.expander("Agent 2 - Code"):
    file2 = st.text_input("enter file name ")
    agent2 = st.button("Execute Agent 2")
    feedback2 = st.text_input("user feedback ")
    feedbackagent2 = st.button("Execute with feedback")

if agent2:
    prompt_2 = st.session_state.response1+" give only code in python"
    st.session_state.messages.append({"role": "user", "content": prompt_2})
    with st.chat_message("user"):
        st.markdown(st.session_state.response1)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.response2 = response
    st.session_state.messages.append({"role": "assistant", "content": response})

if feedbackagent2:
    fbprompt_2 = st.session_state.response2+" "+feedback2
    st.session_state.messages.append({"role": "user", "content": fbprompt_2})
    with st.chat_message("user"):
        st.markdown(fbprompt_2)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.response2 = response
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar.expander("Agent 3 - Test case"):
    file3 = st.text_input("enter file name")
    agent3 = st.button("Execute Agent 3")
    feedback3 = st.text_input("user feedback")
    feedbackagent3 = st.button("Execute with feedback ")

if agent3:
    prompt_3 = st.session_state.response2+" give testcase for the given code in python"
    st.session_state.messages.append({"role": "user", "content": prompt_3})
    with st.chat_message("user"):
        st.markdown(prompt_3)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.response3 = response
    st.session_state.messages.append({"role": "assistant", "content": response})

if feedbackagent3:
    fbprompt_3 = st.session_state.response3+" "+feedback3
    st.session_state.messages.append({"role": "user", "content": fbprompt_3})
    with st.chat_message("user"):
        st.markdown(fbprompt_3)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.response3 = response
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar.expander("Agent 4 - Interpret"):
    file4 = st.text_input("enter file name4")
    agent4 = st.button("Execute Agent 4")
    feedback4 = st.text_input("user feedback4")
    feedbackagent4 = st.button("Execute with feedback4")

if agent4:
    prompt_4 = st.session_state.response2+st.session_state.response3+" give test coverage of the code and test case, give in output 10%,20,..100%"
    st.session_state.messages.append({"role": "user", "content": prompt_4})
    with st.chat_message("user"):
        st.markdown(prompt_4)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.response3 = response
    st.session_state.messages.append({"role": "assistant", "content": response})

if feedbackagent3:
    fbprompt_4 = st.session_state.response4+" "+feedback4
    st.session_state.messages.append({"role": "user", "content": fbprompt_4})
    with st.chat_message("user"):
        st.markdown(fbprompt_4)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
        st.session_state.response3 = response
    st.session_state.messages.append({"role": "assistant", "content": response})

with st.sidebar.expander("Agent 5 - Summary"):
    save_code = st.button("Save code")
    save_test = st.button("Save test case")
    feedback5 = st.text_input("Commit message")
    comit_code = st.button("Commit code")





