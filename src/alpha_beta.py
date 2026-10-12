
import connect_four as cf


def ordered_moves(board):
    """Try center columns first to improve pruning."""
    return sorted(cf.valid(board), key=lambda c: abs(c - cf.C // 2))


def alpha_beta(board, depth, alpha=float("-inf"), beta=float("inf"),
               maximizing=True, stats=None):
    """
    Minimax search with Alpha-Beta pruning.
    Returns (score, best_column).
    """
    if stats is None:
        stats = {"nodes": 0, "cutoffs": 0}

    stats["nodes"] += 1

    if cf.win(board, cf.AI):
        return 100000 + depth, None

    if cf.win(board, cf.HUMAN):
        return -100000 - depth, None

    moves = ordered_moves(board)

    if depth == 0 or not moves:
        return cf.score(board), None

    best_column = None

    if maximizing:
        best_score = float("-inf")

        for column in moves:
            child = [row[:] for row in board]
            cf.move(child, column, cf.AI)

            score, _ = alpha_beta(
                child, depth - 1, alpha, beta, False, stats
            )

            if score > best_score:
                best_score = score
                best_column = column

            alpha = max(alpha, best_score)

            if alpha >= beta:
                stats["cutoffs"] += 1
                break

        return best_score, best_column

    best_score = float("inf")

    for column in moves:
        child = [row[:] for row in board]
        cf.move(child, column, cf.HUMAN)

        score, _ = alpha_beta(
            child, depth - 1, alpha, beta, True, stats
        )

        if score < best_score:
            best_score = score
            best_column = column

        beta = min(beta, best_score)

        if alpha >= beta:
            stats["cutoffs"] += 1
            break

    return best_score, best_column


def choose_move(board, depth=4):
    """Return the best column and search statistics."""
    stats = {"nodes": 0, "cutoffs": 0}

    _, column = alpha_beta(
        board,
        depth,
        float("-inf"),
        float("inf"),
        True,
        stats,
    )

    return column, stats
