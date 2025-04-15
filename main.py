import asyncio
import threading
import streamlit as st
from modules.implementations.nodejs.team import NodeJsTeam
from modules.logging.logger import setup_logger
from modules.persistence.shared_pkl_memory import SharedPKLMemory
from streamlit_app import main
import logging

def run_team_worker(process_id):
   try:
        team = NodeJsTeam(process_id)
        asyncio.run(team.start_working())
   except Exception as e:
        memory = SharedPKLMemory(process_id)
        logger = logging.getLogger(__name__)
        logger.info(e)
        memory.get_memory("error").add("error",str(e))

# Initialize session state
if 'process_id' not in st.session_state:
    st.session_state.process_id = "9049507c-7f9b-42de-9981-252d62ea4231"
    setup_logger(st.session_state.process_id)

if 'team_thread_started' not in st.session_state:
    # Start background thread only once
    thread = threading.Thread(target=run_team_worker, args=(st.session_state.process_id,))
    thread.daemon = True
    thread.start()
    st.session_state.team_thread_started = True

# Run the Streamlit main app with persistent process_id
main(st.session_state.process_id)