import pygame
import random

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_WIDTH = 10  # 10 blocks wide
BOARD_HEIGHT = 17  # 17 blocks tall
BLOCK_SIZE = 40  # Size of each block on the main board
PREVIEW_BLOCK_SIZE = 25  # Smaller block size for previews (inventory/next blocks)
INITIAL_DROP_SPEED = 600  # Set a moderate drop speed in milliseconds
LEVEL_INCREMENT = 100  # Increase level every 100 points
LEVEL_SPEEDUP = 1  # FPS increase per level up

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (238, 130, 238)

# Block colors
BLOCK_COLORS = {
    'O': RED,
    'I': ORANGE,
    'S': YELLOW,
    'Z': GREEN,
    'L': BLUE,
    'J': INDIGO,
    'T': VIOLET,
}

# Block shapes
SHAPES = {
    'O': [[1, 1], [1, 1]],
    'I': [[1], [1], [1], [1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'L': [[1, 0], [1, 0], [1, 1]],
    'J': [[0, 1], [0, 1], [1, 1]],
    'T': [[1, 1, 1], [0, 1, 0]],
}

# Fonts
font_large = pygame.font.SysFont(None, 80)
font_medium = pygame.font.SysFont(None, 36)

class Block:
    def __init__(self, shape_key):
        """Initialize a block with a shape and fixed color."""
        self.shape_key = shape_key
        self.shape = SHAPES[shape_key]
        self.color = BLOCK_COLORS[shape_key]
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        """Rotate the block shape clockwise."""
        new_shape = [list(row) for row in zip(*self.shape[::-1])]
        if not game.will_collide(new_shape, 0, 0):  # Check if rotation will cause collision
            self.shape = new_shape

    def reset_position(self):
        """Reset the block position to the top of the board."""
        self.x = BOARD_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

class GhostLine:
    def get_ghost_y(self, block):
        """Get the y-position where the block will land."""
        ghost_y = block.y
        while not game.will_collide(block.shape, 0, ghost_y - block.y + 1):
            ghost_y += 1
        return ghost_y

    def draw(self, screen, block, x_offset, y_offset):
        """Draw the ghost line at the predicted landing position."""
        ghost_y = self.get_ghost_y(block)
        for row_index, row in enumerate(block.shape):
            for col_index, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, block.color,  # Use block color for ghost line
                                     (x_offset + (block.x + col_index) * BLOCK_SIZE,
                                      y_offset + (ghost_y + row_index) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2)

class GameBoard:
    def __init__(self):
        """Initialize the game board with empty spaces."""
        self.board = [[WHITE for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.stored_block = None
        self.current_block = None
        self.next_blocks = [Block(random.choice(list(SHAPES.keys()))) for _ in range(3)]
        self.ghost_block = GhostLine()
        self.drop_speed = INITIAL_DROP_SPEED
        self.last_drop_time = pygame.time.get_ticks()
        self.game_state = "menu"

    def new_block(self):
        """Create a new block from the next_blocks list and store the current one."""
        self.current_block = self.next_blocks.pop(0)
        self.next_blocks.append(Block(random.choice(list(SHAPES.keys()))))
        if self.will_collide(self.current_block.shape, 0, 0):
            self.game_state = "game_over"

    def move_block(self, dx, dy):
        """Move the current block by a certain amount if there is no collision."""
        if not self.will_collide(self.current_block.shape, dx, dy):
            self.current_block.x += dx
            self.current_block.y += dy
        elif dy > 0:  # If moving down and collides, lock the block
            self.lock_block()
            self.new_block()

    def rotate_block(self):
        """Rotate the current block if possible."""
        current_time = pygame.time.get_ticks()
        if current_time - getattr(self, 'last_rotation_time', 0) > 500:  # 500ms delay between rotations
            self.current_block.rotate()
            self.last_rotation_time = current_time

    def store_current_block(self):
        """Store the current block in the inventory or switch with the stored block."""
        if self.stored_block is None:
            self.stored_block = Block(self.current_block.shape_key)  # Store a new instance of the block in its original form
            self.new_block()
        else:
            # Swap the current block with the stored block and reset position
            self.current_block, self.stored_block = self.stored_block, Block(self.current_block.shape_key)
            self.current_block.reset_position()

    def use_stored_block(self):
        """Use the stored block if available."""
        if self.stored_block:
            self.current_block, self.stored_block = self.stored_block, Block(self.current_block.shape_key)
            self.current_block.reset_position()

    def lock_block(self):
        """Lock the current block into the board and check for full rows."""
        for row_index, row in enumerate(self.current_block.shape):
            for col_index, val in enumerate(row):
                if val:
                    x = self.current_block.x + col_index
                    y = self.current_block.y + row_index
                    if y >= 0:
                        self.board[y][x] = self.current_block.color
        rows_cleared = self.clear_full_rows()
        self.lines_cleared += rows_cleared
        self.score += rows_cleared * 10
        self.update_level()

    def clear_full_rows(self):
        """Clear any full rows from the board and return the number of rows cleared."""
        rows_to_clear = [index for index, row in enumerate(self.board) if all(col != WHITE for col in row)]
        for row_index in rows_to_clear:
            del self.board[row_index]
            self.board.insert(0, [WHITE for _ in range(BOARD_WIDTH)])
        return len(rows_to_clear)

    def update_level(self):
        """Increase the level and speed based on lines cleared."""
        if self.lines_cleared // 10 >= self.level:
            self.level += 1
            self.drop_speed = max(200, self.drop_speed - 50)

    def will_collide(self, shape, dx, dy):
        """Check if moving or rotating the block will cause a collision."""
        for row_index, row in enumerate(shape):
            for col_index, val in enumerate(row):
                if val:
                    new_x = self.current_block.x + col_index + dx
                    new_y = self.current_block.y + row_index + dy
                    if new_x < 0 or new_x >= BOARD_WIDTH or new_y >= BOARD_HEIGHT:
                        return True
                    if new_y >= 0 and self.board[new_y][new_x] != WHITE:
                        return True
        return False

    def handle_input(self):
    #Handle player input for block movement and control.
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        # Faster response for moving left and right (e.g., 100ms delay)
        if keys[pygame.K_LEFT] and current_time - getattr(self, 'last_move_time', 0) > 100:
            self.move_block(-1, 0)
            self.last_move_time = current_time
        elif keys[pygame.K_RIGHT] and current_time - getattr(self, 'last_move_time', 0) > 100:
            self.move_block(1, 0)
            self.last_move_time = current_time

        # Keep slower response for rotating (e.g., 500ms delay)
        if keys[pygame.K_UP] and current_time - getattr(self, 'last_rotation_time', 0) > 500:
            self.rotate_block()
            self.last_rotation_time = current_time

        # Keep faster response for soft drop (e.g., 300ms delay)
        if keys[pygame.K_DOWN] and current_time - getattr(self, 'last_drop_time', 0) > 300:
            self.move_block(0, 1)
            self.last_drop_time = current_time

        # Store block with 'z'
        if keys[pygame.K_z]:
            self.store_current_block()

        # Use stored block with 'x'
        if keys[pygame.K_x]:
            self.use_stored_block()

        # Hard drop with spacebar, keep delay as needed (e.g., 500ms)
        if keys[pygame.K_SPACE] and current_time - getattr(self, 'last_hard_drop_time', 0) > 500:
            while not self.will_collide(self.current_block.shape, 0, 1):
                self.move_block(0, 1)
            self.lock_block()
            self.new_block()
            self.last_hard_drop_time = current_time


    def draw(self, screen):
        """Draw the game board, ghost block, and current block."""
        screen.fill(WHITE)
        
        # Draw the board and blocks
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                pygame.draw.rect(screen, self.board[y][x], 
                                 (200 + x * BLOCK_SIZE, 100 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(screen, BLACK, 
                                 (200 + x * BLOCK_SIZE, 100 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 2)

        # Draw the ghost piece
        self.ghost_block.draw(screen, self.current_block, 200, 100)

        # Draw the current block
        if self.current_block:
            for row_index, row in enumerate(self.current_block.shape):
                for col_index, val in enumerate(row):
                    if val:
                        x_pos = 200 + (self.current_block.x + col_index) * BLOCK_SIZE
                        y_pos = 100 + (self.current_block.y + row_index) * BLOCK_SIZE
                        pygame.draw.rect(screen, self.current_block.color, (x_pos, y_pos, BLOCK_SIZE, BLOCK_SIZE), 0)
                        pygame.draw.rect(screen, BLACK, (x_pos, y_pos, BLOCK_SIZE, BLOCK_SIZE), 2)

        # Display score and level
        game_ui.draw_ui_elements(screen, self.score, self.level, self.stored_block, self.next_blocks)

class UI:
    def draw_ui_elements(self, screen, score, level, stored_block, next_blocks):
        score_text = font_medium.render(f"Score: {score}", True, BLACK)
        level_text = font_medium.render(f"Level: {level}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        self.draw_stored_block(screen, stored_block, 10, 100)
        self.draw_next_blocks(screen, next_blocks, SCREEN_WIDTH - 175, 100)

    def draw_stored_block(self, screen, stored_block, x_offset, y_offset):
        if stored_block:
            for row_index, row in enumerate(stored_block.shape):
                for col_index, val in enumerate(row):
                    if val:
                        pygame.draw.rect(screen, stored_block.color,
                                         (x_offset + col_index * PREVIEW_BLOCK_SIZE,
                                          y_offset + row_index * PREVIEW_BLOCK_SIZE, PREVIEW_BLOCK_SIZE, PREVIEW_BLOCK_SIZE))

    def draw_next_blocks(self, screen, next_blocks, x_offset, y_offset):
        for block_index, block in enumerate(next_blocks):
            for row_index, row in enumerate(block.shape):
                for col_index, val in enumerate(row):
                    if val:
                        pygame.draw.rect(screen, block.color,
                                         (x_offset + col_index * PREVIEW_BLOCK_SIZE,
                                          y_offset + block_index * 5 * PREVIEW_BLOCK_SIZE + row_index * PREVIEW_BLOCK_SIZE, PREVIEW_BLOCK_SIZE, PREVIEW_BLOCK_SIZE))

def draw_menu(screen):
    screen.fill(WHITE)
    title_text = font_large.render("TETRIS", True, BLACK)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 200))
    instruction_text = font_medium.render("Press Enter to Start", True, BLACK)
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 400))
    pygame.display.flip()

def draw_game_over(screen, score):
    screen.fill(WHITE)
    over_text = font_large.render("GAME OVER", True, BLACK)
    score_text = font_medium.render(f"Your Score: {score}", True, BLACK)
    restart_text = font_medium.render("Press Y to Restart or N to Quit", True, BLACK)
    screen.blit(over_text, (SCREEN_WIDTH // 2 - over_text.get_width() // 2, 200))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))
    pygame.display.flip()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')

    clock = pygame.time.Clock()
    global game, game_ui
    game = GameBoard()
    game_ui = UI()

    running = True
    while running:
        if game.game_state == "menu":
            draw_menu(screen)
        elif game.game_state == "game_over":
            draw_game_over(screen, game.score)
        else:
            current_time = pygame.time.get_ticks()
            if current_time - game.last_drop_time > game.drop_speed:
                game.move_block(0, 1)
                game.last_drop_time = current_time
            game.handle_input()
            game.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if game.game_state == "menu" and event.key == pygame.K_RETURN:
                    game.new_block()
                    game.game_state = "playing"
                elif event.key == pygame.K_y and game.game_state == "game_over":
                    game.__init__()
                    game.new_block()
                elif event.key == pygame.K_n and game.game_state == "game_over":
                    running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
