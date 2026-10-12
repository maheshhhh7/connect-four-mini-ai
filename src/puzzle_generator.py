
import random
import sys
from pathlib import Path

# Allow this module to import the existing game and search algorithms.
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import connect_four as cf
import alpha_beta as ab


def copy_board(board):
    return [row[:] for row in board]


def has_winning_move(board, player):
    """Return legal columns that win immediately for the given player."""
    winning_columns = []

    for column in cf.valid(board):
        candidate = copy_board(board)
        cf.move(candidate, column, player)

        if cf.win(candidate, player):
            winning_columns.append(column)

    return winning_columns


def validate_position(board):
    """
    Check basic Connect Four position constraints.

    This validates board dimensions, cell values, gravity, and piece counts.
    """
    if len(board) != cf.R or any(len(row) != cf.C for row in board):
        return False, "Board must have 6 rows and 7 columns."

    allowed = {".", cf.AI, cf.HUMAN}
    if any(cell not in allowed for row in board for cell in row):
        return False, "Board contains an unknown cell value."

    # A piece cannot float above an empty cell.
    for column in range(cf.C):
        found_empty_below = False

        for row in range(cf.R - 1, -1, -1):
            if board[row][column] == ".":
                found_empty_below = True
            elif found_empty_below:
                return False, "A disc is floating above an empty space."

    ai_count = sum(cell == cf.AI for row in board for cell in row)
    human_count = sum(cell == cf.HUMAN for row in board for cell in row)

    if human_count not in (ai_count, ai_count + 1):
        return False, "Piece counts are inconsistent with human-first play."

    return True, "Position passes basic board constraints."


def make_winning_puzzle(max_attempts=300):
    """
    Generate a puzzle where the AI has an immediate winning move.

    Backtracking places legal moves from an empty board. Candidate positions
    are accepted only when they satisfy basic constraints and contain a win
    for the AI on its next move.
    """
    for _ in range(max_attempts):
        board = cf.board()
        history = []

        # Build a random legal sequence without allowing earlier wins.
        number_of_moves = random.randint(6, 20)

        for turn in range(number_of_moves):
            legal = cf.valid(board)
            if not legal:
                break

            # Alternating moves: human starts.
            player = cf.HUMAN if turn % 2 == 0 else cf.AI
            random.shuffle(legal)

            placed = False
            for column in legal:
                candidate = copy_board(board)
                cf.move(candidate, column, player)

                if cf.win(candidate, player):
                    continue

                # Constraint: the generated prefix must not already be terminal.
                board = candidate
                history.append((column, player))
                placed = True
                break

            if not placed:
                break

        # AI must be the side to move in a human-first game.
        ai_count = sum(cell == cf.AI for row in board for cell in row)
        human_count = sum(cell == cf.HUMAN for row in board for cell in row)

        if human_count != ai_count:
            continue

        valid, _ = validate_position(board)
        if not valid:
            continue

        winning_columns = has_winning_move(board, cf.AI)
        if not winning_columns:
            continue

        # Validate a winning move with the existing search algorithm.
        chosen_column, stats = ab.choose_move(board, depth=4)

        if chosen_column is not None:
            candidate = copy_board(board)
            cf.move(candidate, chosen_column, cf.AI)

            if cf.win(candidate, cf.AI):
                return {
                    "board": board,
                    "winning_columns": winning_columns,
                    "validated_column": chosen_column,
                    "search_stats": stats,
                    "description": "Find a move that wins immediately.",
                }

    return None


def board_to_text(board):
    """Return a readable text representation of a board."""
    lines = [" ".join(row) for row in board]
    lines.append("1 2 3 4 5 6 7")
    return "\n".join(lines)
