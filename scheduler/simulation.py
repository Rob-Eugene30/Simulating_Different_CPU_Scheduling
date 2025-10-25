from scheduler.lrjf import lrjf
from scheduler.rr import round_robin
from scheduler.srjf import srjf
from scheduler.fcfs import fcfs

def run_simulation(algo, processes, quantum=None):
    """Dispatch simulation to appropriate algorithm."""
    if algo == "LRJF":
        return lrjf(processes)
    elif algo == "Round Robin":
        return round_robin(processes, quantum)
    elif algo == "SRJF":
        return srjf(processes)
    elif algo == "FCFS":
        return fcfs(processes)
    else:
        raise ValueError(f"Invalid algorithm: {algo}")