from mains.heuristic.runner import heuristic_runner
from players.HeuristicFunctions.LCC.LccBehind import LccBehind

if __name__ == "__main__":
    heuristic_runner(LccBehind(id=2), "LCC")
