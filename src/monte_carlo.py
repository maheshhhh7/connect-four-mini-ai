
import random
import connect_four as cf


def rollout(board, player_to_move):
    """
    Play a random game until someone wins or the board is full.
    Returns 1 for an AI win, -1 for a human win, and 0 for a draw.
    """
    position = [row[:] for row in board]
    player = player_to_move

    while True:
        if cf.win(position, cf.AI):
            return 1

        if cf.win(position, cf.HUMAN):
            return -1

        moves = cf.valid(position)

        if not moves:
            return 0

        column = random.choice(moves)
        cf.move(position, column, player)

        if cf.win(position, player):
            return 1 if player == cf.AI else -1

        player = cf.HUMAN if player == cf.AI else cf.AI


def choose_move(board, simulations=100, seed=None):
    """
    Estimate each legal AI move using random Monte Carlo rollouts.

    Returns:
        best_column: selected column index, or None if no moves remain
        stats: rollout counts and estimated outcomes for each column
    """
    if simulations < 1:
        raise ValueError("simulations must be at least 1")

    rng = random.Random(seed)
    legal_moves = cf.valid(board)

    if not legal_moves:
        return None, {"simulations": simulations, "columns": {}}

    results = {}

    for column in legal_moves:
        candidate = [row[:] for row in board]
        cf.move(candidate, column, cf.AI)

        if cf.win(candidate, cf.AI):
            results[column] = {
                "wins": simulations,
                "losses": 0,
                "draws": 0,
                "win_rate": 1.0,
            }
            continue

        wins = 0
        losses = 0
        draws = 0

        for _ in range(simulations):
            outcome = rollout(candidate, cf.HUMAN)

            if outcome == 1:
                wins += 1
            elif outcome == -1:
                losses += 1
            else:
                draws += 1

        results[column] = {
            "wins": wins,
            "losses": losses,
            "draws": draws,
            "win_rate": wins / simulations,
        }

    # Prefer the highest simulated AI win rate.
    # Randomly break ties for variety.
    best_rate = max(item["win_rate"] for item in results.values())
    best_columns = [
        column for column, item in results.items()
        if item["win_rate"] == best_rate
    ]

    best_column = rng.choice(best_columns)

    stats = {
        "simulations_per_column": simulations,
        "columns": results,
    }

    return best_column, stats
