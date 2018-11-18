import pygame
import time
import random

pygame.init()

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('snake')
clock = pygame.time.Clock()

def newFood():
    x = random.randrange(1,60)
    y = random.randrange(1,60)
    return [[x,y]]

def Display(array, color=(0,0,0)):
    w,h = 8,8
    for location in array:
        x,y = location[0],location[1]
        x = (x-1)*10 +1
        y = (y-1)*10 +1
        pygame.draw.rect(gameDisplay, color,(x,y,w,h))

def UpdateSnake(snake,Vel_Down,Vel_right):
    newX = snake[1][0]
    newY = snake[1][1]
    loc  = [newX+Vel_right,newY+Vel_Down]
    snake.insert(1,loc)
    return snake[:-1]

def checkSnake(snake):
    head = snake[1]
    if head[0]==0 or head[0]==61 or head[1]==0 or head[1]==61:
        return True
    return False

def checkFood(snake,food,Vel_Down,Vel_right):
    head = snake[1]
    food = food[0]
    if head[1]+Vel_Down == food[1] and head[0]+Vel_right ==food[0]:
        snake[0] += 1
        snake.insert(1, food)
        food = newFood()
    else:
        food = [food]
    return snake, food

def game_loop():
    x_Pixels = 60
    y_Pixels = 60

    snake = [1, [1, 1]]

    hit = False

    Vel_Down = 0
    Vel_right = 1

    food = newFood()
    gameDisplay.fill((255, 255, 255))

    while not hit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if Vel_right==0:
                        Vel_right = -1
                        Vel_Down = 0
                elif event.key == pygame.K_RIGHT:
                    if Vel_right==0:
                        Vel_right = 1
                        Vel_Down = 0
                elif event.key == pygame.K_UP:
                    if Vel_Down==0:
                        Vel_right = 0
                        Vel_Down = -1
                elif event.key == pygame.K_DOWN:
                    if Vel_Down==0:
                        Vel_right = 0
                        Vel_Down = 1

        gameDisplay.fill((255, 255, 255))
        pygame.draw.line(gameDisplay, (0, 0, 0), (600, 0), (600, 600), 2)

        snake,food = checkFood(snake, food, Vel_Down, Vel_right)

        snake = UpdateSnake(snake, Vel_Down, Vel_right)

        hit = checkSnake(snake)

        Display(snake[1:], (0,0,0))
        Display(food, (255,0,0))

        pygame.display.update()
        clock.tick(10)


game_loop()
pygame.quit()
quit()
