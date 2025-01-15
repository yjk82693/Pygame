import pygame
import os
import sys
import random

# Screen settings
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 720
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (20, 60, 120)
ORANGE = (250, 170, 70)
RED = (250, 0, 0)

# Serving states
SERVING = 0
PLAYING = 1
GAME_OVER = 2
WINNING_SELECTION = 3
DIFFICULTY_SELECTION = 4

# Difficulty levels
EASY = 1
MEDIUM = 2
HARD = 3

# Function to serve the ball
def serve_ball(ball, player):
    ball.rect.x = player.rect.centerx - ball.rect.width // 2
    ball.rect.y = player.rect.centery - ball.rect.height - 10
    ball.dx = 0  # Ball doesn't move horizontally before serve
    ball.dy = 0  # Ball stays on the paddle until player moves to serve
    return SERVING  # Return serving state

# Define resource path function
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Defining the Ball
class Ball():
    def __init__(self, bounceSound):
        self.rect = pygame.Rect(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), 12, 12)
        self.bounceSound = bounceSound
        self.dx = random.randint(-3, 3)
        self.dy = 5

    # Updating the position of the ball
    def update(self, player, opponent):
        # Check for potential collision before moving the ball
        self.check_collisions(player, opponent)
        
        # Move the ball after handling collisions
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # Handle when the ball goes out of the screen
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.dx *= -1
            self.bounceSound.play()
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.dy *= -1
            self.bounceSound.play()

    # Check for potential collisions with the paddles
    def check_collisions(self, player, opponent):
        # Ball collision with player paddle
        if self.rect.colliderect(player.rect) and self.dy > 0:
            self.rect.bottom = player.rect.top
            self.dy *= -1  # Reverse the vertical direction
            self.dx += player.dx // 2  # Add player's horizontal velocity to the ball
            self.bounceSound.play()

        # Ball collision with opponent paddle
        elif self.rect.colliderect(opponent.rect) and self.dy < 0:
            self.rect.top = opponent.rect.bottom
            self.dy *= -1  # Reverse the vertical direction
            self.dx += random.choice([-2, 2])  # Add a slight random variation
            self.bounceSound.play()

    # Resetting the ball's position and velocity
    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.dx = random.randint(-3, 3)
        self.dy = 5

    # Drawing the ball
    def draw(self, screen):
        pygame.draw.rect(screen, ORANGE, self.rect)

# Defining Player Object
class Player():
    def __init__(self, pingSound):
        self.rect = pygame.Rect(int(SCREEN_WIDTH / 2), SCREEN_HEIGHT - 40, 50, 15)
        self.pingSound = pingSound
        self.dx = 0
        self.dy = 0

    # Update function for Player movements
    def update(self, ball, is_serving):
        # Horizontal movement (left/right)
        if self.rect.left <= 0 and self.dx < 0:
            self.dx = 0
        elif self.rect.right >= SCREEN_WIDTH and self.dx > 0:
            self.dx = 0

        # Vertical movement (up/down)
        if self.rect.top <= SCREEN_HEIGHT / 2 and self.dy < 0:
            self.dy = 0
        elif self.rect.bottom >= SCREEN_HEIGHT and self.dy > 0:
            self.dy = 0

        # When the player is serving, the ball stays on the paddle
        if is_serving:
            ball.rect.x = self.rect.centerx - ball.rect.width // 2
            ball.rect.y = self.rect.top - ball.rect.height

        # Update the paddle position
        self.rect.x += self.dx
        self.rect.y += self.dy

    # Drawing the Player's racket
    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

# Defining Opponent
class Opponent():
    def __init__(self, pongSound):
        self.rect = pygame.Rect(int(SCREEN_WIDTH / 2), 25, 50, 15)
        self.pongSound = pongSound
        self.speed = 4  # Default opponent speed

    # Update movement of the opponent
    def update(self, ball):
        if self.rect.centerx > ball.rect.centerx:
            self.rect.x -= self.speed
        elif self.rect.centerx < ball.rect.centerx:
            self.rect.x += self.speed

    # Drawing the opponent's racket
    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

# Defining Game
class Game():
    def __init__(self):
        bouncePath = resource_path("assets/bounce.wav")
        pingPath = resource_path("assets/ping.wav")
        pongPath = resource_path("assets/pong.wav")
        fontPath = resource_path("assets/TimesNewRoman-Bold.ttf")
        bounceSound = pygame.mixer.Sound(bouncePath)
        pingSound = pygame.mixer.Sound(pingPath)
        pongSound = pygame.mixer.Sound(pongPath)
        self.player = Player(pingSound)
        self.ball = Ball(bounceSound)
        self.opponent = Opponent(pongSound)
        self.font_large = pygame.font.Font(fontPath, 30)
        self.font_medium = pygame.font.Font(fontPath, 25)
        self.playerScore = 0
        self.opponentScore = 0
        self.serving_player = "player"
        self.state = WINNING_SELECTION
        self.winning_goal = None
        self.difficulty = MEDIUM
        self.game_over_message = ""

    # Game Event Handler
    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if self.state == WINNING_SELECTION:
                    if self.winning_goal is None:
                        self.winning_goal = 1
                    if event.key == pygame.K_UP and self.winning_goal < 10:
                        self.winning_goal += 1
                    elif event.key == pygame.K_DOWN and self.winning_goal > 1:
                        self.winning_goal -= 1
                    elif event.key == pygame.K_RETURN and self.winning_goal is not None:
                        self.state = DIFFICULTY_SELECTION
                elif self.state == DIFFICULTY_SELECTION:
                    if event.key == pygame.K_UP:
                        self.difficulty = min(HARD, self.difficulty + 1)
                    elif event.key == pygame.K_DOWN:
                        self.difficulty = max(EASY, self.difficulty - 1)
                    elif event.key == pygame.K_RETURN:
                        self.state = SERVING
                        self.applyDifficultySettings()
                elif self.state == SERVING:
                    if event.key == pygame.K_SPACE:
                        self.ball.dx = random.choice([-3, 3])
                        self.ball.dy = -5  # Ball moves upwards after serve
                        self.state = PLAYING
                elif self.state == GAME_OVER:
                    if event.key == pygame.K_y:
                        self.resetGame()
                    elif event.key == pygame.K_n:
                        return True
                elif event.key == pygame.K_LEFT:
                    self.player.dx -= 5
                elif event.key == pygame.K_RIGHT:
                    self.player.dx += 5
                elif event.key == pygame.K_UP:
                    self.player.dy -= 5
                elif event.key == pygame.K_DOWN:
                    self.player.dy += 5
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.player.dx = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.player.dy = 0
        return False

    # Apply difficulty settings to adjust game speed and opponent behavior
    def applyDifficultySettings(self):
        if self.difficulty == EASY:
            self.opponent.speed = 2
            self.ball.dx = random.randint(-2, 2)
            self.ball.dy = 4
        elif self.difficulty == MEDIUM:
            self.opponent.speed = 4
            self.ball.dx = random.randint(-3, 3)
            self.ball.dy = 5
        elif self.difficulty == HARD:
            self.opponent.speed = 6
            self.ball.dx = random.randint(-4, 4)
            self.ball.dy = 7

    # Processing the Game Logic
    def runLogic(self):
        if self.state == PLAYING:
            self.ball.update(self.player, self.opponent)
            self.player.update(self.ball, False)
            self.opponent.update(self.ball)

            if self.ball.rect.top <= 0:
                self.playerScore += 1
                self.state = serve_ball(self.ball, self.player)
            elif self.ball.rect.bottom >= SCREEN_HEIGHT:
                self.opponentScore += 1
                self.state = serve_ball(self.ball, self.player)

            # Check for a winner
            if self.winning_goal is not None and self.playerScore == self.winning_goal:
                self.state = GAME_OVER
                self.game_over_message = "You won!"
            elif self.winning_goal is not None and self.opponentScore == self.winning_goal:
                self.state = GAME_OVER
                self.game_over_message = "You lost!"

    # Displaying Game Frame
    def displayFrame(self, screen):
        screen.fill(BLUE)
        if self.state == WINNING_SELECTION:
            self.displayWinningSelection(screen)
        elif self.state == DIFFICULTY_SELECTION:
            self.displayDifficultySelection(screen)
        elif self.state == GAME_OVER:
            self.displayMessage(screen, self.game_over_message, WHITE)
            sub_label = self.font_medium.render("Press Y to restart, N to quit", True, WHITE)
            screen.blit(sub_label, (SCREEN_WIDTH // 2 - sub_label.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
            pygame.display.update()
        else:
            self.ball.draw(screen)
            self.player.draw(screen)
            self.opponent.draw(screen)

            for x in range(0, SCREEN_WIDTH, 20):
                pygame.draw.rect(screen, WHITE, [x, SCREEN_HEIGHT / 2, 10, 10])

            opponentScoreLabel = self.font_large.render(str(self.opponentScore), True, WHITE)
            screen.blit(opponentScoreLabel, (SCREEN_WIDTH - 50, 50))
            playerScoreLabel = self.font_large.render(str(self.playerScore), True, WHITE)
            screen.blit(playerScoreLabel, (50, 50))

            pygame.display.update()

    # Display difficulty selection screen
    def displayDifficultySelection(self, screen):
        screen.fill(BLUE)
        difficulty_text = ["Easy", "Medium", "Hard"]
        label = self.font_large.render(f"Select Difficulty: {difficulty_text[self.difficulty - 1]}", True, WHITE)
        sub_label = self.font_medium.render("Press UP/DOWN to change, ENTER to start", True, WHITE)
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(sub_label, (SCREEN_WIDTH // 2 - sub_label.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        pygame.display.update()

    def displayWinningSelection(self, screen):
        screen.fill(BLUE)
        if self.winning_goal is None:
            label = self.font_large.render(f"Choose Winning Goal", True, WHITE)
        else:
            label = self.font_large.render(f"Winning Goal: {self.winning_goal}", True, WHITE)
        sub_label = self.font_medium.render("Press UP/DOWN to change, ENTER to start", True, WHITE)
        screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(sub_label, (SCREEN_WIDTH // 2 - sub_label.get_width() // 2, SCREEN_HEIGHT // 2 + 20))
        pygame.display.update()

    def displayMessage(self, screen, message, color):
        screen.fill(BLUE)
        label = self.font_large.render(message, True, color)
        posX = int((SCREEN_WIDTH / 2) - (label.get_width() / 2))
        posY = int((SCREEN_HEIGHT / 2) - (label.get_height() / 2))
        screen.blit(label, (posX, posY))
        pygame.display.update()

    def resetGame(self):
        self.playerScore = 0
        self.opponentScore = 0
        self.state = WINNING_SELECTION
        self.winning_goal = None
        self.difficulty = MEDIUM

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pingpong Game")
    clock = pygame.time.Clock()
    game = Game()
    done = False
    while not done:
        done = game.processEvents()
        game.runLogic()
        game.displayFrame(screen)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()
