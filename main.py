import streamlit as st
import langchain_helper as lch

st.title("A.I. Agent Generator")

agent_type = st.sidebar.selectbox("Select an AI Agent:", 
                                  ("Creative Muse", "Code Auditor", "FitCoach", "SupportBot", "MoneyMaster"))

agent_labels = {
    "Creative Muse": "Describe the type of creative output you want:",
    "Code Auditor": "Describe the code or issue to audit:",
    "FitCoach": "Describe your fitness goal:",
    "SupportBot": "Describe the type of support you need:",
    "MoneyMaster": "Describe your financial goal:"
}

agent_prompt = st.sidebar.text_area(
    label=agent_labels[agent_type],
    max_chars=100
)

if agent_prompt:
    response = lch.select_agent_and_give_prompt(agent_type, agent_prompt)
    st.text(response)
