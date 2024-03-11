import pygame, sys, random
from config import *

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

scoreFont = pygame.font.SysFont("comicsans", 40)
textFont = pygame.font.SysFont("comicsans", 20)

white = (240, 240, 240)
yellow = (200, 200, 0)


icon = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icon)

gridWidth = width//cellSize
gridHeight = height//cellSize

clock = pygame.time.Clock()

def drawSnake(snake):
    for i in snake:
        pygame.draw.rect(screen, snakeColor, (i[0] * cellSize, i[1] * cellSize, cellSize, cellSize))
        pygame.draw.rect(screen, white, (i[0] * cellSize, i[1] * cellSize, cellSize, cellSize), 1)

def drawFood(food):
    pygame.draw.rect(screen, appleColor, (food[0] * cellSize, food[1] * cellSize, cellSize, cellSize))
    pygame.draw.rect(screen, white, (food[0] * cellSize, food[1] * cellSize, cellSize, cellSize), 1)

def generateFood(snake):
    while True:
        food = [random.randint(1, gridWidth - 2), random.randint(1, gridHeight - 2)]
        if food not in snake:
            return food

def draw_start_screen():
    screen.fill(backgroundColor)
    startText = scoreFont.render("Press SPACE to Start", 1, yellow)
    screen.blit(startText, (width//2-startText.get_width()//2, height//2-50))
    pygame.display.update()

def draw_end_screen(score, bestScore):
    screen.fill(backgroundColor)
    endText = scoreFont.render("Game Over!", 1, yellow)
    screen.blit(endText, (width // 2 - endText.get_width() // 2, height // 2 - 50))
    scoreText = textFont.render(f"Score: {score}", 1, yellow)
    screen.blit(scoreText, (width // 2 - scoreText.get_width() // 2, height // 2))
    bestScoreText = textFont.render(f"Best Score: {bestScore}", 1, yellow)
    screen.blit(bestScoreText, (width // 2 - bestScoreText.get_width() // 2, height // 2 + 30))
    pygame.display.update()


def main():

    gameState = 0

    Score = 0

    snake = [[gridWidth // 2, gridHeight // 2]]  
    snake_direction = [0, 0] 
    food = generateFood(snake)

    screen.fill(backgroundColor)

    with open("assets/snake.txt", "r") as f:
        BestScore = f.read()

    while True:
        
        clock.tick(fps)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if gameState == 0:
            draw_start_screen()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                gameState = 1

        elif gameState == 1:
        
            keys = pygame.key.get_pressed()
        
            if keys[pygame.K_UP] and snake_direction[1] != 1:
                snake_direction = [0, -1]
            if keys[pygame.K_DOWN] and snake_direction[1] != -1:
                snake_direction = [0, 1]
            if keys[pygame.K_LEFT] and snake_direction[0] != 1:
                snake_direction = [-1, 0]
            if keys[pygame.K_RIGHT] and snake_direction[0] != -1:
                snake_direction = [1, 0]
        
            new_head = [snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1]]
        
            if new_head == food:
                food = generateFood(snake)
                Score += 1
            else:
                snake.pop()
        
            if new_head[0] < 0:
                new_head[0] = gridWidth - 1
    
            if new_head[0] >= gridWidth:
                new_head[0] = 0
    
            if new_head[1] < 0:
                new_head[1] = gridHeight - 1
    
            if new_head[1] >= gridHeight:
                new_head[1] = 0
    
        
            if new_head in snake:
                gameState = 2

            snake.insert(0, new_head)

            screen.fill(backgroundColor)
            pygame.draw.rect(screen, rimColor, (0, 0, width, height), 2)

            drawSnake(snake)
            drawFood(food)

            score = scoreFont.render(f"{Score}", 1, yellow)
            screen.blit(score, (35, 30))
            scoreText = textFont.render("Score", 1, yellow)
            screen.blit(scoreText, (20, 15))
            bestScore = scoreFont.render(f"{BestScore}", 1, yellow)
            screen.blit(bestScore, (width-30-35-bestScore.get_width(), 30))
            bestScoreText = textFont.render("Best Score", 1, yellow)
            screen.blit(bestScoreText, (width-30-50-bestScoreText.get_width()/2, 15))

            pygame.display.update()

        elif gameState == 2:
            if Score > int(BestScore):
                BestScore = Score
            with open("assets/snake.txt", "w") as f:
                f.write("")
            with open("assets/snake.txt", "w") as f:
                f.write(str(BestScore))
            
            draw_end_screen(Score, BestScore)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                Score = 0
                snake = [[gridWidth // 2, gridHeight // 2]]
                snake_direction = [0, 0] 
                gameState = 0

main()