import streamlit as st
from pathlib import Path
from streamlit_autorefresh import st_autorefresh
import time
from modules.enums.stages import Stages
from modules.persistence.shared_pkl_memory import SharedPKLMemory
from modules.logging.logger import LOGS_PATH
from modules.utils.command_runner import run_commands
from modules.utils.commands import VsCodeCommands
from modules.utils.memory_based_input_handler import INPUT_MEMORY_KEY, INPUT_REQUESTS_KEY, INPUT_RESPONSES_KEY
import uuid


def display_developer_status(developer_state):
    """Display VSCode and file generation status in a styled container"""
    if developer_state is None:
        return

    st.markdown("""
    <style>
    .status-container {
        background-color: #f8fafc;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .status-text {
        font-size: 16px;
        background: linear-gradient(45deg, #3b82f6, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
    }
    .status-icon {
        font-size: 24px;
    }
    </style>
    """, unsafe_allow_html=True)

    total_files = len(developer_state['files'])
    generated_files = developer_state['current_file_index'] + 1

    st.markdown("<div class='status-container'>", unsafe_allow_html=True)
    
    # File generation status
    if total_files == 0:
        st.markdown('<span class="status-icon">📂</span><span class="status-text"> No files generated yet...</span>', unsafe_allow_html=True)
    elif generated_files == total_files:
        st.markdown('<span class="status-icon">🎉</span><span class="status-text"> All {total_files} files generated!</span>'.format(total_files=total_files), unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-icon">📄</span><span class="status-text"> {generated_files}/{total_files} files generated</span>'.format(generated_files=generated_files, total_files=total_files), unsafe_allow_html=True)

    # VSCode button
    if st.button("📁 Open in VSCode", key=f"vscode_button_{uuid.uuid4()}"):
        success = run_commands([VsCodeCommands.open_vscode()], cwd=developer_state['cwd'])[0].is_success
        if not success:
            st.error("Could not open VSCode. Make sure it's installed and in your PATH.")

    st.markdown("</div>", unsafe_allow_html=True)


def show_logs(log_path):
    """Display the most recent logs at the top of the page with animation"""
    st.markdown("""
    <style>
    .logs-container {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 20px;
        border-left: 4px solid #4CAF50;
    }
    @keyframes highlight {
        0% { background-color: #ffff99; }
        100% { background-color: transparent; }
    }
    .log-line-new {
        animation: highlight 2s ease-in-out;
    }
    .vscode-button {
        display: inline-flex;
        align-items: center;
        background-color: #0078d7;
        color: white;
        padding: 8px 16px;
        border-radius: 4px;
        cursor: pointer;
        text-decoration: none;
        font-weight: 500;
        margin-bottom: 15px;
        border: none;
        transition: background-color 0.3s;
    }
    .vscode-button:hover {
        background-color: #005a9e;
    }
    .vscode-icon {
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Store previous logs in session state to detect changes
    if 'previous_log_lines' not in st.session_state:
        st.session_state.previous_log_lines = []
    
    st.markdown("<div class='logs-container'>", unsafe_allow_html=True)
    
    st.markdown("### 🔍 Live Logs", unsafe_allow_html=True)
    
    if not Path(log_path).exists():
        st.info("No logs available yet")
    else:
        with open(log_path, "r") as f:
            lines = f.readlines()
        
        # Filter empty lines
        lines = [line for line in lines if line.strip()]
        last_lines = lines[-3:]
        
        log_container = st.empty()
        log_html = ""
        
        for i, line in enumerate(last_lines):
            line_stripped = line.strip()
            # Check if this line is new compared to previous state
            is_new = line_stripped not in st.session_state.previous_log_lines
            
            # Add animation class if the line is new
            animation_class = ' class="log-line-new"' if is_new else ''
            log_html += f'<pre{animation_class}><code>{line_stripped}</code></pre>'
        
        log_container.markdown(log_html, unsafe_allow_html=True)
        
        # Update previous logs
        st.session_state.previous_log_lines = [line.strip() for line in last_lines]
    
    st.markdown("</div>", unsafe_allow_html=True)


def render_input_form(memory: SharedPKLMemory):
    """Render enhanced input form with cooler styling"""
    inputs_memory = memory.get_memory(INPUT_MEMORY_KEY)
    inputs = inputs_memory.get(INPUT_REQUESTS_KEY)
    if not inputs:
        return False

    st.markdown("""
    <style>
    .input-form-container {
        background: linear-gradient(135deg, #1e3a8a, #3b82f6);
        border-radius: 10px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        animation: slideIn 0.5s ease-in-out;
        color: white;
    }
    @keyframes slideIn {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    .input-form-container h2 {
        font-size: 2em;
        margin-bottom: 20px;
        text-align: center;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid #93c5fd;
        border-radius: 5px;
        color: white;
        padding: 10px;
        transition: border-color 0.3s;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 8px rgba(96, 165, 250, 0.5);
    }
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #bfdbfe;
    }
    .stButton>button {
        background: linear-gradient(45deg, #10b981, #4ade80);
        color: white;
        padding: 12px 24px;
        border: none;
        border-radius: 5px;
        font-weight: 600;
        transition: all 0.3s;
        width: 100%;
        margin-top: 20px;
    }
    .stButton>button:hover {
        background: linear-gradient(45deg, #059669, #22c55e);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='input-form-container'>", unsafe_allow_html=True)
    st.markdown("## ✍️ Input Request")
    
    responses = []
    with st.form("input_form"):
        for i, inp_obj in enumerate(inputs):
            if inp_obj.multiline:
                val = st.text_area(inp_obj.title, placeholder=inp_obj.description, key=f"input_{i}")
            else:
                val = st.text_input(inp_obj.title, placeholder=inp_obj.description, key=f"input_{i}")
            responses.append(val)
            
        submitted = st.form_submit_button("Submit")
        if submitted:
            inputs_memory.add(INPUT_RESPONSES_KEY, responses)
            inputs_memory.delete(INPUT_REQUESTS_KEY)
            st.success("Responses submitted!")
            time.sleep(1)
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    return True


def main(process_id: str):
    st.set_page_config(
        layout="wide",
        page_title="Project Development Dashboard",
        page_icon="🚀"
    )

    # Add cool header
    st.markdown("""
    <style>
    .header-container {
        background: linear-gradient(45deg, #1e3a8a, #3b82f6);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header-title {
        font-size: 2.5em;
        font-weight: bold;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    </style>
    <div class='header-container'>
        <h1 class='header-title'>Project Development Agent</h1>
    </div>
    """, unsafe_allow_html=True)

    # Refresh the app periodically
    st_autorefresh(interval=1000, limit=None, key="refresh")

    memory = SharedPKLMemory(process_id)
    log_file_path = f"{LOGS_PATH}{process_id}.log"

    # Only show logs and status if input form is not active
    if not render_input_form(memory):
        # Display logs at the top
        show_logs(log_file_path)

        # Display the current Progress
        dev_memory = memory.get_memory(Stages.PROJECT_DEVELOPMENT)
        developer_state = dev_memory.get("graph_state")

        # Error
        if memory.get_memory("error") is not None and memory.get_memory("error").get("error") is not None:
            st.error(memory.get_memory("error").get("error"))
            st.text("Please check the complete logs for more details.")

        # Display developer status
        display_developer_status(developer_state)
