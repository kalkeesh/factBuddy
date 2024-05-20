import streamlit as st
import requests

base_url = "http://localhost:8000"

st.set_page_config(page_title="FactBuddy Chat Bot", page_icon=":robot_face:", layout="centered")

st.title("FactBuddy Chat Bot :robot_face:")
st.markdown("<h4 style='text-align: center; color: grey;'>Your smart assistant for task scheduling and quick information.</h4>", unsafe_allow_html=True)

def display_instructions():
    with st.expander("ℹ️ Instructions"):
        st.markdown("""
        ### How to Use FactBuddy Chat Bot:
        -**The chatbot can only answer the WH questions**
        - **Search for Facts**: Use the search bar to find quick information.
        - **Schedule a Task**: To schedule a task, your prompt should include:
          - The words **"schedule"** or **"task"**.
          - The task name should start with a **"-"** and end with **"at"**.
          - The time given should definitely contain **am** or **pm**.
        - **Case Insensitive**: The prompt is case insensitive.
        - **The tasks can be erased one at a time**.
        -**The tasks cann be completed one at a time.**
        """)

show_instructions = st.button("ℹ️ Instructions")
if show_instructions:
    display_instructions()

def section_title(title, color):
    st.markdown(f"<h2 style='color: {color};'>{title}</h2>", unsafe_allow_html=True)

with st.container():
    section_title("Schedule a Task", "#FF6347")
    with st.form(key='schedule_task_form'):
        col1, col2 = st.columns([4, 1])
        with col1:
            ques = st.text_input("Enter your query sir")
        with col2:
            submit_button = st.form_submit_button(label="search")
        if submit_button:
            response = requests.post(f"{base_url}/schedule_task/", json={"ques": ques})
            if response.status_code == 200:
                st.success(response.json())
            else:
                st.error(response.json()["detail"])

with st.container():
    section_title("Scheduled Tasks", "#32CD32")
    get_tasks_response = requests.get(f"{base_url}/tasks/")
    if get_tasks_response.status_code == 200:
        tasks = get_tasks_response.json()
        if tasks:
            selected_tasks = []
            for index, task in enumerate(tasks):
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.checkbox(f"Task: {task['task']} at {task['time']}", key=f"task_{index}"):
                        selected_tasks.append(task['task'])

            if st.button("Completed Task"):
                for task_name in selected_tasks:
                    delete_response = requests.delete(f"{base_url}/delete_task/", params={"task_name": task_name})
                    if delete_response.status_code == 200:
                        st.success(f"Deleted task: {task_name}")
                    else:
                        st.error(f"Failed to delete task: {task_name}")
        else:
            st.write("No tasks available for management.")
    else:
        st.error("Failed to retrieve tasks.")

st.markdown("---")

if __name__ == "__main__":
    st.title("Chatbot Task Operations")
