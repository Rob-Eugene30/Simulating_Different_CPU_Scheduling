def lrjf(processes):
    """Longest Remaining Job First (Preemptive)"""
    time = 0
    completed = []
    gantt = []
    ready = []
    processes = sorted(processes, key=lambda x: x['arrival'])
    remaining = {p['pid']: p['burst'] for p in processes}
    last_pid = None

    while processes or ready:
        while processes and processes[0]['arrival'] <= time:
            ready.append(processes.pop(0))
        if ready:
            ready.sort(key=lambda x: remaining[x['pid']], reverse=True)
            p = ready[0]
            remaining[p['pid']] -= 1
            if p['pid'] != last_pid:
                gantt.append((p['pid'], time, time + 1))
            else:
                gantt[-1] = (p['pid'], gantt[-1][1], time + 1)
            last_pid = p['pid']
            time += 1
            if remaining[p['pid']] == 0:
                p['completion'] = time
                p['turnaround'] = time - p['arrival']
                p['waiting'] = p['turnaround'] - p['burst']
                completed.append(p)
                ready.remove(p)
        else:
            time += 1
            last_pid = None
    return completed, gantt
