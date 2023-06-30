from mains.heuristic.runner import heuristic_runner
from players.HeuristicFunctions.FCC.FccAhead import FccAhead

# runs FccAhead algorithm

if __name__ == "__main__":
    heuristic_runner(FccAhead(id=2), "FCC")
