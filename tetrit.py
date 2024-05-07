import pygame
import random

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]]  # Z
]


class TetrisGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.new_piece()
        self.score = 0
        self.game_over = False

    def new_piece(self):
        return random.choice(SHAPES)

    def draw_block(self, x, y, color):
        pygame.draw.rect(self.screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_board(self):
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if self.board[y][x]:
                    self.draw_block(x, y, self.board[y][x])

    def draw_piece(self, piece, offset_x, offset_y):
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if piece[y][x]:
                    self.draw_block(x + offset_x, y + offset_y, CYAN)

    def check_collision(self, piece, offset_x, offset_y):
        for y in range(len(piece)):
            for x in range(len(piece[y])):
                if piece[y][x]:
                    if offset_x + x < 0 or offset_x + x >= BOARD_WIDTH or \
                       offset_y + y >= BOARD_HEIGHT or \
                       self.board[offset_y + y][offset_x + x]:
                        return True
        return False

    def remove_completed_lines(self):
        lines_to_remove = [i for i, row in enumerate(self.board) if all(row)]
        for index in lines_to_remove:
            del self.board[index]
            self.board.insert(0, [0] * BOARD_WIDTH)
        self.score += len(lines_to_remove)

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and not self.check_collision(self.current_piece,
                                                                self.current_x - 1,
                                                                self.current_y):
                self.current_x -= 1
            if keys[pygame.K_RIGHT] and not self.check_collision(self.current_piece,
                                                                  self.current_x + 1,
                                                                  self.current_y):
                self.current_x += 1
            if keys[pygame.K_DOWN] and not self.check_collision(self.current_piece,
                                                                 self.current_x,
                                                                 self.current_y + 1):
                self.current_y += 1

            if keys[pygame.K_SPACE]:
                while not self.check_collision(self.current_piece,
                                                self.current_x,
                                                self.current_y + 1):
                    self.current_y += 1

            if keys[pygame.K_UP]:
                rotated_piece = [[self.current_piece[j][i] for j in range(len(self.current_piece))] for i in range(len(self.current_piece[0]))]
                if not self.check_collision(rotated_piece, self.current_x, self.current_y):
                    self.current_piece = rotated_piece

            if self.check_collision(self.current_piece, self.current_x, self.current_y + 1):
                for y in range(len(self.current_piece)):
                    for x in range(len(self.current_piece[y])):
                        if self.current_piece[y][x]:
                            self.board[self.current_y + y][self.current_x + x] = 1
                self.remove_completed_lines()
                self.current_piece = self.new_piece()
                self.current_x = BOARD_WIDTH // 2 - len(self.current_piece[0]) // 2
                self.current_y = 0

                if self.check_collision(self.current_piece, self.current_x, self.current_y):
                    self.game_over = True

            self.draw_board()
            self.draw_piece(self.current_piece, self.current_x, self.current_y)
            pygame.display.flip()
            self.clock.tick(10)

        pygame.quit()


if __name__ == "__main__":
    game = TetrisGame()
    game.run()
