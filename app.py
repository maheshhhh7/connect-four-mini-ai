
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

st.set_page_config(
    page_title="Connect Four AI Lab",
    page_icon="🔴",
    layout="wide",
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
    st.session_state.history.append(f"You played column {column + 1}.")

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
        f"{stats['nodes']:,} nodes and pruned {stats['cutoffs']:,} branches."
    )

    if cf.win(board, cf.AI):
        st.session_state.message = "🤖 AI wins! Start a new game."
        st.session_state.finished = True
    elif not cf.valid(board):
        st.session_state.message = "🤝 Draw!"
        st.session_state.finished = True
    else:
        st.session_state.message = f"AI chose column {ai_column + 1}. Your turn!"


def show_board(board):
    for row in board:
        cells = st.columns(7)
        for column, cell in enumerate(cells):
            piece = row[column]
            symbol = "🔴" if piece == cf.HUMAN else "🟡" if piece == cf.AI else "⚪"
            cell.markdown(
                f"<div style='text-align:center;font-size:27px;"
                f"background:#1769aa;border-radius:6px;padding:6px 0;"
                f"margin-bottom:3px'>{symbol}</div>",
                unsafe_allow_html=True,
            )


# ---------------- APP TABS ----------------

st.title("🔴 Connect Four AI Lab")
st.caption("Game · Explainable AI · CSP Puzzle · Monte Carlo")

game_tab, puzzle_tab, comparison_tab = st.tabs(
    ["🎮 Play Game", "🧩 Puzzle Mode", "📊 AI Comparison"]
)

# ---------------- GAME TAB ----------------

with game_tab:
    st.info(st.session_state.message)

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

    if not st.session_state.finished and cf.valid(st.session_state.board):
        scores = evaluate_columns(st.session_state.board)

        if scores:
            st.write(
                "Alpha-Beta evaluation scores for available moves. "
                "These are heuristic values, not probabilities."
            )
            st.bar_chart(pd.DataFrame({"Evaluation score": scores}))
            st.metric("Best evaluated column", max(scores, key=scores.get))

            for name, score in scores.items():
                st.write(f"**{name}:** {score}")
    else:
        st.write("Start a new game to see candidate move scores.")

    st.header("⚡ Minimax vs Alpha-Beta")

    if st.session_state.last_search:
        stats = st.session_state.last_search
        a, b, c = st.columns(3)
        a.metric("Minimax nodes", f"{stats['Minimax nodes']:,}")
        b.metric("Alpha-Beta nodes", f"{stats['Alpha-Beta nodes']:,}")
        c.metric("Pruning cutoffs", f"{stats['Cutoffs']:,}")

        if stats["Minimax nodes"]:
            reduction = (
                1 - stats["Alpha-Beta nodes"] / stats["Minimax nodes"]
            ) * 100
            st.metric("Node reduction", f"{reduction:.1f}%")
    else:
        st.write("Play a move to compare both algorithms.")

    with st.expander("📚 Move history"):
        for item in reversed(st.session_state.history):
            st.write("•", item)

# ---------------- PUZZLE TAB ----------------

with puzzle_tab:
    st.header("🧩 Find the Winning Move")
    st.write("Find the column where yellow can connect four immediately.")

    if st.button("🎲 Generate New Puzzle", use_container_width=True):
        with st.spinner("Generating puzzle..."):
            st.session_state.puzzle = pg.make_winning_puzzle()
            st.session_state.puzzle_message = (
                "Puzzle ready!" if st.session_state.puzzle
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
                        st.success(f"Correct! Column {column + 1} wins.")
                    else:
                        st.error("Not an immediate winning move. Try again!")

        if st.button("💡 Reveal Validated Solution"):
            st.success(
                f"Validated winning column: "
                f"{puzzle['validated_column'] + 1}"
            )
            st.write("Search nodes:", puzzle["search_stats"]["nodes"])
            st.write("Pruning cutoffs:", puzzle["search_stats"]["cutoffs"])

    st.caption(
        "This generator checks legal board constraints and immediate wins. "
        "It is a CSP-style demonstration, not a general win-in-N solver."
    )


# ---------------- MONTE CARLO COMPARISON TAB ----------------

with comparison_tab:
    st.header("📊 Alpha-Beta vs Monte Carlo")
    st.write(
        "Compare the search-based AI with an agent that estimates move "
        "quality through random game simulations."
    )

    simulations = st.slider(
        "Monte Carlo simulations per column",
        min_value=10,
        max_value=200,
        value=50,
        step=10,
    )

    if st.button("Run AI Comparison", use_container_width=True):
        board = st.session_state.board

        if st.session_state.finished or not cf.valid(board):
            st.warning("Start a new game before running the comparison.")
        else:
            with st.spinner("Running Monte Carlo simulations..."):
                alpha_column, alpha_stats = ab.choose_move(
                    board, depth=cf.DEPTH
                )
                mc_column, mc_stats = mc.choose_move(
                    board, simulations=simulations
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
                f"Column {results['alpha_column'] + 1}"
                if results["alpha_column"] is not None else "No move",
            )
            st.metric("Alpha-Beta nodes", f"{results['alpha_nodes']:,}")

        with right:
            st.metric(
                "Monte Carlo choice",
                f"Column {results['mc_column'] + 1}"
                if results["mc_column"] is not None else "No move",
            )
            st.metric(
                "Simulations per column",
                results["simulations"],
            )

        mc_rows = []
        for column, data in results["mc_stats"]["columns"].items():
            mc_rows.append({
                "Column": column + 1,
                "Win rate": data["win_rate"],
                "Wins": data["wins"],
                "Losses": data["losses"],
                "Draws": data["draws"],
            })

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
        st.write("Run the comparison to see both AI choices and simulation results.")


st.divider()
st.subheader("⚖️ Responsible AI")
st.write(
    "This is an educational prototype. Alpha-Beta uses limited-depth search; "
    "Monte Carlo uses random rollouts. Neither method guarantees optimal play "
    "in every position. Simulation results depend on the chosen settings."
)
