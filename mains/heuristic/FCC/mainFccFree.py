from mains.heuristic.runner import heuristic_runner
from players.HeuristicFunctions.FCC.FccFree import FccFree

if __name__ == "__main__":
    heuristic_runner(FccFree(id=2), "FCC")
