from players.AbstractPlayer import AbstractPlayer, distance


class LccBehind(AbstractPlayer):
    def __init__(self, id):
        super().__init__(id)

    # runs STC until the robot meets with the opponent, then, trying to be one step behind of the opponent
    def next_move(self, current_location, opponent_current_location, opponent_next_location):
        distance_to_next_cell = distance(current_location, opponent_current_location)
        if distance_to_next_cell <= 3:
            lst = self.get_neighbors_of_sub_cell(current_location) + [current_location]
            return min(lst, key=lambda x: distance(x, opponent_current_location)), None
        else:
            return self.run_stc(current_location, self.player_id), None
