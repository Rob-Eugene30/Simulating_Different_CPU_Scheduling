def sjf(processes):
    """Shortest Job First (Non-Preemptive)"""
    
    procs = sorted(processes, key=lambda x: (x['arrival'], x['pid']))

    time = 0
    completed = []
    gantt = []

    remaining = procs[:]  

    while remaining:
        ready = [p for p in remaining if p['arrival'] <= time]

        if not ready:
            next_arrival = min(p['arrival'] for p in remaining)
            if time < next_arrival:
                gantt.append(("Idle", time, next_arrival))
                time = next_arrival
            continue

        ready.sort(key=lambda p: (p['burst'], p['arrival'], p['pid']))
        p = ready[0]

        start_time = time
        finish_time = time + p['burst']

        p['completion'] = finish_time
        p['turnaround'] = finish_time - p['arrival']
        p['waiting'] = p['turnaround'] - p['burst']

        completed.append(p)
        gantt.append((p['pid'], start_time, finish_time))

        time = finish_time
        remaining.remove(p)

    return completed, gantt