
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import connect_four as cf
import alpha_beta
import puzzle_generator
import monte_carlo


def test_alpha_beta_returns_legal_move():
    board = cf.board()

    column, stats = alpha_beta.choose_move(board, depth=3)

    assert column in cf.valid(board)
    assert stats["nodes"] > 0
    assert stats["cutoffs"] >= 0


def test_alpha_beta_takes_immediate_win():
    board = cf.board()

    # Three AI discs along the bottom; column 4 completes four.
    for column in (0, 1, 2):
        cf.move(board, column, cf.AI)

    column, _ = alpha_beta.choose_move(board, depth=3)

    assert column == 3


def test_puzzle_board_constraints():
    board = cf.board()

    valid, message = puzzle_generator.validate_position(board)

    assert valid is True
    assert "passes" in message


def test_puzzle_generator_returns_validated_puzzle():
    puzzle = puzzle_generator.make_winning_puzzle()

    assert puzzle is not None
    assert puzzle["validated_column"] in puzzle["winning_columns"]
    assert puzzle["search_stats"]["nodes"] > 0


def test_monte_carlo_returns_legal_move():
    board = cf.board()

    column, stats = monte_carlo.choose_move(
        board, simulations=5, seed=42
    )

    assert column in cf.valid(board)
    assert len(stats["columns"]) == 7


def test_monte_carlo_rejects_zero_simulations():
    with pytest.raises(ValueError):
        monte_carlo.choose_move(cf.board(), simulations=0)


def test_monte_carlo_returns_no_move_for_full_board():
    board = [["X"] * cf.C for _ in range(cf.R)]

    column, stats = monte_carlo.choose_move(board, simulations=5)

    assert column is None
    assert stats["columns"] == {}
