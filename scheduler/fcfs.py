def fcfs(processes):
    """First-Come, First-Serve (Non-Preemptive)"""
    
    processes = sorted(processes, key=lambda x: (x['arrival'], x['pid']))
    
    time = 0
    completed = []
    gantt = []

    for p in processes:
        if time < p['arrival']:
            gantt.append(("Idle", time, p['arrival']))
            time = p['arrival']

        start_time = time
        finish_time = time + p['burst']

        p['completion'] = finish_time
        p['turnaround'] = finish_time - p['arrival']
        p['waiting'] = p['turnaround'] - p['burst']

        completed.append(p)
        gantt.append((p['pid'], start_time, finish_time))

        time = finish_time

    return completed, gantt
