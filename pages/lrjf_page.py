import streamlit as st
from schedulers.simulation import run_simulation
from schedulers.utils import create_gantt_chart, to_dataframe, compute_averages

def show():
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown("<h1>🔵 Longest Remaining Job First</h1>", unsafe_allow_html=True)

    num_processes = st.number_input("Number of Processes", 1, 10, 3)
    processes = []
    for i in range(num_processes):
        arrival = st.number_input(f"Arrival Time (P{i+1})", 0, 50, 0, key=f"arr_{i}")
        burst = st.number_input(f"Burst Time (P{i+1})", 1, 50, 5, key=f"burst_{i}")
        processes.append({"pid": i+1, "arrival": arrival, "burst": burst})

    if st.button("▶ Run Simulation", use_container_width=True):
        result, gantt = run_simulation("LRJF", processes)
        df = to_dataframe(result)
        st.dataframe(df, use_container_width=True)

        avg_wait, avg_turn = compute_averages(df)
        st.success(f"Average Waiting Time: {avg_wait:.2f}")
        st.success(f"Average Turnaround Time: {avg_turn:.2f}")
        st.pyplot(create_gantt_chart(gantt))

    if st.button("⬅ Back to Menu", use_container_width=True):
        st.session_state.page = "menu"

    st.markdown('</div>', unsafe_allow_html=True)
