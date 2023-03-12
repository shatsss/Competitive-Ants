from mains.heuristic.runner import heuristic_runner
from players.HeuristicFunctions.LCC.LccOpponent import LccOpponent

if __name__ == "__main__":
    heuristic_runner(LccOpponent(id=2), "LCC")
