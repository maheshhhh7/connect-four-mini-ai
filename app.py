
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import connect_four as cf
import alpha_beta as ab
import puzzle_generator as pg
import monte_carlo as mc


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Connect Four AI Lab",
    page_icon="🔴",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------- PROFESSIONAL DARK THEME ----------------

st.markdown(
    """
    <style>
    /* Main application background */
    .stApp {
        background:
            radial-gradient(
                ellipse at top left,
                rgba(37, 99, 235, 0.14),
                transparent 45%
            ),
            linear-gradient(135deg, #080d19 0%, #101a2e 100%);
        color: #e5edf9;
    }

    /* Main content spacing */
    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    [data-testid="stHeader"] {
        background: rgba(8, 13, 25, 0.75);
    }

    /* Hero section */
    .hero {
        padding: 28px 30px;
        margin-bottom: 24px;
        border: 1px solid rgba(129, 140, 248, 0.24);
        border-radius: 22px;
        background: linear-gradient(
            120deg,
            rgba(30, 41, 75, 0.96),
            rgba(15, 23, 42, 0.94)
        );
        box-shadow: 0 16px 45px rgba(0, 0, 0, 0.20);
    }

    .hero-title {
        font-size: clamp(30px, 4vw, 46px);
        line-height: 1.15;
        font-weight: 800;
        letter-spacing: -1.4px;
        color: #f8fafc;
        margin: 0 0 12px 0;
    }

    .hero-subtitle {
        color: #a8b8d4;
        font-size: 15px;
        margin: 0;
        line-height: 1.7;
    }

    .hero-tags {
        margin-top: 18px;
        display: flex;
        flex-wrap: wrap;
        gap: 9px;
    }

    .hero-tag {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        color: #dbeafe;
        background: rgba(59, 130, 246, 0.13);
        border: 1px solid rgba(96, 165, 250, 0.24);
        font-size: 12px;
        font-weight: 600;
    }

    /* Headings */
    h1, h2, h3 {
        color: #f8fafc !important;
        letter-spacing: -0.5px;
    }

    h2 {
        margin-top: 14px !important;
    }

    p, label, li {
        color: #d5deed;
    }

    /* Tabs */
    [data-testid="stTabs"] [role="tablist"] {
        gap: 10px;
        border-bottom: 1px solid #29364d;
    }

    [data-testid="stTabs"] button[role="tab"] {
        padding: 12px 17px;
        border-radius: 12px 12px 0 0;
        font-weight: 650;
        transition: background 0.2s ease;
    }

    [data-testid="stTabs"] button[role="tab"]:hover {
        background: rgba(59, 130, 246, 0.12);
    }

    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #93c5fd;
    }

    /* Metric cards */
    [data-testid="stMetric"] {
        padding: 19px;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.20);
        background: linear-gradient(
            145deg,
            rgba(30, 41, 59, 0.92),
            rgba(15, 23, 42, 0.88)
        );
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }

    [data-testid="stMetricLabel"] {
        color: #a8b8d4 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 750;
    }

    /* Buttons */
    .stButton > button {
        min-height: 43px;
        border-radius: 11px;
        border: 1px solid #334766;
        background: linear-gradient(
            135deg,
            #172640,
            #1b2e4c
        );
        color: #eaf2ff;
        font-weight: 650;
        transition: all 0.18s ease;
    }

    .stButton > button:hover {
        border-color: #60a5fa;
        background: linear-gradient(
            135deg,
            #1d3b65,
            #263d68
        );
        color: #ffffff;
        transform: translateY(-1px);
    }

    .stButton > button:focus {
        border-color: #93c5fd;
        color: #ffffff;
        box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.2);
    }

    /* Status messages */
    [data-testid="stAlert"] {
        border-radius: 13px;
        border: 1px solid rgba(148, 163, 184, 0.18);
    }

    /* Expanders */
    [data-testid="stExpander"] {
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 14px;
        background: rgba(15, 23, 42, 0.48);
    }

    /* Data tables */
    [data-testid="stDataFrame"] {
        border: 1px solid #29364d;
        border-radius: 12px;
        overflow: hidden;
    }

    /* Slider */
    [data-testid="stSlider"] {
        padding-top: 10px;
        padding-bottom: 10px;
    }

    /* Dividers */
    hr {
        border-color: rgba(148, 163, 184, 0.18) !important;
    }

    /* Board styling */
    .board-shell {
        padding: 13px;
        border-radius: 18px;
        background: linear-gradient(
            145deg,
            #155eaa,
            #123b78
        );
        border: 1px solid rgba(147, 197, 253, 0.35);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.20);
    }

    .board-cell {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 46px;
        margin: 3px;
        border-radius: 50%;
        background: #0b1930;
        border: 2px solid rgba(191, 219, 254, 0.25);
        font-size: 29px;
        line-height: 1.3;
    }

    .board-red {
        color: #fb4b64;
        text-shadow: 0 2px 12px rgba(251, 75, 100, 0.35);
    }

    .board-yellow {
        color: #facc15;
        text-shadow: 0 2px 12px rgba(250, 204, 21, 0.3);
    }

    .board-empty {
        color: #1d3557;
    }

    /* Footer */
    .app-footer {
        text-align: center;
        color: #8fa2bd;
        font-size: 12px;
        padding: 18px 0 5px 0;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    /* Small screens */
    @media (max-width: 700px) {
        .block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .hero {
            padding: 21px 18px;
            border-radius: 16px;
        }

        .board-cell {
            min-height: 30px;
            margin: 1px;
            font-size: 20px;
        }

        .board-shell {
            padding: 5px;
        }

        [data-testid="stMetric"] {
            padding: 12px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------- SESSION STATE ----------------

defaults = {
    "board": cf.board(),
    "message": "Your turn! Choose a column.",
    "finished": False,
    "history": [],
    "last_search": None,
    "last_ai_column": None,
    "puzzle": None,
    "puzzle_message": "Generate a puzzle to begin.",
    "mc_results": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- SEARCH ANALYSIS ----------------

def evaluate_columns(board):
    scores = {}

    for column in cf.valid(board):
        test = [row[:] for row in board]
        cf.move(test, column, cf.AI)

        if cf.win(test, cf.AI):
            score = 100000
        elif cf.win(test, cf.HUMAN):
            score = -100000
        else:
            score, _ = ab.alpha_beta(
                test,
                cf.DEPTH - 1,
                float("-inf"),
                float("inf"),
                False,
            )

        scores[f"Column {column + 1}"] = score

    return scores


def minimax_node_count(board, depth):
    count = 0

    def search(position, remaining, maximizing):
        nonlocal count
        count += 1

        if cf.win(position, cf.AI):
            return 100000
        if cf.win(position, cf.HUMAN):
            return -100000

        moves = cf.valid(position)
        if remaining == 0 or not moves:
            return cf.score(position)

        best = float("-inf") if maximizing else float("inf")

        for column in moves:
            child = [row[:] for row in position]
            player = cf.AI if maximizing else cf.HUMAN
            cf.move(child, column, player)

            value = search(child, remaining - 1, not maximizing)

            if maximizing:
                best = max(best, value)
            else:
                best = min(best, value)

        return best

    search(board, depth, True)
    return count


# ---------------- GAME ACTIONS ----------------

def reset_game():
    st.session_state.board = cf.board()
    st.session_state.message = "Your turn! Choose a column."
    st.session_state.finished = False
    st.session_state.history = []
    st.session_state.last_search = None
    st.session_state.last_ai_column = None
    st.session_state.mc_results = None


def play(column):
    board = st.session_state.board

    if st.session_state.finished or column not in cf.valid(board):
        return

    cf.move(board, column, cf.HUMAN)
    st.session_state.history.append(
        f"You played column {column + 1}."
    )

    if cf.win(board, cf.HUMAN):
        st.session_state.message = "🎉 You win!"
        st.session_state.finished = True
        return

    if not cf.valid(board):
        st.session_state.message = "🤝 Draw!"
        st.session_state.finished = True
        return

    depth = cf.DEPTH
    minimax_nodes = minimax_node_count(board, depth)
    ai_column, stats = ab.choose_move(board, depth)

    if ai_column is None:
        st.session_state.message = "🤝 No moves remain."
        st.session_state.finished = True
        return

    cf.move(board, ai_column, cf.AI)

    st.session_state.last_ai_column = ai_column
    st.session_state.last_search = {
        "Minimax nodes": minimax_nodes,
        "Alpha-Beta nodes": stats["nodes"],
        "Cutoffs": stats["cutoffs"],
        "Depth": depth,
    }

    st.session_state.history.append(
        f"AI chose column {ai_column + 1}; Alpha-Beta searched "
        f"{stats['nodes']:,} nodes and pruned "
        f"{stats['cutoffs']:,} branches."
    )

    if cf.win(board, cf.AI):
        st.session_state.message = "🤖 AI wins! Start a new game."
        st.session_state.finished = True
    elif not cf.valid(board):
        st.session_state.message = "🤝 Draw!"
        st.session_state.finished = True
    else:
        st.session_state.message = (
            f"AI chose column {ai_column + 1}. Your turn!"
        )


# ---------------- BOARD DISPLAY ----------------

def show_board(board):
    st.markdown('<div class="board-shell">', unsafe_allow_html=True)

    for row in board:
        cells = st.columns(7, gap="small")

        for column, cell in enumerate(cells):
            piece = row[column]

            if piece == cf.HUMAN:
                symbol = "●"
                piece_class = "board-red"
            elif piece == cf.AI:
                symbol = "●"
                piece_class = "board-yellow"
            else:
                symbol = "●"
                piece_class = "board-empty"

            cell.markdown(
                f"""
                <div class="board-cell {piece_class}">
                    {symbol}
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- HERO HEADER ----------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🔴 Connect Four AI Lab</div>
        <p class="hero-subtitle">
            Play against AI, explore search algorithms, solve tactical
            puzzles, and compare decision-making strategies.
        </p>
        <div class="hero-tags">
            <span class="hero-tag">MINIMAX</span>
            <span class="hero-tag">ALPHA-BETA PRUNING</span>
            <span class="hero-tag">PUZZLE MODE</span>
            <span class="hero-tag">MONTE CARLO</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------- APP TABS ----------------

game_tab, puzzle_tab, comparison_tab = st.tabs(
    [
        "🎮 Play Game",
        "🧩 Puzzle Mode",
        "📊 AI Comparison",
    ]
)


# ---------------- GAME TAB ----------------

with game_tab:
    st.info(st.session_state.message)

    st.subheader("Make your move")

    buttons = st.columns(7)

    for column, container in enumerate(buttons):
        with container:
            st.button(
                str(column + 1),
                key=f"play_{column}",
                use_container_width=True,
                disabled=(
                    st.session_state.finished
                    or column not in cf.valid(st.session_state.board)
                ),
                on_click=play,
                args=(column,),
            )

    st.subheader("Game Board")
    show_board(st.session_state.board)

    st.button(
        "🔄 New Game",
        key="reset_game",
        on_click=reset_game,
        use_container_width=True,
    )

    st.divider()
    st.header("🧠 Explainable AI Dashboard")

    if (
        not st.session_state.finished
        and cf.valid(st.session_state.board)
    ):
        scores = evaluate_columns(st.session_state.board)

        if scores:
            st.write(
                "Compare the heuristic evaluation scores of available "
                "moves. These scores are not probabilities."
            )

            score_frame = pd.DataFrame(
                {
                    "Column": list(scores.keys()),
                    "Evaluation score": list(scores.values()),
                }
            ).set_index("Column")

            st.bar_chart(score_frame)

            best_column = max(scores, key=scores.get)
            st.metric("Best evaluated column", best_column)

            with st.expander("View all evaluation scores"):
                for name, score in scores.items():
                    st.write(f"**{name}:** {score}")
    else:
        st.write("Start a new game to see candidate move scores.")

    st.header("⚡ Minimax vs Alpha-Beta")

    if st.session_state.last_search:
        stats = st.session_state.last_search

        first, second, third = st.columns(3)

        first.metric(
            "Minimax nodes",
            f"{stats['Minimax nodes']:,}",
        )
        second.metric(
            "Alpha-Beta nodes",
            f"{stats['Alpha-Beta nodes']:,}",
        )
        third.metric(
            "Pruning cutoffs",
            f"{stats['Cutoffs']:,}",
        )

        if stats["Minimax nodes"]:
            reduction = (
                1
                - stats["Alpha-Beta nodes"]
                / stats["Minimax nodes"]
            ) * 100

            st.metric("Node reduction", f"{reduction:.1f}%")
    else:
        st.write("Play a move to compare both algorithms.")

    with st.expander("📚 Move history"):
        if st.session_state.history:
            for item in reversed(st.session_state.history):
                st.write("•", item)
        else:
            st.write("Your moves and AI decisions will appear here.")


# ---------------- PUZZLE TAB ----------------

with puzzle_tab:
    st.header("🧩 Find the Winning Move")

    st.write(
        "Yellow is the AI piece. Find a column where yellow can "
        "connect four immediately."
    )

    if st.button(
        "🎲 Generate New Puzzle",
        key="generate_puzzle",
        use_container_width=True,
    ):
        with st.spinner("Generating puzzle..."):
            st.session_state.puzzle = pg.make_winning_puzzle()

            st.session_state.puzzle_message = (
                "Puzzle ready!"
                if st.session_state.puzzle
                else "No puzzle found. Please try again."
            )

    st.info(st.session_state.puzzle_message)

    puzzle = st.session_state.puzzle

    if puzzle:
        show_board(puzzle["board"])

        st.write("Select the winning column:")

        choices = st.columns(7)

        for column, container in enumerate(choices):
            with container:
                if st.button(
                    str(column + 1),
                    key=f"puzzle_choice_{column}",
                    use_container_width=True,
                ):
                    if column in puzzle["winning_columns"]:
                        st.success(
                            f"Correct! Column {column + 1} wins."
                        )
                    else:
                        st.error(
                            "Not an immediate winning move. Try again!"
                        )

        if st.button(
            "💡 Reveal Validated Solution",
            key="reveal_solution",
        ):
            st.success(
                "Validated winning column: "
                f"{puzzle['validated_column'] + 1}"
            )

            st.write(
                "Search nodes:",
                puzzle["search_stats"]["nodes"],
            )
            st.write(
                "Pruning cutoffs:",
                puzzle["search_stats"]["cutoffs"],
            )

    st.caption(
        "This generator checks legal board constraints and immediate "
        "wins. It is a CSP-style demonstration, not a general "
        "win-in-N solver."
    )


# ---------------- MONTE CARLO COMPARISON TAB ----------------

with comparison_tab:
    st.header("📊 Alpha-Beta vs Monte Carlo")

    st.write(
        "Compare a search-based AI with an agent that estimates "
        "move quality using random game simulations."
    )

    simulations = st.slider(
        "Monte Carlo simulations per column",
        min_value=10,
        max_value=200,
        value=50,
        step=10,
    )

    if st.button(
        "Run AI Comparison",
        key="run_comparison",
        use_container_width=True,
    ):
        board = st.session_state.board

        if st.session_state.finished or not cf.valid(board):
            st.warning(
                "Start a new game before running the comparison."
            )
        else:
            with st.spinner("Running Monte Carlo simulations..."):
                alpha_column, alpha_stats = ab.choose_move(
                    board,
                    depth=cf.DEPTH,
                )

                mc_column, mc_stats = mc.choose_move(
                    board,
                    simulations=simulations,
                )

                st.session_state.mc_results = {
                    "alpha_column": alpha_column,
                    "alpha_nodes": alpha_stats["nodes"],
                    "mc_column": mc_column,
                    "mc_stats": mc_stats,
                    "simulations": simulations,
                }

    results = st.session_state.mc_results

    if results:
        left, right = st.columns(2)

        with left:
            st.metric(
                "Alpha-Beta choice",
                (
                    f"Column {results['alpha_column'] + 1}"
                    if results["alpha_column"] is not None
                    else "No move"
                ),
            )

            st.metric(
                "Alpha-Beta nodes",
                f"{results['alpha_nodes']:,}",
            )

        with right:
            st.metric(
                "Monte Carlo choice",
                (
                    f"Column {results['mc_column'] + 1}"
                    if results["mc_column"] is not None
                    else "No move"
                ),
            )

            st.metric(
                "Simulations per column",
                results["simulations"],
            )

        mc_rows = []

        for column, data in results["mc_stats"]["columns"].items():
            mc_rows.append(
                {
                    "Column": column + 1,
                    "Win rate": data["win_rate"],
                    "Wins": data["wins"],
                    "Losses": data["losses"],
                    "Draws": data["draws"],
                }
            )

        if mc_rows:
            frame = pd.DataFrame(mc_rows).set_index("Column")

            st.subheader("Monte Carlo results")
            st.bar_chart(frame[["Win rate"]])
            st.dataframe(frame, use_container_width=True)

        st.caption(
            "Monte Carlo win rates are estimates from random rollouts. "
            "They are not guaranteed outcomes and may vary between runs."
        )
    else:
        st.write(
            "Run the comparison to see both AI choices and "
            "simulation results."
        )


# ---------------- RESPONSIBLE AI ----------------

st.divider()

with st.expander("⚖️ Responsible AI and limitations"):
    st.write(
        "This is an educational prototype. Alpha-Beta uses "
        "limited-depth search, while Monte Carlo uses random rollouts. "
        "Neither method guarantees optimal play in every position. "
        "Simulation results depend on the chosen settings."
    )

st.markdown(
    """
    <div class="app-footer">
        CONNECT FOUR AI LAB · Educational AI project
    </div>
    """,
    unsafe_allow_html=True,
)
