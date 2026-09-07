import random

R, C = 6, 7
AI, HUMAN = "O", "X"
DEPTH = 4
random.seed(15184)
nodes = 0


def board():
    return [["."] * C for _ in range(R)]


def show(b):
    for row in b:
        print(" ".join(row))
    print("1 2 3 4 5 6 7\n")


def valid(b):
    return [c for c in range(C) if b[0][c] == "."]


def move(b, c, p):
    for r in range(R - 1, -1, -1):
        if b[r][c] == ".":
            b[r][c] = p
            return


def win(b, p):
    for r in range(R):
        for c in range(C):
            for dr, dc in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
                if all(
                    0 <= r + dr*i < R and
                    0 <= c + dc*i < C and
                    b[r + dr*i][c + dc*i] == p
                    for i in range(4)
                ):
                    return True
    return False


def score(b):
    s = 0
    for r in range(R):
        for c in range(C):
            if b[r][c] == AI:
                s += 2
            elif b[r][c] == HUMAN:
                s -= 2

    # Center preference
    s += sum(b[r][C // 2] == AI for r in range(R)) * 3
    return s


def minimax(b, depth, maximizing):
    global nodes
    nodes += 1

    if win(b, AI):
        return 100000
    if win(b, HUMAN):
        return -100000

    moves = valid(b)

    if depth == 0 or not moves:
        return score(b)

    if maximizing:
        best = -float("inf")
        for c in moves:
            x = [row[:] for row in b]
            move(x, c, AI)
            best = max(best, minimax(x, depth - 1, False))
        return best

    best = float("inf")
    for c in moves:
        x = [row[:] for row in b]
        move(x, c, HUMAN)
        best = min(best, minimax(x, depth - 1, True))
    return best


def ai_move(b):
    global nodes
    nodes = 0
    best, choices = -float("inf"), []

    for c in valid(b):
        x = [row[:] for row in b]
        move(x, c, AI)
        s = minimax(x, DEPTH - 1, False)

        if s > best:
            best, choices = s, [c]
        elif s == best:
            choices.append(c)

    return random.choice(choices)


def game():
    b = board()

    while True:
        show(b)

        try:
            c = int(input("Your move (1-7): ")) - 1
            if c not in valid(b):
                print("Invalid move!")
                continue
        except ValueError:
            print("Enter a number from 1-7!")
            continue

        move(b, c, HUMAN)

        if win(b, HUMAN):
            show(b)
            print("You win!")
            return

        if not valid(b):
            print("Draw!")
            return

        print("AI thinking...")
        c = ai_move(b)
        move(b, c, AI)
        print(f"AI chose {c + 1} | Nodes: {nodes}")

        if win(b, AI):
            show(b)
            print("AI wins!")
            return


if __name__ == "__main__":
    game()