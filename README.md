# Connect Four Mini AI – Minimax

A simple Connect Four game where a human player plays against an AI opponent.

The AI uses the **Depth-Limited Minimax Algorithm** with a **Static Evaluation Function** to select its moves.

---

## Project Overview

Connect Four is a two-player game played on a **6 × 7 board**.

Players take turns dropping pieces into columns. The first player to connect four pieces horizontally, vertically, or diagonally wins the game.

In this project:

- `X` represents the Human player.
- `O` represents the AI player.
- `.` represents an empty position.

The AI uses Minimax to look ahead at possible future moves and select a move with the best evaluation.

---

## Objectives

- Implement a playable Connect Four game.
- Implement the Depth-Limited Minimax algorithm.
- Use a static evaluation function.
- Allow a human to play against the AI.
- Detect horizontal, vertical, and diagonal wins.
- Detect draw conditions.
- Handle invalid user input.
- Count the number of nodes explored by the AI.

---

## Technologies Used

- Python 3
- Minimax Algorithm
- Static Evaluation Function
- Git and GitHub

---

## Algorithm

### Depth-Limited Minimax

The AI uses the Minimax algorithm to evaluate possible future game states.

The AI is the **maximizing player**, while the Human is treated as the **minimizing player**.

The search continues until:

1. The AI wins.
2. The Human wins.
3. There are no available moves.
4. The selected search depth reaches zero.

When the depth limit is reached, the static evaluation function is used.

---

## Search Depth

The project uses a fixed search depth of **4**.

```python
DEPTH = 4
