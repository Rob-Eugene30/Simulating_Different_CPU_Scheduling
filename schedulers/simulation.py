#This is where the mapping(?) happens 

from schedulers.lrjf import lrjf
from schedulers.rr import round_robin

def run_simulation(algo, processes, quantum=None):
    if algo == "LRJF":
        return lrjf(processes)
    elif algo == "Round Robin":
        return round_robin(processes, quantum)
    else:
        raise ValueError("Invalid algorithm selected.")
