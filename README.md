# Connect Four Mini AI

A Connect Four game where a human player competes against an AI opponent using the **Depth-Limited Minimax algorithm** with a **static evaluation function**.

---

## 1. Problem Statement

The objective is to develop a Connect Four AI agent that can play against a human player.

The game is played on a **6 × 7 board**. Players take turns dropping their pieces into one of the seven columns. The first player to connect four pieces horizontally, vertically, or diagonally wins the game.

The AI must select its moves using **depth-limited Minimax** and evaluate non-terminal game states using a static heuristic function.

---

## 2. Objectives

- Implement a playable 6 × 7 Connect Four game.
- Implement the Minimax algorithm.
- Use a fixed search depth to limit the game-tree search.
- Implement a static evaluation function for non-terminal boards.
- Allow a human player to play against the AI.
- Detect wins, draws, and invalid moves.
- Display the number of nodes searched by the AI.

---

## 3. Approach

The project uses the **Minimax algorithm** to make decisions.

For every possible AI move, the program creates a copy of the board and searches possible future moves.

The AI acts as the **maximizing player**, while the human player is treated as the **minimizing player**.

The search continues until:

1. A player wins.
2. The board becomes full.
3. The selected search depth reaches zero.

When the depth limit is reached without a winner, the board is evaluated using the static evaluation function.

---

## 4. Minimax Algorithm

The Minimax algorithm considers possible future game states.

### Maximizing Step

The AI tries to choose the move with the highest evaluation score.

```text
Best Score = Maximum of possible scores
