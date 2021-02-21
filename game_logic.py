board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]


def print_game_board(game_board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -  ")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(game_board[i][j])
            else:
                print(str(game_board[i][j]) + " ", end="")


def find_empty_place(game_board):
    for i in range(9):
        for j in range(9):
            if game_board[i][j] == 0:
                return i, j
    return False


def check_row(game_board, num, row):
    for j in range(9):
        if game_board[row][j] == num:
            return False
    return True


def check_col(game_board, num, col):
    for i in range(9):
        if game_board[i][col] == num:
            return False
    return True


def check_square(game_board, num, row, col):
    box_row = row // 3
    box_col = col // 3
    for i in range(box_row * 3, box_row * 3 + 3):
        for j in range(box_col * 3, box_col * 3 + 3):
            if game_board[i][j] == num:
                return False
    return True


def is_board_valid(game_board, num, row, col):
    if check_col(game_board, num, col) and check_row(game_board, num, row) and check_square(game_board, num, row, col):
        return True
    return False


def solve_board(game_board):
    curr_pos = find_empty_place(game_board)
    if not curr_pos:
        return True
    else:
        row, col = curr_pos

    for i in range(1, 10):
        if is_board_valid(game_board, i, row, col):
            game_board[row][col] = i
            if solve_board(game_board):
                return True
    game_board[row][col] = 0
    return False

print_game_board(board)
print(""
      ""
      ""
      ""
      ""
      ""
      "")
solve_board(board)
print_game_board(board)








