#Round Robin (RR) Scheduling Algorithm 
# Sinimulan ko Myrr hehe cuz eto may quantum parameter >:(

def round_robin(processes, quantum):
    queue = []
    gantt = []
    time = 0
    processes = sorted(processes, key=lambda x: x['arrival'])
    remaining = {p['pid']: p['burst'] for p in processes}
    completed = {}

    while processes or queue:
        while processes and processes[0]['arrival'] <= time:
            queue.append(processes.pop(0))
        if queue:
            p = queue.pop(0)
            exec_time = min(quantum, remaining[p['pid']])
            start = time
            time += exec_time
            end = time
            remaining[p['pid']] -= exec_time
            gantt.append((p['pid'], start, end))
            if remaining[p['pid']] == 0:
                p['completion'] = time
                p['turnaround'] = p['completion'] - p['arrival']
                p['waiting'] = p['turnaround'] - p['burst']
                completed[p['pid']] = p
            else:
                while processes and processes[0]['arrival'] <= time:
                    queue.append(processes.pop(0))
                queue.append(p)
        else:
            time += 1
    return list(completed.values()), gantt

