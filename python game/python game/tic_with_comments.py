import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_PADDING = 50
LINE_WIDTH = 20
BOARD_SIZE = 3
CELL_SIZE = (WIDTH - 2 * GRID_PADDING) // BOARD_SIZE
FPS = 60

# Colors
BACKGROUND_GRADIENT_START = (50, 50, 50)
BACKGROUND_GRADIENT_END = (30, 30, 30)
GRID_GRADIENT_START = (120, 120, 120)
GRID_GRADIENT_END = (128, 0, 128)
PLAYER_TURN_GRADIENT_START = (200, 200, 200)
PLAYER_TURN_GRADIENT_END = (128, 0, 128)
RED = (255, 0, 0)
FONT_SIZE = 36

# Initialize the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

# Load background image
background_image = pygame.image.load("background_image.jpg").convert()
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Function to draw the Tic-Tac-Toe board
def draw_board():
    for i in range(1, BOARD_SIZE):
        pygame.draw.line(screen, GRID_GRADIENT_END, (GRID_PADDING + i * CELL_SIZE, GRID_PADDING),
                         (GRID_PADDING + i * CELL_SIZE, HEIGHT - GRID_PADDING), LINE_WIDTH)
        pygame.draw.line(screen, GRID_GRADIENT_END, (GRID_PADDING, GRID_PADDING + i * CELL_SIZE),
                         (WIDTH - GRID_PADDING, GRID_PADDING + i * CELL_SIZE), LINE_WIDTH)

# Function to draw X at a given position with animation
def draw_x(row, col, progress):
    start_pos1 = (GRID_PADDING + col * CELL_SIZE + CELL_SIZE // 4, GRID_PADDING + row * CELL_SIZE + CELL_SIZE // 4)
    end_pos1 = (GRID_PADDING + (col + 1) * CELL_SIZE - CELL_SIZE // 4, GRID_PADDING + (row + 1) * CELL_SIZE - CELL_SIZE // 4)
    current_pos1 = (start_pos1[0] + (end_pos1[0] - start_pos1[0]) * progress,
                   start_pos1[1] + (end_pos1[1] - start_pos1[1]) * progress)

    start_pos2 = (GRID_PADDING + (col + 1) * CELL_SIZE - CELL_SIZE // 4, GRID_PADDING + row * CELL_SIZE + CELL_SIZE // 4)
    end_pos2 = (GRID_PADDING + col * CELL_SIZE + CELL_SIZE // 4, GRID_PADDING + (row + 1) * CELL_SIZE - CELL_SIZE // 4)
    current_pos2 = (start_pos2[0] + (end_pos2[0] - start_pos2[0]) * progress,
                   start_pos2[1] + (end_pos2[1] - start_pos2[1]) * progress)

    pygame.draw.line(screen, PLAYER_TURN_GRADIENT_END, start_pos1, current_pos1, LINE_WIDTH)
    pygame.draw.line(screen, PLAYER_TURN_GRADIENT_END, start_pos2, current_pos2, LINE_WIDTH)

# Function to draw O at a given position with animation
def draw_o(row, col, progress):
    center = (GRID_PADDING + col * CELL_SIZE + CELL_SIZE // 2, GRID_PADDING + row * CELL_SIZE + CELL_SIZE // 2)
    radius = CELL_SIZE // 3
    current_radius = radius * progress

    pygame.draw.circle(screen, PLAYER_TURN_GRADIENT_END, center, int(current_radius), LINE_WIDTH)

# Function to check for a win
def check_winner(board, player):
    for i in range(BOARD_SIZE):
        if all(board[i][j] == player for j in range(BOARD_SIZE)) or all(board[j][i] == player for j in range(BOARD_SIZE)):
            return True

    if all(board[i][i] == player for i in range(BOARD_SIZE)) or all(board[i][BOARD_SIZE - 1 - i] == player for i in range(BOARD_SIZE)):
        return True

    return False

# Function to check for a draw
def check_draw(board):
    return all(board[i][j] != ' ' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE))

# Function to make a move for the computer with a delay
def make_computer_move(board):
    pygame.time.wait(1000)
    empty_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == ' ']
    return random.choice(empty_cells) if empty_cells else None

# Function to display loading animation
def draw_loading_animation():
    loading_text = font.render("Computer's Turn...", True, PLAYER_TURN_GRADIENT_END)
    text_rect = loading_text.get_rect(center=(WIDTH // 2, GRID_PADDING // 2))
    screen.blit(loading_text, text_rect)

# Main game loop
def main():
    board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = 'X'
    progress = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == 'X':
                col = (event.pos[0] - GRID_PADDING) // CELL_SIZE
                row = (event.pos[1] - GRID_PADDING) // CELL_SIZE

                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board[row][col] == ' ':
                    board[row][col] = 'X'
                    current_player = 'O'

        # Draw background image
        screen.blit(background_image, (0, 0))

        draw_board()

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if board[i][j] == 'X':
                    draw_x(i, j, progress)
                elif board[i][j] == 'O':
                    draw_o(i, j, progress)

        # Display player turn or loading animation
        if current_player == 'X':
            player_turn_text = font.render(f"Player {current_player}'s turn", True, PLAYER_TURN_GRADIENT_END)
            text_rect = player_turn_text.get_rect(center=(WIDTH // 2, GRID_PADDING // 2))
            screen.blit(player_turn_text, text_rect)
        else:
            draw_loading_animation()

        pygame.display.flip()
        clock.tick(FPS)

        # Computer's move
        if current_player == 'O':
            computer_move = make_computer_move(board)
            if computer_move:
                row, col = computer_move
                board[row][col] = 'O'
                current_player = 'X'

        # Animate moves
        if progress < 1:
            progress += 0.05

        # Check for a winner or draw
        if check_winner(board, 'X'):
            print("Player X wins!")
            pygame.quit()
            sys.exit()
        elif check_winner(board, 'O'):
            print("Player O wins!")
            pygame.quit()
            sys.exit()
        elif check_draw(board):
            print("It's a draw!")
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
