from players.AbstractPlayer import AbstractPlayer


class FccRAhead(AbstractPlayer):
    def __init__(self, id):
        super().__init__(id)

    # runs reverse-STC until the robot meets with the opponent, then, trying to be one step ahead of the opponent
    def next_move(self, current_location, opponent_current_location, opponent_next_location):
        if current_location == opponent_current_location or opponent_next_location == current_location:
            return self.run_stc(current_location, 1), None
        else:
            return self.run_reverse_stc(current_location, self.player_id), None
