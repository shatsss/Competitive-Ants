def update_scores(game_mode, graph, next_locations, player_0_next_location, player_1_next_location, players_list,
                  scores):
    if game_mode == "FCC":
        if player_0_next_location == player_1_next_location and graph.is_cell_not_visited_by_any_player(
                player_0_next_location):
            scores[0] += 0.5
            scores[1] += 0.5
        else:
            if graph.is_cell_not_visited_by_any_player(player_0_next_location):
                scores[0] += 1
            if graph.is_cell_not_visited_by_any_player(player_1_next_location):
                scores[1] += 1
    elif game_mode == "LCC":
        if player_0_next_location == player_1_next_location and graph.is_cell_not_visited_by_any_player(
                player_0_next_location):
            scores[0] += 0.5
            scores[1] += 0.5

        elif player_0_next_location == player_1_next_location and graph.is_visited_last_by_player(
                player_0_next_location,
                players_list[0].player_id):
            scores[0] -= 0.5
            scores[1] += 0.5

        elif player_0_next_location == player_1_next_location and graph.is_visited_last_by_player(
                player_0_next_location,
                players_list[1].player_id):
            scores[1] -= 0.5
            scores[0] += 0.5

        else:
            if graph.is_cell_not_visited_by_any_player(next_locations[0]):
                scores[0] += 1
            elif graph.is_visited_last_by_player(next_locations[0], players_list[1].player_id):
                scores[0] += 1
                scores[1] -= 1
            elif graph.is_visited_last_by_both_players(next_locations[0]):
                scores[0] += 0.5
                scores[1] -= 0.5

            if graph.is_cell_not_visited_by_any_player(next_locations[1]):
                scores[1] += 1
            elif graph.is_visited_last_by_player(next_locations[1], players_list[0].player_id):
                scores[1] += 1
                scores[0] -= 1
            elif graph.is_visited_last_by_both_players(next_locations[1]):
                scores[1] += 0.5
                scores[0] -= 0.5
    else:
        raise Exception("Mode: " + game_mode + " is not supported")
