import pygame
from constants import *
from game import Game
import time

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
icon = pygame.image.load(ICON)
pygame.display.set_icon(icon)

def get_mouse_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return (int(row), int(col))

def main():
    game = Game(win)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game.over:
                if game.human_turn == game.turn:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        game.mouse_pos = get_mouse_pos(pygame.mouse.get_pos())
                        game.clicked()
                else:
                    move, minimax_score = game.minimax(game.board, DEPTH, True)

                    for col in range(COLS):
                        if game.get_circle(game.starting_pos[0], col, game.board):
                            circle = game.get_circle(game.starting_pos[0], col, game.board)

                    time.sleep(1)
                    game.move(circle, game.starting_pos[0], move[1])
                    pygame.display.flip()

                    time.sleep(1)
                    game.move(circle, move[0], move[1])
                    if game.check_if_won(game.colors[game.turn], game.board):
                        game.over = True
                        game.game_over()
                    else:
                        game.move_count += 1
                        if game.move_count == ROWS * COLS:
                            game.tie = True
                            game.over = True
                            game.game_over()
                        else:
                            game.change_turn()
                            game.starting_circle()

        pygame.display.flip()

if __name__ == '__main__':
    main()