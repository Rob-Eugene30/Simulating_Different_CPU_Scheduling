import streamlit as st

def show():
    st.markdown("""
    <div class="container">
        <h1>💻 CPU Scheduling Simulator</h1>
        <p style="text-align:center;">
            Welcome to the interactive <strong>CPU Scheduling Simulator</strong>!<br>
            Explore how different CPU scheduling algorithms manage processes visually and intuitively.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Start"):
        st.session_state.page = "menu"
