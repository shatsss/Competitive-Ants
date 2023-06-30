from typing import Tuple

from players.AbstractPlayer import AbstractPlayer


# This is Bob
class StcPlayer(AbstractPlayer):
    def __init__(self, id):
        super().__init__(id)

    # runs STC algorithm
    def next_move(self, current_location: Tuple[float]):
        return self.run_stc(current_location, self.player_id)
