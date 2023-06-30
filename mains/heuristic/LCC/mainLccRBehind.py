from mains.heuristic.runner import heuristic_runner
from players.HeuristicFunctions.LCC.LccRBehind import LccRBehind

# runs LccRBehind algorithm
if __name__ == "__main__":
    heuristic_runner(LccRBehind(id=2), "LCC")
