# Board size, number of stones in a row to win
# Tic Tac Toe: 3, 3
# Gomoku: 15, 5
BOARD_SIZE, WIN = 3, 3 # for debugging purposes

# Symbols for printing the board
# White, black, blank, seperator or spacing between symbols
SYMBOLS = '*', 'O', '·', ' '

# Import board position to resume playing
# Board posotion is a list of sublists with each sublist being a row and the last item indicating the turn
IMPORT = None


from copy import deepcopy

def print_board():
    print('\n' + '\n'.join(SYMBOLS[3].join(row) for row in board[:-1]))

def reset_board():
    global board
    board = deepcopy(IMPORT) if IMPORT else [[SYMBOLS[2]] * BOARD_SIZE for _ in range(BOARD_SIZE)] + [True]
    print_board()

reset_board()
print('Enter x y coordinates seperated by a space or nothing to quit. Indexing starts at 1 at the top left.')

while True:
    try:
        move = tuple(map(int, input(f"{SYMBOLS[not board[-1]]} side's move: ").split()))
    except ValueError:
        print('Coordinates must be integers.')
        continue
    if not move:
        print(board)
        break
    if len(move) != 2:
        print('Coordinates must be 2 numbers.')
        continue
    if 0 in move:
        print('Coordinates cannot be 0.')
        continue
    x = move[0] - 1 if move[0] > 0 else move[0] + BOARD_SIZE
    y = move[1] - 1 if move[1] > 0 else move[1] + BOARD_SIZE
    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        print(f'Coordinates must be between -{BOARD_SIZE} and {BOARD_SIZE}.')
        continue
    if board[y][x] != SYMBOLS[2]:
        print(f'{move[0]} {move[1]} already taken by {board[y][x]}.')
        continue

    board[-1] = not board[-1]
    board[y][x] = SYMBOLS[board[-1]]
    print_board()

    consecutive = [0, 0, 0, 0]
    for offset in tuple(range(-WIN + 1, 0)) + tuple(range(1, WIN)):
        consecutive[0] = consecutive[0] + 1 if 0 <= x + offset < BOARD_SIZE and board[y][x + offset] == SYMBOLS[board[-1]] else 0
        consecutive[1] = consecutive[1] + 1 if 0 <= y + offset < BOARD_SIZE and board[y + offset][x] == SYMBOLS[board[-1]] else 0
        consecutive[2] = consecutive[2] + 1 if 0 <= x + offset < BOARD_SIZE and 0 <= y + offset < BOARD_SIZE and board[y + offset][x + offset] == SYMBOLS[board[-1]] else 0
        consecutive[3] = consecutive[3] + 1 if 0 <= x + offset < BOARD_SIZE and 0 <= y - offset < BOARD_SIZE and board[y - offset][x + offset] == SYMBOLS[board[-1]] else 0
        if any(count == WIN - 1 for count in consecutive):
            print(f'{SYMBOLS[board[-1]]} won.')
            reset_board()
            break

    if not any(SYMBOLS[2] in row for row in board[:-1]):
        print('Board filled.')
        reset_board()