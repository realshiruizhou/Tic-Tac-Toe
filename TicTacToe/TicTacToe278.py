from collections import deque
import sys
constraints = [[0, 1, 2], [0, 3, 6], [3, 4, 5], [1, 4, 7], [6, 7, 8], [2, 5, 8], [0, 4, 8], [2, 4, 6]]


def display(state):
    count = 1
    for a in state:
        if count % 3 == 0:
            print(a + " ")
        else:
            print(a + " ", end="", flush=True)
        count += 1


def win(state):
    for a in constraints:
        x = 0
        o = 0
        for b in a:
            if state[b] == "X":
                x += 1
            elif state[b] == "O":
                o += 1
        if x == 3:
            return "X"
        elif o == 3:
            return "O"
    if "." not in state:
        return "D"
    return False


def game_state(state):
    possible = []
    x_count = 0
    o_count = 0
    for c in range(0, 9):
        if state[c] == ".":
            possible.append(c)
        elif state[c] == "X":
            x_count += 1
        elif state[c] == "O":
            o_count += 1
    if x_count == o_count:
        return possible, "X"
    else:
        return possible, "O"


def games():
    fringe = deque()
    fringe.appendleft(".........")
    count = 0
    while len(fringe) != 0:
        v = fringe.pop()
        c = win(v)
        if c:
            count += 1
            continue
        c = game_state(v)
        for a in range(0, len(c[0])):
            child = v[:c[0][a]] + c[1] + v[c[0][a] + 1:]
            fringe.append(child)
    return count


def final_boards():
    fringe = deque()
    fringe.appendleft(".........")
    visited = set()
    final = []
    while len(fringe) != 0:
        v = fringe.pop()
        c = win(v)
        if c:
            if v not in visited:
                visited.add(v)
                final.append(v)
            continue
        c = game_state(v)
        for a in range(0, len(c[0])):
            child = v[:c[0][a]] + c[1] + v[c[0][a] + 1:]
            fringe.append(child)
    return final


def frequency(state):
    count = 0
    for a in state:
        if a == ".":
            count += 1
    return 9 - count


def number():
    ref = {5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}
    for a in final_boards():
        n = frequency(a)
        if n < 9:
            ref[n] = ref[n] + 1
        else:
            g = win(a)
            if g == "X":
                ref[9] = ref[9] + 1
            elif g == "D":
                ref[10] = ref[10] + 1
    return ref


def possible():
    temp = []
    for a in range(0, len(board)):
        if board[a] == ".":
            temp.append(str(a))
    return " ".join(temp)


def empty(state):
    temp = []
    for a in range(0, len(state)):
        if state[a] == ".":
            temp.append(a)
    return temp


def opposite(state):
    if state == "X":
        return "O"
    else:
        return "X"


def minimax(state, current):
    w = win(state)
    if w:
        if w == "O":
            return {-1: 0.0}
        elif w == "X":
            return {-1: 1.0}
        elif w == "D":
            return {-1: .5}
    result = {}
    for a in empty(state):
        new_state = state[:a] + current + state[a + 1:]
        val = minimax(new_state, opposite(current))
        if current == "X":
            boardEval = min(val.values())
        else:
            boardEval = max(val.values())
        result[a] = boardEval
    return result
    

board = sys.argv[1]
if frequency(board) == 0:
    print("Am I playing X or O?")
    playing = input()
    print()
    if playing == "O":
        print("current board:")
        print()
        display(board)
        print()
        print("You can move to any of these spaces: " + possible())
        print("Your choice? ")
        first = int(input())
        board = board[:first] + "X" + board[first + 1:]
        print("current board:")
        print()
        display(board)
        print()
else:
    playing = game_state(board)[1]
player = opposite(playing)
while not win(board):
    possible_move = minimax(board, playing)
    move = -1
    for a in possible_move:
        if possible_move[a] == .5:
            print("Move " + str(a) + " will result in a draw")
        elif playing == "X":
            if possible_move[a] == 1:
                print("Move " + str(a) + " will result in a win")
                move = a
            else:
                print("Move " + str(a) + " will result in a loss")
        else:
            if possible_move[a] == 0:
                print("Move " + str(a) + " will result in a win")
                move = a
            else:
                print("Move " + str(a) + " will result in a loss")
    if move == -1:
        for b in possible_move:
            if possible_move[b] == .5:
                move = b
                break
    if move == -1:
        for c in possible_move:
            move = c
            break
    board = board[:move] + playing + board[move + 1:]
    print()
    print("I choose to move to space " + str(move))
    print()
    print("current board:")
    print()
    display(board)
    print()
    temp = win(board)
    if not temp:
        print("You can move to any of these spaces: " + possible())
        print("Your choice? ")
        p_move = int(input())
        board = board[:p_move] + player + board[p_move + 1:]
        display(board)
        print()
        temp = win(board)
    if temp == player:
        print("You win!")
    elif temp == playing:
        print("I win!")
    elif temp == "D":
        print("Tie!")
# python TicTacToe278.py "........."
