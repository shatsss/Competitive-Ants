from players.AbstractPlayer import AbstractPlayer


class FccAhead(AbstractPlayer):
    def __init__(self, id):
        super().__init__(id)

    # runs STC until the robot meets with the opponent, then, trying to be one step ahead of the opponent
    def next_move(self, current_location, opponent_current_location, opponent_next_location):
        if current_location == opponent_current_location or opponent_next_location == current_location:
            id_to_look = 1
        else:
            id_to_look = self.player_id  # 2
        return self.run_stc(current_location, id_to_look), None
