import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ---------- CONFIG ----------
DEFAULT_N = 5
DEFAULT_SPEED = 1.0  # 1.0 = 1 sec/tick, higher = faster

# ---------- GENERATE RANDOM PROCESSES ----------
def generate_processes(n=5, arrival_max=8, burst_min=2, burst_max=6):
    processes = []
    for i in range(1, n + 1):
        processes.append({
            'PID': f'P{i}',
            'ArrivalTime': random.randint(0, arrival_max),
            'BurstTime': random.randint(burst_min, burst_max)
        })
    return sorted(processes, key=lambda x: x['ArrivalTime'])

# ---------- FCFS LOGIC ----------
def fcfs_schedule(processes):
    current_time = 0
    schedule = []
    for p in processes:
        if current_time < p['ArrivalTime']:
            current_time = p['ArrivalTime']
        start = current_time
        end = start + p['BurstTime']
        schedule.append((p['PID'], start, end))
        current_time = end
    return schedule

# ---------- METRICS ----------
def compute_metrics(processes, schedule):
    for i, p in enumerate(processes):
        p['StartTime'] = schedule[i][1]
        p['CompletionTime'] = schedule[i][2]
        p['TurnaroundTime'] = p['CompletionTime'] - p['ArrivalTime']
        p['WaitingTime'] = p['TurnaroundTime'] - p['BurstTime']
    df = pd.DataFrame(processes)
    avg_tat = df['TurnaroundTime'].mean()
    avg_wt = df['WaitingTime'].mean()
    return df, avg_tat, avg_wt

# ---------- ANIMATION ----------
def animate_fcfs(processes, schedule, avg_tat, avg_wt, speed):
    colors = plt.cm.tab10.colors
    total_time = max(end for _, _, end in schedule)

    fig, ax = plt.subplots(figsize=(10, 4))
    pids = [p['PID'] for p in processes]
    ax.set_yticks(range(len(pids)))
    ax.set_yticklabels(pids)
    ax.set_xlim(0, total_time + 1)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Processes")
    ax.grid(True, axis='x', linestyle='--', alpha=0.5)

    def update(frame):
        ax.clear()
        ax.set_title(f"🧠 FCFS Simulation — Time: {frame}s")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Processes")
        ax.set_yticks(range(len(pids)))
        ax.set_yticklabels(pids)
        ax.set_xlim(0, total_time + 1)
        ax.grid(True, axis='x', linestyle='--', alpha=0.5)

        # Draw processes
        for i, (pid, start, end) in enumerate(schedule):
            if frame >= end:
                ax.barh(i, end - start, left=start, color=colors[i % len(colors)], edgecolor='black')
            elif frame > start:
                ax.barh(i, frame - start, left=start, color='gold', edgecolor='black')
            if start <= frame < end:
                ax.text(frame, i, f"⏳ {pid}", ha='left', va='center', color='black', fontweight='bold')

        # Metrics panel
        ax.text(total_time * 0.65, len(pids) - 0.3,
                f"Avg Turnaround: {avg_tat:.2f}\nAvg Waiting: {avg_wt:.2f}",
                fontsize=10, bbox=dict(facecolor='white', alpha=0.8))

    ani = FuncAnimation(fig, update, frames=range(total_time + 2),
                        interval=1000 / speed, repeat=False)
    plt.show()

# ---------- MAIN ----------
if __name__ == "__main__":
    try:
        n = int(input(f"Enter number of processes (default {DEFAULT_N}): ") or DEFAULT_N)
        speed = float(input(f"Enter speed multiplier (default {DEFAULT_SPEED}): ") or DEFAULT_SPEED)
    except ValueError:
        n, speed = DEFAULT_N, DEFAULT_SPEED

    processes = generate_processes(n)
    schedule = fcfs_schedule(processes)
    df, avg_tat, avg_wt = compute_metrics(processes, schedule)

    print("\n📋 Generated Processes:\n")
    print(df.to_string(index=False))
    print(f"\nAverage Turnaround Time: {avg_tat:.2f}")
    print(f"Average Waiting Time: {avg_wt:.2f}")
    print("\n🕓 Running FCFS Simulation...\n")

    animate_fcfs(processes, schedule, avg_tat, avg_wt, speed)
