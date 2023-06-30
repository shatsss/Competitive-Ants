# This class calculates the updated scores according to the last action of each player and game


def update_scores(game_mode, graph, next_locations, player_0_next_location, player_1_next_location, players_list,
                  scores):
    # calculate scores for the FCC game
    if game_mode == "FCC":
        # both players entered to a new cell at the same time
        if player_0_next_location == player_1_next_location and graph.is_cell_not_visited_by_any_player(
                player_0_next_location):
            scores[0] += 0.5
            scores[1] += 0.5
        else:
            # first player entered to a new cell
            if graph.is_cell_not_visited_by_any_player(player_0_next_location):
                scores[0] += 1
            # second player entered to a new cell
            if graph.is_cell_not_visited_by_any_player(player_1_next_location):
                scores[1] += 1

    # calculate scores for the LCC game
    elif game_mode == "LCC":
        # both players entered to a new cell at the same time
        if player_0_next_location == player_1_next_location and graph.is_cell_not_visited_by_any_player(
                player_0_next_location):
            scores[0] += 0.5
            scores[1] += 0.5
        # both players entered to a cell of first player at the same time
        elif player_0_next_location == player_1_next_location and graph.is_visited_last_by_player(
                player_0_next_location,
                players_list[0].player_id):
            scores[0] -= 0.5
            scores[1] += 0.5
        # both players entered to a cell of second player at the same time
        elif player_0_next_location == player_1_next_location and graph.is_visited_last_by_player(
                player_0_next_location,
                players_list[1].player_id):
            scores[1] -= 0.5
            scores[0] += 0.5

        else:
            # first player visited unvisited cell
            if graph.is_cell_not_visited_by_any_player(next_locations[0]):
                scores[0] += 1
            # first player visited second player cell
            elif graph.is_visited_last_by_player(next_locations[0], players_list[1].player_id):
                scores[0] += 1
                scores[1] -= 1
            # first player visited cell that visited last by both players
            elif graph.is_visited_last_by_both_players(next_locations[0]):
                scores[0] += 0.5
                scores[1] -= 0.5

            # second player visited unvisited cell
            if graph.is_cell_not_visited_by_any_player(next_locations[1]):
                scores[1] += 1
            # second player visited first player cell
            elif graph.is_visited_last_by_player(next_locations[1], players_list[0].player_id):
                scores[1] += 1
                scores[0] -= 1
            # second player visited cell that visited last by both players
            elif graph.is_visited_last_by_both_players(next_locations[1]):
                scores[1] += 0.5
                scores[0] -= 0.5
    else:
        raise Exception("Mode: " + game_mode + " is not supported")
