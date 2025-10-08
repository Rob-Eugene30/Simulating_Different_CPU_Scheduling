import streamlit as st

def show():
    st.markdown("""
    <div class="container">
        <h1>⚙️ Choose Your Simulation Mode</h1>
        <p style="text-align:center;">Select a scheduling algorithm to begin:</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔵 Longest Remaining Job First", use_container_width=True):
            st.session_state.page = "lrjf"
    with col2:
        if st.button("🟢 Round Robin", use_container_width=True):
            st.session_state.page = "rr"
    with col3:
        if st.button("🏆 Battle Royale", use_container_width=True):
            st.session_state.page = "battle"

    if st.button("⬅️ Back to Welcome", use_container_width=True):
        st.session_state.page = "welcome"
