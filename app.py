#Main App For Running the GUI
import streamlit as st
from pathlib import Path
from pages import welcome, menu, lrjf_page, rr_page, battle_royal

# Load CSS
with open(Path("assets/styles.css")) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "welcome"

# Page routing
pages = {
    "welcome": welcome,
    "menu": menu,
    "lrjf": lrjf_page,
    "rr": rr_page,
    "battle": battle_royal
}

pages[st.session_state.page].show()
