import pygame
import os
import sys
import random

# SCREEN WIDTH and SCREEN HEIGHT
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700

# Defining Colors
WHITE = (255, 255, 255)
SEA = (80, 180, 220)
GROUND = (140, 120, 40)
DARK_GROUND = (70, 60, 20)
RED = (255, 0, 0)

FPS = 60

# Global function to get the resource path
def resourcePath(relativePath):
    try:
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(os.path.dirname(__file__))  # Updated to the OrcasRush folder
    return os.path.join(basePath, relativePath)

# Defining Fish object
class Fish:
    def __init__(self):
        self.image = pygame.image.load(resourcePath('assets/orca.png'))
        self.sound = pygame.mixer.Sound(resourcePath('assets/swim.wav'))
        self.rect = self.image.get_rect()
        self.width = self.image.get_rect().width
        self.height = self.image.get_rect().height

    def reset(self):
        self.rect.x = 250
        self.rect.y = 250
        self.dx = 0
        self.dy = 0

    def swim(self):
        self.dy = -10
        self.sound.play()

    def update(self):
        # Apply gravity
        self.dy += 0.5
        if self.dy > 10:  # Limit falling speed
            self.dy = 10
        self.rect.y += self.dy

        # Prevent fish from going above the screen
        if self.rect.y <= 0:
            self.rect.y = 0

        # If the fish hits the bottom, trigger game over
        if self.rect.y + self.height >= SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - self.height
            self.dy = 0
            return True  # Game over

        return False  # No game over

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Defining Pipe Object
class Pipe:
    def __init__(self, difficulty_gap=200):
        """
        difficulty_gap: Defines the distance between the upper and lower pipes.
        """
        self.pipe_image = pygame.image.load(resourcePath('assets/pipe01.png'))
        self.pipe_rect_top = self.pipe_image.get_rect()
        self.pipe_rect_bottom = self.pipe_image.get_rect()
        self.gap_size = difficulty_gap  # The distance between the top and bottom pipes

        self.setPos()

    def setPos(self):
        # Random height for top pipe, bottom pipe will be calculated based on this height and gap_size
        pipe_height = random.randint(100, SCREEN_HEIGHT - self.gap_size - 100)

        # Setting positions for top and bottom pipes
        self.pipe_rect_top.x = SCREEN_WIDTH
        self.pipe_rect_top.y = pipe_height - self.pipe_rect_top.height

        self.pipe_rect_bottom.x = SCREEN_WIDTH
        self.pipe_rect_bottom.y = pipe_height + self.gap_size

    def update(self):
        # Move the pipes to the left
        self.pipe_rect_top.x -= 4
        self.pipe_rect_bottom.x -= 4

    def outOfScreen(self):
        return self.pipe_rect_top.x + self.pipe_rect_top.width <= 0

    def checkCollision(self, fish):
        # Check collision with top and bottom pipes
        if self.pipe_rect_top.colliderect(fish.rect) or self.pipe_rect_bottom.colliderect(fish.rect):
            return True
        return False

    def draw(self, screen):
        # Draw the top and bottom pipes
        screen.blit(self.pipe_image, self.pipe_rect_top)
        screen.blit(self.pipe_image, self.pipe_rect_bottom)

# Defining Game Object
class Game:
    def __init__(self):
        self.font_large = pygame.font.SysFont("FixedSys", 50, True, False)
        self.font_medium = pygame.font.SysFont("FixedSys", 40, True, False)
        pygame.mixer.music.load(resourcePath('assets/bgm.mp3'))
        self.fish = Fish()
        self.pipes = [Pipe(difficulty_gap=200)]  # Initial difficulty gap
        self.pipe_spawn_distance = 300  # Distance for spawning new pipes
        self.distance_since_last_pipe = 0  # Tracks distance covered since last pipe was added
        self.score = 0
        self.best_score = 0  # Tracks the best score
        self.menuOn = True
        self.gameOver = False

    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if self.menuOn or self.gameOver:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.play(-1)
                        self.score = 0
                        self.menuOn = False
                        self.gameOver = False
                        self.fish.reset()
                        self.pipes = [Pipe(difficulty_gap=200)]  # Reset pipes for new game
                        self.distance_since_last_pipe = 0  # Reset pipe distance
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.fish.swim()
        return False

    def runLogic(self):
        if not self.menuOn and not self.gameOver:
            if self.fish.update():  # If fish hits the bottom, trigger game over
                pygame.mixer.music.stop()
                self.gameOver = True
                if self.score > self.best_score:  # Update best score if new high score
                    self.best_score = self.score

            self.distance_since_last_pipe += 4  # Increment the distance covered by pipes
            if self.distance_since_last_pipe >= self.pipe_spawn_distance:
                self.pipes.append(Pipe(difficulty_gap=random.randint(180, 300)))  # Add pipe with random gap size
                self.distance_since_last_pipe = 0  # Reset distance tracker
                self.score += 1  # Increase score after new pipe appears

            for pipe in self.pipes:
                pipe.update()
                if pipe.outOfScreen():
                    self.pipes.remove(pipe)  # Remove pipes that go off-screen to free memory
                if pipe.checkCollision(self.fish):
                    pygame.mixer.music.stop()
                    self.gameOver = True
                    if self.score > self.best_score:
                        self.best_score = self.score

    def drawText(self, screen, text, font, x, y, color):
        textObj = font.render(text, True, color)
        textRect = textObj.get_rect()
        textRect.center = (x, y)
        screen.blit(textObj, textRect)

    def displayMenu(self, screen):
        screen.fill(SEA)
        centerX = SCREEN_WIDTH // 2
        centerY = SCREEN_HEIGHT // 2
        self.drawText(screen, "Press Space Key to Start", self.font_large, centerX, centerY, DARK_GROUND)
        pygame.display.update()

    def displayGameOver(self, screen):
        screen.fill(SEA)
        centerX = SCREEN_WIDTH // 2
        centerY = SCREEN_HEIGHT // 2
        self.drawText(screen, "Game Over!", self.font_large, centerX, centerY - 50, RED)
        self.drawText(screen, f"Score: {self.score}, Best: {self.best_score}", self.font_medium, centerX, centerY + 50, WHITE)
        self.drawText(screen, "Press Space to Play Again", self.font_medium, centerX, centerY + 150, WHITE)
        pygame.display.update()

    def displayFrame(self, screen):
        screen.fill(SEA)
        pygame.draw.rect(screen, GROUND, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
        pygame.draw.line(screen, DARK_GROUND, (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 4)
        self.fish.draw(screen)
        for pipe in self.pipes:
            pipe.draw(screen)
        self.drawText(screen, "Score: " + str(self.score), self.font_medium, 100, 50, WHITE)
        pygame.display.update()

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Orca's Rush")
    clock = pygame.time.Clock()
    game = Game()
    done = False
    while not done:
        done = game.processEvents()
        if game.menuOn:
            game.displayMenu(screen)
        elif game.gameOver:
            game.displayGameOver(screen)
        else:
            game.runLogic()
            game.displayFrame(screen)
            clock.tick(FPS)
    pygame.quit()

if __name__ == '__main__':
    main()
