from mains.heuristic.runner import heuristic_runner
from players.HeuristicFunctions.LCC.LccOpponent import LccOpponent

# runs LccOpponent algorithm
if __name__ == "__main__":
    heuristic_runner(LccOpponent(id=2), "LCC")
