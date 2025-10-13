from scheduler.lrjf import lrjf
from scheduler.rr import round_robin

def run_simulation(algo, processes, quantum=None):
    """Dispatch simulation to appropriate algorithm."""
    if algo == "LRJF":
        return lrjf(processes)
    elif algo == "Round Robin":
        return round_robin(processes, quantum)
    else:
        raise ValueError(f"Invalid algorithm: {algo}")
