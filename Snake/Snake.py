import pygame
import sys
import random
from time import sleep

# Screen settings
screenWidth = 800
screenHeight = 600

# Scoreboard grid configuration
gridSize = 20
gridWidth = screenWidth // gridSize
gridHeight = screenHeight // gridSize

# Movement directions for the snake
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Defining colors
WHITE = (255, 255, 255)  # Text color
GREEN = (0, 255, 0)      # Start/restart button color
RED = (255, 0, 0)        # Game Over text color
BLACK = (0, 0, 0)        # Background color
BLACK_BORDER = (0, 0, 0) # Button border color

# Snake class handling the snake's properties and behaviors
class Snake:
    def __init__(self):
        # Create the initial snake state
        self.createSnake()

    # Create the snake with initial position and direction
    def createSnake(self):
        self.length = 2
        # Store the position as a list of tuples (x, y)
        self.positions = [(int(screenWidth / 2), int(screenHeight / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    # Control snake's movement direction
    def controlSnake(self, xy):
        # Prevent the snake from reversing into itself
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
        else:
            self.direction = xy

    # Move the snake and check for collisions
    def moveSnake(self):
        currentPosition = self.positions[0]
        newPosition = (currentPosition[0] + (self.direction[0] * gridSize), currentPosition[1] + (self.direction[1] * gridSize))

        # If the snake collides with itself, reset the game
        if len(self.positions) > 2 and newPosition in self.positions[2:]:
            return True  # Snake hits itself, game over

        # If the snake escapes the game area, reset the game
        elif newPosition[0] < 0 or newPosition[0] >= screenWidth or newPosition[1] < 0 or newPosition[1] >= screenHeight:
            return True  # Snake goes out of bounds, game over

        # Normal snake movement
        else:
            self.positions.insert(0, newPosition)
            if len(self.positions) > self.length:
                self.positions.pop()
        return False

    # Increase the snake's length when it eats food
    def eatFood(self):
        self.length += 1

    # Draw the snake on the screen
    def drawSnake(self, screen):
        red, green, blue = 50 / (self.length - 1), 150, 150 / (self.length - 1)
        for i, position in enumerate(self.positions):
            color = (100 + red * i, green, blue * i)
            rect = pygame.Rect((position[0], position[1]), (gridSize, gridSize))
            pygame.draw.rect(screen, color, rect)

# Feed class handling the food properties and behaviors
class Feed:
    def __init__(self):
        self.position = (0, 0)
        self.color = GREEN
        self.createFeed()

    # Create new food in a random position
    def createFeed(self):
        x = random.randint(0, gridWidth - 1)
        y = random.randint(1, gridHeight - 1)
        self.position = x * gridSize, y * gridSize

    # Draw the food on the screen
    def drawFeed(self, screen):
        rect = pygame.Rect((self.position[0], self.position[1]), (gridSize, gridSize))
        pygame.draw.rect(screen, self.color, rect)

# Game class handling the overall game logic and display
class Game:
    def __init__(self):
        self.state = 0  # 0 = Initial Start, 1 = Playing, 2 = Game Over, 3 = Restart
        self.resetGame()  # Initialize game objects

    # Reset the game by re-creating the snake and feed
    def resetGame(self):
        self.snake = Snake()
        self.feed = Feed()
        self.speed = 5

    # Display the initial start screen
    def showInitialScreen(self, screen):
        font = pygame.font.SysFont('FixedSys', 60, True)
        titleText = font.render("Play Snake's Adventure!", True, WHITE)
        titleRect = titleText.get_rect(center=(screenWidth / 2, screenHeight / 2 - 100))

        # Create button with "Start" text
        startText = font.render("Start", True, WHITE)
        textRect = startText.get_rect(center=(screenWidth / 2, screenHeight / 2 + 50))
        buttonRect = pygame.Rect(0, 0, textRect.width + 40, textRect.height + 20)
        buttonRect.center = (screenWidth / 2, screenHeight / 2 + 50)

        # Fill background with black
        screen.fill(BLACK)

        # Draw the title and start button
        screen.blit(titleText, titleRect)
        pygame.draw.rect(screen, GREEN, buttonRect)
        pygame.draw.rect(screen, BLACK_BORDER, buttonRect, 4)
        screen.blit(startText, textRect)
        pygame.display.update()

        # Wait for mouse click to start the game
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = event.pos
                    if buttonRect.collidepoint(mousePos):
                        waiting = False  # Exit loop and start the game
                        self.state = 1  # Switch to playing state

    # Display the restart screen after game over
    def showRestartScreen(self, screen):
        font = pygame.font.SysFont('FixedSys', 60, True)
        buttonText = font.render("Restart", True, WHITE)
        textRect = buttonText.get_rect(center=(screenWidth / 2, screenHeight / 2 + 50))

        # Create a button rectangle with padding around the text
        buttonRect = pygame.Rect(0, 0, textRect.width + 40, textRect.height + 20)
        buttonRect.center = (screenWidth / 2, screenHeight / 2 + 50)

        # Create a message text for restart confirmation
        font_small = pygame.font.SysFont('FixedSys', 40)
        messageText = font_small.render("Do you want to restart the game?", True, WHITE)
        messageRect = messageText.get_rect(center=(screenWidth / 2, screenHeight / 2 - 50))

        # Draw the black screen background
        screen.fill(BLACK)

        # Blit the message text and button
        screen.blit(messageText, messageRect)
        pygame.draw.rect(screen, GREEN, buttonRect)
        pygame.draw.rect(screen, BLACK_BORDER, buttonRect, 4)
        screen.blit(buttonText, textRect)
        pygame.display.update()

        # Wait for mouse click to restart the game
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = event.pos
                    if buttonRect.collidepoint(mousePos):
                        waiting = False  # Exit loop and restart the game
                        self.resetGame()  # Reset the game
                        self.state = 1  # Switch to playing state

    # Display the game over screen
    def showGameOver(self, screen):
        font = pygame.font.SysFont('FixedSys', 60, True)
        gameOverText = font.render("Game Over", True, RED)
        textRect = gameOverText.get_rect(center=(screenWidth / 2, screenHeight / 2))

        # Fill the screen with black and show "Game Over" text
        screen.fill(BLACK)
        screen.blit(gameOverText, textRect)
        pygame.display.update()
        sleep(3)  # Wait for 3 seconds before showing restart option

        # Show restart screen
        self.state = 3  # Go to the restart screen after game over

    # Handle events like quitting or key presses
    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.controlSnake(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.controlSnake(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.controlSnake(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.controlSnake(RIGHT)
        return False

    # Update the game state
    def runLogics(self):
        gameOver = self.snake.moveSnake()
        self.checkEat(self.snake, self.feed)
        self.speed = min(20, 10 + self.snake.length / 2)
        return gameOver

    # Check if the snake has eaten the food
    def checkEat(self, snake, feed):
        if snake.positions[0] == feed.position:
            snake.eatFood()
            feed.createFeed()

    # Display game info such as snake length and speed
    def drawInfo(self, length, speed, screen):
        info = "Length: " + str(length) + "    " + "Speed: " + str(round(speed, 2))
        font = pygame.font.SysFont('FixedSys', 30, False, False)
        textObj = font.render(info, True, WHITE)
        textRect = textObj.get_rect()
        textRect.x, textRect.y = 10, 10
        screen.blit(textObj, textRect)

    # Display the current game frame
    def displayFrame(self, screen):
        screen.fill(WHITE)
        self.drawInfo(self.snake.length, self.speed, screen)
        self.snake.drawSnake(screen)
        self.feed.drawFeed(screen)
        pygame.display.update()

    # Main game loop
    def main(self):
        pygame.init()
        pygame.display.set_caption('Snake Game')
        screen = pygame.display.set_mode((screenWidth, screenHeight))
        clock = pygame.time.Clock()

        while True:
            if self.state == 0:  # Show initial start screen
                self.showInitialScreen(screen)
            elif self.state == 1:  # Playing state
                if self.processEvents():  # Quit event
                    break
                if self.runLogics():  # Snake collision (Game Over)
                    self.state = 2
                self.displayFrame(screen)
                clock.tick(self.speed)
            elif self.state == 2:  # Game Over state
                self.showGameOver(screen)
            elif self.state == 3:  # Restart screen
                self.showRestartScreen(screen)

        pygame.quit()

# Run the game
if __name__ == '__main__':
    Game().main()
