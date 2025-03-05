import pygame
import random

# Khởi tạo pygame
pygame.init()

# Kích thước màn hình
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLS, ROWS = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE

# Màu sắc
BACKGROUND_COLOR = (20, 20, 20)
GRID_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
COLORS = [(0, 255, 255), (0, 0, 255), (255, 165, 0), (255, 255, 0),
          (0, 255, 0), (128, 0, 128), (255, 0, 0)]

# Các hình dạng của khối
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

# Lớp đại diện cho khối Tetris
class Tetromino:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Bảng game
board = [[(0, 0, 0) for _ in range(COLS)] for _ in range(ROWS)]
current_piece = Tetromino(COLS // 2, 0)
score = 0

font = pygame.font.Font(None, 36)

def is_valid_position(piece, dx=0, dy=0):
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                new_x = piece.x + j + dx
                new_y = piece.y + i + dy
                if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                    return False
                if new_y >= 0 and board[new_y][new_x] != (0, 0, 0):
                    return False
    return True

def merge_piece(piece):
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                board[piece.y + i][piece.x + j] = piece.color

def clear_rows():
    global board, score
    new_board = [row for row in board if any(cell == (0, 0, 0) for cell in row)]
    cleared = ROWS - len(new_board)
    score += cleared * 100
    while len(new_board) < ROWS:
        new_board.insert(0, [(0, 0, 0) for _ in range(COLS)])
    board = new_board

def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_board():
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell != (0, 0, 0):
                draw_block(x, y, cell)

def draw_block(x, y, color):
    rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, color, rect, border_radius=5)
    pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=5)  # Viền trắng
    pygame.draw.rect(screen, (0, 0, 0), rect.inflate(-4, -4), 2, border_radius=5)  # Bóng tối

def draw_piece(piece):
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                draw_block(piece.x + j, piece.y + i, piece.color)

def draw_score():
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))

# Vòng lặp game
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
fall_time = 0
fall_speed = 500  # 500ms mỗi lần rơi

while running:
    screen.fill(BACKGROUND_COLOR)
    draw_grid()
    draw_board()
    draw_piece(current_piece)
    draw_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and is_valid_position(current_piece, dx=-1):
                current_piece.x -= 1
            elif event.key == pygame.K_RIGHT and is_valid_position(current_piece, dx=1):
                current_piece.x += 1
            elif event.key == pygame.K_DOWN and is_valid_position(current_piece, dy=1):
                current_piece.y += 1
            elif event.key == pygame.K_UP:
                current_piece.rotate()
                if not is_valid_position(current_piece):
                    current_piece.rotate()
                    current_piece.rotate()
                    current_piece.rotate()

    if pygame.time.get_ticks() - fall_time > fall_speed:
        if is_valid_position(current_piece, dy=1):
            current_piece.y += 1
        else:
            merge_piece(current_piece)
            clear_rows()
            current_piece = Tetromino(COLS // 2, 0)
            if not is_valid_position(current_piece):
                running = False  # Game over
        fall_time = pygame.time.get_ticks()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()