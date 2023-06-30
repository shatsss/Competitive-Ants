from players.AbstractPlayer import AbstractPlayer


class LccOpponent(AbstractPlayer):
    def __init__(self, id):
        super().__init__(id)

    # goes to cells that visited by the opponent
    def next_move(self, current_location, opponent_current_location, opponent_next_location):
        neighbors = self.get_neighbors_of_sub_cell(current_location)
        for neighbor in neighbors:
            if self.graph.is_visited_last_by_player(neighbor, 1) or self.graph.is_visited_last_by_player(neighbor, 3):
                return neighbor, None
        return self.run_stc(current_location, self.player_id), None
