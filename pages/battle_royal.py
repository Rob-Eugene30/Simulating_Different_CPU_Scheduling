import streamlit as st
from schedulers.simulation import run_simulation
from schedulers.utils import create_gantt_chart, to_dataframe, compute_averages

def show():
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown("<h1>🏆 Battle Royale: LRJF vs Round Robin</h1>", unsafe_allow_html=True)

    num_processes = st.number_input("Number of Processes", 1, 10, 3)
    processes = []
    for i in range(num_processes):
        arrival = st.number_input(f"Arrival Time (P{i+1})", 0, 50, 0, key=f"b_arr_{i}")
        burst = st.number_input(f"Burst Time (P{i+1})", 1, 50, 5, key=f"b_burst_{i}")
        processes.append({"pid": i+1, "arrival": arrival, "burst": burst})

    quantum = st.number_input("Quantum for RR", 1, 20, 4)

    if st.button("⚔ Run Battle", use_container_width=True):
        result_lrjf, gantt_lrjf = run_simulation("LRJF", [p.copy() for p in processes])
        result_rr, gantt_rr = run_simulation("Round Robin", [p.copy() for p in processes], quantum)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔵 LRJF")
            df = to_dataframe(result_lrjf)
            st.dataframe(df)
            avg_wait, avg_turn = compute_averages(df)
            st.info(f"Wait: {avg_wait:.2f}, Turn: {avg_turn:.2f}")
            st.pyplot(create_gantt_chart(gantt_lrjf))

        with col2:
            st.subheader("🟢 Round Robin")
            df = to_dataframe(result_rr)
            st.dataframe(df)
            avg_wait, avg_turn = compute_averages(df)
            st.info(f"Wait: {avg_wait:.2f}, Turn: {avg_turn:.2f}")
            st.pyplot(create_gantt_chart(gantt_rr))

    if st.button("⬅ Back to Menu", use_container_width=True):
        st.session_state.page = "menu"

    st.markdown('</div>', unsafe_allow_html=True)
