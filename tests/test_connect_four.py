from src.connect_four import *


def test_board():
    b = board()

    assert len(b) == 6
    assert len(b[0]) == 7


def test_win():
    b = board()

    for c in range(4):
        move(b, c, HUMAN)

    assert win(b, HUMAN)


def test_ai():
    b = board()

    move(b, 3, HUMAN)

    c = ai_move(b)

    assert c in valid(b)
