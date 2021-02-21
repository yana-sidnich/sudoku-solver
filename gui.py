import pygame
import sys
import copy
import game_logic


"""
Cell class.
Represents a single cell on the sudoku board
"""


class Cell:
    def __init__(self, final_value, temp_value, indexes):
        self.final_value = final_value
        self.temp_value = temp_value
        self.indexes = indexes


"""
SudokuBoard class.
Represents the game board of the ongoing game.
"""


class SudokuBoard:
    cells = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    def __init__(self, playing_board):
        self.playing_board = playing_board
        self.cells_list = SudokuBoard.cells
        self.curr_cell = None
        self.solved = False

    def initialize_cell_array(self):
        for i in range(9):
            for j in range(9):
                if self.playing_board[i][j] != 0:
                    self.cells_list[i][j] = Cell(self.playing_board[i][j], 0, (i, j))
                else:
                    self.cells_list[i][j] = Cell(0, 0, (i, j))

    def draw_lines_around_cell(self):
        i, j = self.curr_cell.indexes
        pygame.draw.line(game_display, RED, (j * 90, i * 90), ((j + 1) * 90, (i + 1) * 90))
        pygame.draw.line(game_display, RED, (j * 90, (i + 1) * 90), (((j + 1) * 90), (i + 1) * 90))
        pygame.display.update()

    def detect_clicked_cell(self, pos):
        j_index = pos[0] // 90
        i_index = pos[1] // 90
        if (0 <= i_index <= 8) and (0 <= j_index <= 8):
            self.curr_cell = self.cells[i_index][j_index]
            self.draw_lines_around_cell()
            return True

        return False

    def place_guess(self, indexes, num):
        i, j = indexes
        if self.playing_board[i][j] != 0:
            error_text = text_font.render("Cant change this cell!!!!", True, BLACK)
            game_display.blit(error_text, (25, 830))
            return
        else:
            self.cells_list[i][j].temp_value = num
            self.curr_cell = self.cells_list[i][j]
            num_text = num_font.render(str(num), True, LIGHT_GRAY)
            game_display.blit(num_text, (j * 90 + 10, i * 90 + 10))
            return

    def place_final_guess(self):
        i, j = self.curr_cell.indexes
        copy_board = copy.deepcopy(self.playing_board)
        if self.playing_board[i][j] != 0:
            error_text = text_font.render("Cant change this cell!!!!", True, BLACK)
            game_display.blit(error_text, (25, 830))
            pygame.display.update()
            pygame.time.wait(2000)
        else:
            if game_logic.is_board_valid(self.playing_board, self.curr_cell.temp_value, i, j):
                copy_board[i][j] = self.curr_cell.temp_value
                if game_logic.solve_board(copy_board):
                    self.playing_board[i][j] = self.curr_cell.temp_value
                    self.cells_list[i][j].final_value = self.cells_list[i][j].temp_value
                    self.cells_list[i][j].temp_value = 0
                    self.playing_board[i][j] = self.curr_cell.final_value
                    self.curr_cell = self.cells_list[i][j]
                    num_text = num_font.render(str(self.curr_cell.final_value), True, BLACK)
                    game_display.blit(num_text, (j * 90 + 45, i * 90 + 45))
                else:
                    self.playing_board[i][j] = 0
                    error_text = text_font.render("Not solvable", True, BLACK)
                    game_display.blit(error_text, (25, 830))
                    pygame.display.update()
                    pygame.time.wait(2000)
            else:
                error_text = text_font.render("Cant place this number here", True, BLACK)
                game_display.blit(error_text, (25, 830))
                pygame.display.update()
                pygame.time.wait(2000)

    def is_board_solved(self):
        for i in range(9):
            for j in range(9):
                if self.playing_board[i][j] == 0:
                    return False
        return True

    def print_current_grid(self):
        for i in range(9):
            for j in range(9):
                if self.playing_board[i][j] != 0:
                    num_text = num_font.render(str(self.playing_board[i][j]), True, BLACK)
                    game_display.blit(num_text, (j * 90 + 45, i * 90 + 45))
                else:
                    if self.cells_list[i][j].temp_value != 0:
                        num_text = num_font.render(str(self.cells_list[i][j].temp_value), True, LIGHT_GRAY)
                        game_display.blit(num_text, (j * 90 + 10, i * 90 + 10))

    def delete_cell(self):
        i, j = self.curr_cell.indexes
        if self.playing_board[i][j] != 0:
            error_text = text_font.render("Cant delete this number", True, BLACK)
            game_display.blit(error_text, (25, 830))
            pygame.display.update()
            pygame.time.wait(2000)
        else:
            self.curr_cell.temp_value = 0

    def visualize_solution(self):
        empty_cell_pos = game_logic.find_empty_place(self.playing_board)
        if not empty_cell_pos:
            return True
        else:
            row, col = empty_cell_pos
            pos_x = col * CELL_SIZE + 45
            pos_y = row * CELL_SIZE + 45

        for i in range(1, 10):
            if game_logic.is_board_valid(self.playing_board, i, row, col):
                self.playing_board[row][col] = i
                self.curr_cell = self.cells[row][col]
                pygame.draw.rect(game_display, GREEN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                num_text = num_font.render(str(i), True, BLACK)
                game_display.blit(num_text, (pos_x, pos_y))
                pygame.display.update()
                pygame.time.delay(100)
                if self.visualize_solution():
                    return True

            self.playing_board[row][col] = 0
            pygame.draw.rect(game_display, RED, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            num_text = num_font.render(str(i), True, BLACK)
            game_display.blit(num_text, (pos_x, pos_y))
            pygame.display.update()
            pygame.time.delay(100)

        return False


# Sets size of grid window sizes need to divide by 9
WINDOW_WIDTH = 810
WINDOW_HEIGHT = 880
END_GRID_HEIGHT = 810
SQUARE_SIZE = WINDOW_WIDTH // 3
CELL_SIZE = SQUARE_SIZE // 3

# Set up the colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Function to draw the sudoku grid
def draw_grid():

    # Draw the secondary horizontal lines
    for i in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(game_display, LIGHT_GRAY, (i, 0), (i, END_GRID_HEIGHT))

    # Draw the secondary vertical lines
    for j in range(0, END_GRID_HEIGHT, CELL_SIZE):
        pygame.draw.line(game_display, LIGHT_GRAY, (0, j), (WINDOW_WIDTH, j))

    # Draw the main horizontal lines
    for i in range(0, WINDOW_WIDTH, SQUARE_SIZE):
        pygame.draw.line(game_display, BLACK, (i, 0), (i, END_GRID_HEIGHT))

    # Draw the main vertical lines
    for j in range(0, END_GRID_HEIGHT + 2, SQUARE_SIZE):
        pygame.draw.line(game_display, BLACK, (0, j), (WINDOW_WIDTH, j))


def generate_board():
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

    return board


def draw_current_game_window(board):
    game_display.fill(WHITE)
    draw_grid()
    game_board.print_current_grid()


# Setting the game window, fonts and text
pygame.init()
game_display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("sudoku solver")
text_font = pygame.font.Font("freesansbold.ttf", 20)
solve_button_text = text_font.render("SOLVE!", True, BLACK)
num_font = pygame.font.SysFont("comicsans", 40)


# Creating a new game
game_board = SudokuBoard(generate_board())
game_board.initialize_cell_array()
draw_current_game_window(game_board)
solve_button = pygame.draw.rect(game_display, RED, (675, 818, 120, 55))
game_display.blit(solve_button_text, (700, 835))
pressed_key = 0
is_valid_cell = False


# Main game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            click_pos = pygame.mouse.get_pos()
            if solve_button.collidepoint(click_pos):
                game_board.visualize_solution()
            is_valid_cell = game_board.detect_clicked_cell(click_pos)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                pressed_key = 1
            if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                pressed_key = 2
            if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                pressed_key = 3
            if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                pressed_key = 4
            if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                pressed_key = 5
            if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                pressed_key = 6
            if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                pressed_key = 7
            if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                pressed_key = 8
            if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                pressed_key = 9
            if event.key == pygame.K_DELETE:
                game_board.delete_cell()
                is_valid_cell = False
            if event.key == pygame.K_RETURN:
                game_board.place_final_guess()
                is_valid_cell = False
                if game_board.is_board_solved():
                    win_text = text_font.render("You woooonnnnnnnn", True, BLACK)
                    game_display.blit(win_text, (25, 830))
                    pygame.display.update()
                    pygame.time.wait(2000)
                    run = False

        if is_valid_cell and pressed_key != 0:
            game_board.place_guess(game_board.curr_cell.indexes, pressed_key)
            pressed_key = 0
            cell_indexes = False

    draw_current_game_window(game_board)
    solve_button = pygame.draw.rect(game_display, RED, (675, 818, 120, 55))
    game_display.blit(solve_button_text, (700, 835))
    pygame.display.update()

pygame.quit()
sys.exit()
