# from openai import OpenAI
# import streamlit as st
#
# st.title("Testing Agent Framework!")
#
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
#
# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-3.5-turbo"
#
# if "messages" not in st.session_state:
#     st.session_state.messages = []
#
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
#
# if prompt := st.chat_input("What is up?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)
#
#     with st.chat_message("assistant"):
#         stream = client.chat.completions.create(
#             model=st.session_state["openai_model"],
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         )
#         response = st.write_stream(stream)
#     st.session_state.messages.append({"role": "assistant", "content": response})
import streamlit as st

def agent1(user_input):
    return f"Agent 1 processed: {user_input}"

def agent2(user_input):
    return f"Agent 2 processed: {user_input}"

def agent3(user_input):
    return f"Agent 3 processed: {user_input}"

def agent4(user_input):
    return f"Agent 4 processed: {user_input}"

def agent5(user_input):
    return f"Agent 5 processed: {user_input}"

def main():
    st.set_page_config(page_title="Agent Chat App", layout="wide")

    st.sidebar.title("Agents Sequence")
    agent_options = ["Agent 1", "Agent 2", "Agent 3", "Agent 4", "Agent 5"]

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_agent" not in st.session_state:
        st.session_state.current_agent = 0

    st.title("Chat with Agents in Sequence")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_input = st.text_input("Your message:", key="user_input")

    if st.button("Send") and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        agents = [agent1, agent2, agent3, agent4, agent5]
        current_agent = st.session_state.current_agent

        if current_agent < len(agents):
            response = agents[current_agent](user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.current_agent += 1
        else:
            st.session_state.current_agent = 0  # Reset after Agent 5

        st.rerun()

if __name__ == "__main__":
    main()
