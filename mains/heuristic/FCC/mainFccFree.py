from mains.heuristic.runner import heuristic_runner
from players.HeuristicFunctions.FCC.FccFree import FccFree

# runs FccFree algorithm
if __name__ == "__main__":
    heuristic_runner(FccFree(id=2), "FCC")
