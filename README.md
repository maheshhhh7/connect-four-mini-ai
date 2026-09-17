# Connect Four Mini AI – Minimax

A Python implementation of the **Connect Four** game with an AI opponent powered by the **Depth-Limited Minimax algorithm**. The AI analyzes possible future moves, evaluates board positions using a heuristic function, and chooses the best move based on Minimax search.

---

## Project Overview

Connect Four is a classic two-player strategy game played on a **6 × 7 board**. The human player uses **X** and the AI uses **O**. Players take turns dropping pieces into columns, and the first player to connect **four pieces** horizontally, vertically, or diagonally wins.

This project demonstrates how **Artificial Intelligence** can be used to play a turn-based game using the Minimax decision-making algorithm.

### Features

* 6 × 7 Connect Four game board.
* Human vs AI gameplay.
* AI implemented using **Depth-Limited Minimax**.
* Static heuristic evaluation function.
* Win detection in all four directions.
* Input validation and draw detection.
* Automated testing using **Pytest**.

---

## Directory Structure

```text
connect-four-mini-ai/
│
├── src/
│   └── connect_four.py          # Main game and AI implementation
│
├── tests/
│   └── test_connect_four.py     # Automated test cases
│
├── docs/
│   ├── report.pdf               # Project report
│   └── screenshots/
│       ├── game_execution.png   # Game execution screenshot
│       └── test_results.png     # Pytest result screenshot
│
├── README.md                    # Project documentation
├── requirements.txt             # Required Python packages
├── .gitignore                   # Git ignored files
└── LICENSE                      # MIT License
```

---

## Problem Statement

The challenge is to build an AI player that can make intelligent decisions in Connect Four instead of selecting random moves.

The AI must:

* Find all valid moves.
* Predict future game states.
* Consider the opponent's best response.
* Evaluate each board position.
* Choose the move with the highest possible score.

Since searching every possible game state is computationally expensive, the AI uses **Depth-Limited Minimax** with a search depth of **4**.

---

## Approach

### Minimax Algorithm

Minimax is a search algorithm used in two-player games where one player tries to maximize the score and the other tries to minimize it.

* **AI (O)** → Maximizing Player
* **Human (X)** → Minimizing Player

### Working Flow

1. Generate all valid moves.
2. Simulate each AI move.
3. Predict the human's response.
4. Continue searching until **depth = 4**.
5. Evaluate the board using a heuristic function.
6. Compare all scores.
7. Choose the move with the highest score.

### Evaluation Function

The AI evaluates non-terminal board positions using the following heuristic:

| Board Position            |   Score |
| ------------------------- | ------: |
| AI piece (`O`)            |      +2 |
| Human piece (`X`)         |      -2 |
| AI piece in center column |      +3 |
| AI win                    | +100000 |
| Human win                 | -100000 |

The center column is given extra preference because it provides more opportunities to create winning combinations.

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/maheshhhh7/connect-four-mini-ai.git
cd connect-four-mini-ai
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the Game

```bash
python src/connect_four.py
```

### 4. Run Tests

```bash
pytest -q
```

---

## Sample Input / Output

### Sample Input

```text
Your move (1-7): 4
```

### Sample Output

```text
AI thinking...
AI chose 4 | Nodes: 2800
```

The AI analyzes possible future moves using Minimax, evaluates the board, and selects the move with the highest score.

### Test Output

```text
3 passed
```

All implemented test cases execute successfully.

---

## Visual Artifacts & Documentation

The **docs** folder contains all supporting materials for the project.

| File                             | Description                                                                             |
| -------------------------------- | --------------------------------------------------------------------------------------- |
| `report.pdf`                     | Project report with problem formulation, approach, complexity, results, and reflection. |
| `screenshots/game_execution.png` | Screenshot of the Connect Four game running with AI move output.                        |
| `screenshots/test_results.png`   | Screenshot showing successful Pytest execution (`3 passed`).                            |

These files provide visual evidence of the project's implementation and testing.

---

## Results

The project was successfully implemented and tested.

* AI successfully plays Connect Four.
* Minimax search is used for AI decision-making.
* Search depth is limited to **4**.
* Board positions are evaluated using a heuristic function.
* The game displays the number of nodes explored during AI search.
* All automated tests passed successfully.

---

## License

This project is licensed under the **MIT License**.

See the `LICENSE` file for complete license information.
