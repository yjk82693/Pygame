import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Puzzle Game")

# FPS
FPS = 60
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
BORDER_COLOR = (0, 0, 0)  # Border color for distinguishing blocks
colors = [
    (255, 0, 0),      # Red
    (255, 255, 0),    # Yellow
    (0, 255, 0),      # Green
    (0, 0, 255),      # Blue
    (128, 0, 128),    # Purple
    (255, 165, 0)     # Orange
]

# Block size
BLOCK_SIZE = 64

# 2D Board dimensions (number of blocks horizontally and vertically)
BOARD_WIDTH = 8
BOARD_HEIGHT = 8

# Game States
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME OVER"

# Block Object
class Block:
    def __init__(self):
        self.color = random.choice(colors)
        self.rect = pygame.Rect(0, 0, BLOCK_SIZE, BLOCK_SIZE)

# Game Object
class Game:
    def __init__(self):
        self.score = 0
        self.best_score = 0
        self.time_left = 90  # Start with 1 minute 30 seconds (90 seconds)
        self.board = [[Block() for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.cursor_x = 0
        self.cursor_y = 0
        self.selected = None  # To store the selected block for swapping
        self.state = STATE_MENU
        self.game_over = False

    def create_board(self):
        """Create board ensuring no initial matches."""
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                while self.is_match(x, y):
                    self.board[y][x] = Block()

    def is_match(self, x, y):
        """Check for horizontal and vertical matches."""
        # Check horizontal match
        if x > 1 and self.board[y][x].color == self.board[y][x-1].color == self.board[y][x-2].color:
            return True
        # Check vertical match
        if y > 1 and self.board[y][x].color == self.board[y-1][x].color == self.board[y-2][x].color:
            return True
        return False

    def swap_blocks(self, x1, y1, x2, y2):
        """Swaps two blocks."""
        self.board[y1][x1], self.board[y2][x2] = self.board[y2][x2], self.board[y1][x1]

    def find_matches(self):
        """Find matches of 3 or more and return them as a list."""
        matched_blocks = []
        # Horizontal matches
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH - 2):
                if self.board[y][x].color == self.board[y][x+1].color == self.board[y][x+2].color:
                    matched_blocks += [(x, y), (x+1, y), (x+2, y)]

        # Vertical matches
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT - 2):
                if self.board[y][x].color == self.board[y+1][x].color == self.board[y+2][x].color:
                    matched_blocks += [(x, y), (x, y+1), (x, y+2)]

        return set(matched_blocks)

    def remove_matches(self, matches):
        """Remove matched blocks and fill in new blocks."""
        for x, y in matches:
            self.board[y][x] = None  # Remove block by setting it to None

        # Shift down the blocks and fill in new ones
        for x in range(BOARD_WIDTH):
            column = [self.board[y][x] for y in range(BOARD_HEIGHT) if self.board[y][x] is not None]
            missing = BOARD_HEIGHT - len(column)
            new_blocks = [Block() for _ in range(missing)]
            column = new_blocks + column

            for y in range(BOARD_HEIGHT):
                self.board[y][x] = column[y]

        # Update score
        self.score += len(matches) * 10
        # Increase time left by 0.1 second for each matching block
        self.time_left += len(matches) * 0.1

    def resolve_board(self):
        """Resolve the board until no more matches exist."""
        while True:
            matches = self.find_matches()
            if matches:
                self.remove_matches(matches)
            else:
                break

    def update(self):
        """Main game logic, including time decrement."""
        if self.state == STATE_PLAYING:
            if self.time_left > 0:
                self.time_left -= 1 / FPS  # Decrease time by the frame rate
            else:
                self.state = STATE_GAME_OVER  # If time runs out, switch to GAME OVER
                self.game_over = True
                # Update the best score
                if self.score > self.best_score:
                    self.best_score = self.score

    def draw(self):
        """Draws the game elements to the screen."""
        screen.fill(BLACK)

        if self.state == STATE_MENU:
            # Draw the main menu
            font = pygame.font.SysFont(None, 72)
            title_text = font.render("Puzzle Game", True, WHITE)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))

            font_small = pygame.font.SysFont(None, 48)
            start_text = font_small.render("Press Enter to Start", True, WHITE)
            screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))

        elif self.state == STATE_PLAYING:
            # Draw the blocks and the borders around them
            for y in range(BOARD_HEIGHT):
                for x in range(BOARD_WIDTH):
                    block = self.board[y][x]
                    block.rect.topleft = (x * BLOCK_SIZE, y * BLOCK_SIZE + 100)  # Offset for score display
                    pygame.draw.rect(screen, block.color, block.rect)

                    # Draw the regular border
                    pygame.draw.rect(screen, BORDER_COLOR, block.rect, 2)

                    # If block is selected, highlight it with a bold white border
                    if self.selected == (x, y):
                        pygame.draw.rect(screen, WHITE, block.rect, 5)  # Draw a thicker white border

            # Draw the cursor (the current position of the player)
            pygame.draw.rect(screen, WHITE, (self.cursor_x * BLOCK_SIZE, self.cursor_y * BLOCK_SIZE + 100, BLOCK_SIZE, BLOCK_SIZE), 3)

            # Draw the score
            font = pygame.font.SysFont(None, 48)
            score_text = font.render(f"Score: {self.score}", True, TEXT_COLOR)
            screen.blit(score_text, (10, 10))

            # Draw the time left
            time_text = font.render(f"Time: {int(self.time_left)}", True, TEXT_COLOR)
            screen.blit(time_text, (SCREEN_WIDTH - 200, 10))

        elif self.state == STATE_GAME_OVER:
            # Draw the game over screen
            font = pygame.font.SysFont(None, 72)
            game_over_text = font.render("Game Over!", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 4))

            font_small = pygame.font.SysFont(None, 48)
            current_score_text = font_small.render(f"Your Score: {self.score}", True, WHITE)
            screen.blit(current_score_text, (SCREEN_WIDTH // 2 - current_score_text.get_width() // 2, SCREEN_HEIGHT // 2))

            best_score_text = font_small.render(f"Best Score: {self.best_score}", True, WHITE)
            screen.blit(best_score_text, (SCREEN_WIDTH // 2 - best_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

            restart_text = font_small.render("Press Enter to Restart", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))


    def handle_input(self, event):
        """Handles cursor movement, block selection/swap, and menu inputs."""
        if self.state == STATE_MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = STATE_PLAYING
                self.create_board()

        elif self.state == STATE_PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.cursor_x > 0:
                    self.cursor_x -= 1
                elif event.key == pygame.K_RIGHT and self.cursor_x < BOARD_WIDTH - 1:
                    self.cursor_x += 1
                elif event.key == pygame.K_UP and self.cursor_y > 0:
                    self.cursor_y -= 1
                elif event.key == pygame.K_DOWN and self.cursor_y < BOARD_HEIGHT - 1:
                    self.cursor_y += 1
                elif event.key == pygame.K_SPACE:
                    if self.selected is None:
                        self.selected = (self.cursor_x, self.cursor_y)  # Select the first block
                    else:
                        # Try swapping blocks
                        self.swap_blocks(self.selected[0], self.selected[1], self.cursor_x, self.cursor_y)
                        
                        # Check for matches after swapping
                        matches = self.find_matches()
                        if matches:
                            self.resolve_board()  # Resolve board if there are matches
                        else:
                            # No match, so revert the swap
                            self.swap_blocks(self.selected[0], self.selected[1], self.cursor_x, self.cursor_y)
                        
                        self.selected = None  # Deselect the block

        elif self.state == STATE_GAME_OVER:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Restart the game
                self.score = 0
                self.time_left = 90
                self.state = STATE_PLAYING
                self.create_board()

# Main Game Loop
def main():
    game = Game()
    
    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_input(event)

        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
