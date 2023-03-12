from players.AbstractPlayer import AbstractPlayer


class FccFree(AbstractPlayer):
    def __init__(self, id):
        super().__init__(id)

    def next_move(self, current_location, opponent_current_location, opponent_next_location):
        neighbors = self.get_neighbors_of_sub_cell(current_location)
        for neighbor in neighbors:
            if self.graph.is_cell_not_visited_by_any_player(neighbor):
                return neighbor, None

        return self.run_stc(current_location, self.player_id), None
