import streamlit as st
from PIL import Image
from src.graph import interview_graph, GraphState

st.set_page_config(page_title="AI-Based MS Excel Mock", page_icon="🤖", layout="wide")
st.title("🤖 AI-Based MS Excel Mock")

# Initialize session state keys
if "messages" not in st.session_state:
    st.session_state.messages = []
if "graph_state" not in st.session_state:
    st.session_state.graph_state = None

def start_interview():
    """Kicks off a new interview."""
    st.session_state.messages = []
    
    # FIX: The initial state dictionary must contain all keys from GraphState
    initial_state: GraphState = {
        "task_id": "",
        "task_description": "",
        "task_file_path": "",
        "user_explanation": None,
        "user_screenshot": None,
        "evaluation": None,
        "tasks_completed": [],
        "interview_history": [],
        "final_report": None
    }
    
    with st.spinner("Preparing first task..."):
        response = interview_graph.invoke(initial_state)
    st.session_state.graph_state = response
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"### Task 1 of 5\n\n" + response['task_description'],
        "download_path": response['task_file_path'],
        "task_id": response['task_id']
    })

def handle_submission():
    """Processes the user's answer and gets the next step."""
    explanation = st.session_state.explanation_input
    screenshot_file = st.session_state.screenshot_input

    if not explanation and not screenshot_file:
        st.warning("Please provide an explanation, a screenshot, or both.")
        return

    current_state = st.session_state.graph_state
    if not current_state:
        st.error("Error: Interview state not found. Please restart.")
        return

    current_state['user_explanation'] = explanation
    current_state['user_screenshot'] = Image.open(screenshot_file) if screenshot_file else None
    
    with st.spinner("Evaluating and preparing next task..."):
        response = interview_graph.invoke(current_state)
    st.session_state.graph_state = response

    if not response.get("final_report"):
        task_num = len(response.get("tasks_completed", [])) + 1
        msg_content = f"Answer submitted. Here is your next task:\n\n### Task {task_num} of 5\n\n" + response['task_description']
        st.session_state.messages.append({"role": "assistant", "content": msg_content, "download_path": response['task_file_path'], "task_id": response['task_id']})
    else:
        st.session_state.messages.append({"role": "assistant", "content": response['final_report']})
    
    st.session_state.explanation_input = ""

# --- Main UI Logic ---
if not st.session_state.messages:
    st.header("AI-Powered MS Excel Interviewer")
    st.write("This is a 5-task mock interview to test your practical MS Excel skills, randomly chosen from a larger question bank.")
    st.button("Start Interview", on_click=start_interview, type="primary")
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "download_path" in msg:
                with open(msg["download_path"], "rb") as f:
                    st.download_button("Download Dataset", f, "task_data.csv", "text/csv", key=msg['task_id'])

    is_finished = st.session_state.graph_state and st.session_state.graph_state.get("final_report")
    
    if is_finished:
        st.success("Interview Complete!")
        st.balloons()
        if st.button("Start New Interview"):
            start_interview()
    else:
        with st.form(key="submission_form"):
            st.write("---")
            st.text_area("Your explanation (Optional):", key="explanation_input", height=150)
            st.file_uploader("Upload your screenshot (Optional):", type=["png", "jpg", "jpeg"], key="screenshot_input")
            st.form_submit_button("Submit Answer", on_click=handle_submission)