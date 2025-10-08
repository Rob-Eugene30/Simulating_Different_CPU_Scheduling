#For Tools guys dito rin nten gawin yung mga shi for the Gantt Chart and DataFrame
import matplotlib.pyplot as plt
import pandas as pd

def create_gantt_chart(gantt):
    fig, ax = plt.subplots(figsize=(8, 3))
    for pid, start, end in gantt:
        ax.barh(f"P{pid}", end - start, left=start, edgecolor='black')
        ax.text((start + end) / 2, f"P{pid}", f"P{pid}", ha='center', va='center', color='white')
    ax.set_xlabel("Time")
    ax.set_ylabel("Processes")
    ax.set_title("Gantt Chart")
    return fig

def to_dataframe(processes):
    return pd.DataFrame(processes, columns=["pid", "arrival", "burst", "completion", "turnaround", "waiting"])

def compute_averages(df):
    avg_wait = df["waiting"].mean()
    avg_turn = df["turnaround"].mean()
    return avg_wait, avg_turn
    
