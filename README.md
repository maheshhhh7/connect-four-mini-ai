
# Connect Four AI Lab

An interactive Connect Four project demonstrating adversarial search,
explainable AI, constraint-based puzzle generation, and Monte Carlo
simulation through a Streamlit web application.

## Features

- Interactive Connect Four game: human vs AI.
- Minimax search for game-tree evaluation.
- Alpha-Beta pruning with center-first move ordering.
- Explainable AI dashboard showing candidate-column evaluation scores.
- Search statistics, including visited nodes and pruning cutoffs.
- CSP-style puzzle generator for positions with an immediate winning move.
- Monte Carlo agent using random rollouts to estimate candidate move outcomes.
- AI comparison dashboard for Alpha-Beta and Monte Carlo.
- Automated tests for core game logic and AI features.

## Technologies

- Python
- Streamlit
- Pandas
- Pytest

## Project Structure

```text
connect-four-mini-ai/
├── app.py
├── src/
│   ├── connect_four.py
│   ├── alpha_beta.py
│   ├── puzzle_generator.py
│   └── monte_carlo.py
├── tests/
│   ├── test_connect_four.py
│   └── test_ai_features.py
├── docs/
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer recommended.
- pip package manager.

## Installation

Clone the repository:

```bash
git clone https://github.com/maheshhhh7/connect-four-mini-ai.git
cd connect-four-mini-ai
```

Create and activate a virtual environment.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install streamlit pandas pytest
```

## Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

```text
http://localhost:8501
```

## Run Tests

```bash
python -m pytest -v
```

## Algorithms

### Minimax

Explores possible moves up to a fixed depth and evaluates board positions.
The AI uses the evaluation score to choose a move.

### Alpha-Beta Pruning

Optimizes Minimax by pruning branches that cannot affect the final decision.
Center-first move ordering can improve pruning efficiency.

### Explainable AI

Displays heuristic scores for available columns. These scores explain the
search evaluation but are not probabilities or guaranteed winning chances.

### CSP-Style Puzzle Generation

Builds legal board positions, checks basic board constraints, and searches
for positions with an immediate winning move. This is a demonstration of
constraint checking, not a complete general-purpose CSP solver.

### Monte Carlo Simulation

Runs random simulated games after candidate moves and records wins, losses,
draws, and estimated win rates. Results can vary with random rollouts and
are not guarantees of future outcomes.

## Limitations

- Search depth is limited.
- Heuristic evaluation may miss strong moves.
- Monte Carlo results depend on the number and randomness of simulations.
- Puzzle generation targets immediate winning moves rather than all win-in-N
  puzzles.
- The application is an educational prototype, not a perfect Connect Four AI.

## Testing

Run `python -m pytest -v` to execute the automated test suite.

## Future Improvements

- Add configurable search depth.
- Compare performance across multiple board positions.
- Improve puzzle generation for win-in-N challenges.
- Add reproducible Monte Carlo benchmarks.
- Improve visual explanations of tactical decisions.

## License

See the repository's LICENSE file.
