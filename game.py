from constants import *
from circle import Circle
import pygame
import random
import math

class Game:
    def __init__(self, win):
        self.win = win
        self.colors = [RED, YELLOW]
        self.turn = 0
        self.human_turn = 0
        self.starting_pos = (0, 6)
        self.mouse_pos = None
        self.over = False
        self.tie = False
        self.move_count = 0
        self.create_board()
        self.draw_start_screen()
        self.starting_circle()

    def starting_circle(self):
        circle = Circle(self.win, self.colors[self.turn], self.starting_pos[0], self.starting_pos[1])
        self.board[self.starting_pos[0]][self.starting_pos[1]] = circle
        circle.draw()

    def change_turn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0

    def get_circle(self, row, col, board):
        return board[row][col]

    def clear(self, row, col):
        pygame.draw.circle(self.win, WHITE, (col * SQUARE_SIZE + RADIUS, row * SQUARE_SIZE + RADIUS), RADIUS)

    def move(self, circle, row, col):
        self.clear(circle.row, circle.col)
        self.board[circle.row][circle.col], self.board[row][col] = self.board[row][col], self.board[circle.row][
            circle.col]
        circle.move(row, col)

    def get_valid_row(self, col, board):
        for row in range(ROWS):
            circle = self.get_circle(ROWS - row, col, board)
            if not circle:
                return ROWS - row

    def check_if_won(self, color, board):
        # Check vertical
        for c in range(COLS):
            for r in range(ROWS - 3):
                if board[r + 1][c] and board[r + 2][c] and board[r + 3][c] and board[r + 4][c]:
                    if board[r + 1][c].color == board[r + 2][c].color == board[r + 3][c].color == \
                            board[r + 4][c].color == color:
                        return True

        # Check horizontal
        for r in range(ROWS):
            for c in range(COLS - 3):
                if board[r + 1][c] and board[r + 1][c + 1] and board[r + 1][c + 2] and board[r + 1][
                    c + 3]:
                    if board[r + 1][c].color == board[r + 1][c + 1].color == board[r + 1][c + 2].color == \
                            board[r + 1][c + 3].color == color:
                        return True

        # Check positively sloped diagonales
        for c in range(COLS - 3):
            for r in range(ROWS - 3):
                if board[r + 1][c] and board[r + 2][c + 1] and board[r + 3][c + 2] and board[r + 4][
                    c + 3]:
                    if board[r + 1][c].color == board[r + 2][c + 1].color == board[r + 3][c + 2].color == \
                            board[r + 4][c + 3].color == color:
                        return True

        # Check negatively sloped diagonales
        for c in range(COLS - 3):
            for r in range(3, ROWS):
                if board[r + 1][c] and board[r][c + 1] and board[r - 1][c + 2] and board[r - 2][
                    c + 3]:
                    if board[r + 1][c].color == board[r][c + 1].color == board[r - 1][c + 2].color == \
                            board[r - 2][c + 3].color == color:
                        return True

    def game_over(self):
        font = pygame.font.SysFont("Arial", 40)
        if self.tie:
            text = font.render(f"It's a tie!!!", True, BLACK)
        else:
            text = font.render(f"{'RED' if self.colors[self.turn] == (255, 0, 0) else 'YELLOW'} won!!!", True, BLACK)
        self.win.blit(text, (WIDTH / 2 - (text.get_width() / 2), PADDING / 2 - (text.get_height() / 2)))

    def draw_frame(self, circle):
        pygame.draw.circle(self.win, BLACK, (circle.col * SQUARE_SIZE + RADIUS, circle.row * SQUARE_SIZE + RADIUS),
                           RADIUS, 2)

    def remove_frame(self, circle):
        self.clear(circle.row, circle.col)
        circle.draw()

    def clicked(self):
        for col in range(COLS):
            if self.get_circle(self.starting_pos[0], col, self.board):
                circle = self.get_circle(self.starting_pos[0], col, self.board)

        if self.mouse_pos[0] == 0:
            if self.mouse_pos == circle.pos and not circle.selected:
                circle.selected = True
                self.draw_frame(circle)
            elif self.mouse_pos == circle.pos and circle.selected:
                row = self.get_valid_row(circle.col, self.board)
                if row:
                    self.move(circle, row, circle.col)
                    if self.check_if_won(self.colors[self.turn], self.board):
                        self.over = True
                        self.game_over()
                    else:
                        self.move_count += 1
                        if self.move_count == ROWS * COLS:
                            self.tie = True
                            self.over = True
                            self.game_over()
                        else:
                            self.change_turn()
                            self.starting_circle()
            elif self.mouse_pos != circle.pos and circle.selected:
                self.move(circle, self.mouse_pos[0], self.mouse_pos[1])
                self.draw_frame(circle)
            else:
                circle.selected = False
                self.remove_frame(circle)
        else:
            circle.selected = False
            self.remove_frame(circle)

    def create_board(self):
        self.board = []
        for row in range(ROWS + 1):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(0)

    def draw_start_screen(self):
        self.win.fill(WHITE)

        pygame.draw.rect(self.win, BLUE, pygame.Rect(0, PADDING, WIDTH, HEIGHT - PADDING))

        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.circle(self.win, WHITE, (col * SQUARE_SIZE + RADIUS, row * SQUARE_SIZE + RADIUS + PADDING),
                                   RADIUS)

    def drop_circle(self, board, row, col, player):
        board[row][col] = Circle(self.win, self.colors[player], row, col)

    def get_available_moves(self, board):
        moves = []

        for col in range(COLS):
            row = self.get_valid_row(col, board)
            if row:
                moves.append((row, col))

        return moves

    def minimax(self, board, depth, max_player):

        computer_player = 0 if self.human_turn == 1 else 1

        if depth == 0 or self.check_if_won(self.colors[self.human_turn], board) or self.check_if_won(self.colors[computer_player], board) or self.move_count == ROWS * COLS:
            if self.check_if_won(self.colors[self.human_turn], board) or self.check_if_won(self.colors[computer_player], board) or self.move_count == ROWS * COLS:
                if self.check_if_won(self.colors[self.human_turn], board):
                    return (None, -math.inf)
                elif self.check_if_won(self.colors[computer_player], board):
                    return (None, math.inf)
                else: # That means there are no valid moves
                    return (None, 0)
            else: # Depth is 0
                return (None, self.score_pos(board, computer_player))

        if max_player:
            value = -math.inf
            position = random.choice(self.get_available_moves(board))
            for pos in self.get_available_moves(board):
                board_copy = []
                for i in range(len(board)):
                    board_copy.append([])
                    for j in range(len(board[i])):
                        board_copy[i].append(board[i][j])

                self.drop_circle(board_copy, pos[0], pos[1], computer_player)
                new_score = self.minimax(board_copy, depth - 1, False)[1]
                if new_score > value:
                    value = new_score
                    position = pos

            return position, value

        else: # Min player
            value = math.inf
            position = random.choice(self.get_available_moves(board))
            for pos in self.get_available_moves(board):
                board_copy = []
                for i in range(len(board)):
                    board_copy.append([])
                    for j in range(len(board[i])):
                        board_copy[i].append(board[i][j])

                self.drop_circle(board_copy, pos[0], pos[1], self.human_turn)
                new_score = self.minimax(board_copy, depth - 1, True)[1]
                if new_score < value:
                    value = new_score
                    position = pos

            return position, value

    def score_win(self, window, player):
        score = 0
        you = 0
        enemy = 0
        empty = 0
        for circle in window:
            if circle:
                if circle.color == self.colors[player]:
                    you += 1
                else:
                    enemy += 1
            else:
                empty += 1

        if you == 4:
            score += 10000
        elif you == 3 and empty == 1:
            score += 5
        elif you == 2 and empty == 2:
            score += 2
        elif enemy == 3 and empty == 1:
            score -= 4

        return score

    def score_pos(self, board, player):
        score = 0

        # Score center column
        for row in range(ROWS):
            if board[row + 1][3]:
                if board[row + 1][3].color == self.colors[player]:
                    score += 3

        # Score horizontal
        for row in range(ROWS):
            row_list = board[row + 1]
            for col in range(COLS - 3):
                window = row_list[col:col + WINDOW_LENGTH]
                score += self.score_win(window, player)

        # Score vertical
        for col in range(COLS):
            col_list = [board[i + 1][col] for i in range(ROWS)]
            for row in range(ROWS - 3):
                window = col_list[row + 1:row + 1 + WINDOW_LENGTH]
                score += self.score_win(window, player)

        # Score positively sloped diagonals
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                window = [board[row + 3 + 1 - i][col + i] for i in range(WINDOW_LENGTH)]
                score += self.score_win(window, player)

        # Score positively sloped diagonals
        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                window = [board[row + 1 + i][col + i] for i in range(WINDOW_LENGTH)]
                score += self.score_win(window, player)

        return score