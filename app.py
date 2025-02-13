import streamlit as st
import json
import os

# File operations
def load_tasks():
    """Load tasks from JSON file"""
    try:
        with open("tasks.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)

# Task operations
def add_task(new_task):
    """Add new task to list"""
    if new_task.strip():
        st.session_state.tasks.append({"name": new_task.strip(), "completed": False})
        save_tasks(st.session_state.tasks)

def delete_task(index):
    """Delete task from list"""
    del st.session_state.tasks[index]
    save_tasks(st.session_state.tasks)

def toggle_completion(index):
    """Toggle task completion status"""
    st.session_state.tasks[index]["completed"] = not st.session_state.tasks[index]["completed"]
    save_tasks(st.session_state.tasks)

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

# UI Layout
st.title("📝 To-Do List Manager")

# Add new task form
with st.form("new_task"):
    new_task = st.text_input("Add a new task:", placeholder="Enter task here...")
    add_cols = st.columns([3, 1])
    with add_cols[0]:
        submitted = st.form_submit_button("Add Task")
    with add_cols[1]:
        st.write("")  # Spacer

    if submitted:
        add_task(new_task)
        st.experimental_rerun()

# Display tasks
if not st.session_state.tasks:
    st.info("No tasks in your list! Add one above. 😊")
else:
    for index, task in enumerate(st.session_state.tasks):
        cols = st.columns([1, 6, 1, 1])
        
        # Completion checkbox
        with cols[0]:
            st.checkbox(
                f"task_{index}",
                value=task["completed"],
                on_change=toggle_completion,
                args=(index,),
                label_visibility="collapsed"
            )
        
        # Task text
        with cols[1]:
            if task["completed"]:
                st.markdown(f"<s>{task['name']}</s>", unsafe_allow_html=True)
            else:
                st.markdown(task["name"])
        
        # Edit button
        with cols[2]:
            if st.button("✏️", key=f"edit_{index}", help="Edit task"):
                st.session_state.edit_index = index
                st.experimental_rerun()
        
        # Delete button
        with cols[3]:
            st.button(
                "🗑️", 
                key=f"delete_{index}",
                on_click=delete_task,
                args=(index,),
                help="Delete task"
            )

# Edit task modal
if "edit_index" in st.session_state:
    index = st.session_state.edit_index
    original_task = st.session_state.tasks[index]["name"]
    
    with st.form("edit_form"):
        edited_task = st.text_input("Edit task:", value=original_task)
        cols = st.columns([3, 1])
        with cols[0]:
            if st.form_submit_button("Save Changes"):
                if edited_task.strip():
                    st.session_state.tasks[index]["name"] = edited_task.strip()
                    save_tasks(st.session_state.tasks)
                    del st.session_state.edit_index
                    st.experimental_rerun()
        with cols[1]:
            if st.form_submit_button("Cancel"):
                del st.session_state.edit_index
                st.experimental_rerun()
