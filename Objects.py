import pygame
import math
import time
import random
from stars import BackGround


def Vel(Direction='left',mag=1):
    # Vel_Down = 0
    # Vel_right = 1
    # dirr = (Vel_Down,Vel_right)
    Direction=Direction.lower()
    if Direction=='right' or Direction[0]=='r':
        return (0,mag)
    if Direction=='left' or Direction[0]=='l':
        return (0,-mag)
    if Direction=='up' or Direction[0]=='u':
        return (-mag,0)
    if Direction=='down' or Direction[0]=='d':
        return (mag,0)

class SnakeObj(object):
    """docstring for SnakeObj"""
    def __init__(
        self,
        ID=1,
        color=(0,0,0) ,  # color of SnakeObj is Black (default)
        startpoint=0,    # [0,1,2,3] 1 for top left
                         #           2 for top left
                         #           3 for top left
                         #           4 for top left
        mag=1,
        Direction=None,
        AreanaResolution=(60,60)  ##  Areana resolution
        ):
        super(SnakeObj, self).__init__()
        self.ID = ID
        self.color = color
        self.mag = mag
        self.Direction = Direction
        self.AreanaResolution=AreanaResolution
        self.startpoint=startpoint

        self.make()
        self.score = 0
        self.Dead = True

    def make(self):
        X=self.AreanaResolution[0]-1
        Y=self.AreanaResolution[1]-1
        # self.Snake = [(0,0),(0,0),(0,0)]
        # if self.startpoint==1:  # [(a1,b1),(a2,b2),(a3,b3)]
        self.Snake = [(2,0),(1,0),(0,0)]
        self.Direction = 'right'
        if self.startpoint==2:
            self.Snake = [(X-2,Y), (X-1,Y), (X,Y)]
            self.Direction = 'left'
        if self.startpoint==3:
            self.Snake = [(0,Y-2),(0,Y-1),(0,Y)]
            self.Direction = 'up'
        if self.startpoint==4:
            self.Snake = [(X,2),(X,1),(X,0)]
            self.Direction = 'down'

    def re_initialize(self):
        self.make()
        self.Dead = False
        self.score = 0

    def AdvanceThePosition(self):
        #  [(a1,b1),(a2,b2),(a3,b3)]
        #  changes to
        #  [  (a1+vx,b1+vy)     (a1,b1),(a2,b2)]  XXXX--(a3,b3)
        for i in range(self.mag):
            head       = self.Snake[0]
            Velocity  = Vel(self.Direction ,1)
            Vel_right  = Velocity[1]
            Vel_Down   = Velocity[0]
            X = (head[0]+Vel_right)%self.AreanaResolution[0]
            Y = (head[1]+Vel_Down)%self.AreanaResolution[1]
            self.Snake = [(X, Y)]+ self.Snake[:-1]

    def HitCondition(self) :
        head = self.Snake[0]
        if head in self.Snake[1:]:
            self.Dead =True
            return True
        return False

    def ChangeDirection(self,eve_key,source):
        if eve_key == source.K_LEFT:
            if self.Direction != 'right':
                self.Direction = 'left'

        elif eve_key == source.K_RIGHT:
            if self.Direction != 'left':
                self.Direction = 'right'

        elif eve_key == source.K_UP:
            if self.Direction != 'down':
                self.Direction = 'up'

        elif eve_key == source.K_DOWN:
            if self.Direction != 'up':
                self.Direction = 'down'

    def IncreaseLength(self):
        head = self.Snake[0]
        self.Snake.insert(-1, self.Snake[-1])
        self.score+=(5*self.mag)

class Game(object):
    """docstring for Game"""
    def __init__(self):
        self.pygame=pygame
        self.pygame.init()
        display_width  = 600+200 ## 800
        display_height = 600
        x_Pixels = 60
        y_Pixels = 60
        self.caption = 'Snake Game'
        self.colors={
                    'black':(0,0,0),
                    'white':(255,255,255),
                    'red':(255,0,0),
                    'green':(0,255,0),
                    'blue':(0,0,255),
                    'dead':(128,128,128),
                    'msg':(0,153,64)
        }
        self.ScreenResolution=(display_width,display_height)
        self.AreanaResolution=(x_Pixels,y_Pixels)

        self.gameDisplay = self.pygame.display.set_mode(self.ScreenResolution)
        self.pygame.display.set_caption(self.caption)
        self.clock = self.pygame.time.Clock()
        self.BackGround = BackGround( self.gameDisplay,resolution = (600,600))

    def getNewID(self):
        for snake in self.players:
            if snake.Dead:
                # snake.Dead =
                snake.re_initialize()
                return snake.ID,snake

    def initPlayers(self,num=2):
        if num>4:
            print("max players = 4")
            num=4
        self.players = []
        properties = {
                0:[(255,255,0),'left'],
                1:[(255,0,255),'right'],
                2:[(0,255,255),'up'],
                3:[(0,0  ,  255),'down']
        }

        for i in range(1,num+1):
            self.players +=[
                        SnakeObj(
                                ID = i,
                                color = properties[i-1][0],
                                # Direction=properties[i][1],
                                mag = 1,
                                AreanaResolution = self.AreanaResolution,
                                startpoint = i
                                )
            ]

    def newFood(self):
        x = random.randrange(1,self.AreanaResolution[0])
        y = random.randrange(1,self.AreanaResolution[1])
        return (x,y)

    def UpdateScreenAndScore(self):
        self.gameDisplay.fill(self.colors['white'])
        self.gameDisplay.fill(self.colors['black'],(0,0,600,600))
        self.BackGround.move_and_draw_stars()

        if hasattr(self, 'server') and hasattr(self.server,'ID'):
            ID = self.server.ID -1
            self.gameDisplay.fill(self.colors['black'],(600,(ID*100)+40,200,2))

        font = self.pygame.font.SysFont("comicsansms",30)
        for player in self.players:
            text = font.render("Player - "+str(player.ID)+"  = "+str(player.score),True,player.color)
            self.gameDisplay.blit(text,(600,(player.ID-1)*100))
            if player.Dead :
                text = font.render("--DEAD--",True,self.colors['dead'])
                self.gameDisplay.blit(text,(600+20,((player.ID-1)*100)+20))

    def CheckEvents(self):
        player = self.players[0]
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                return True
            if event.type == self.pygame.KEYDOWN:
                player.ChangeDirection(event.key,self.pygame)
        return False

    def FillPixelArray(self,array, color=(0,0,0)):
        w,h = 8,8
        for location in array:
            x,y = location[0],location[1]
            x = x*10 +1
            y = y*10 +1
            self.pygame.draw.rect(self.gameDisplay, color,(x,y,w,h))

    def checkFood(self,Snake):
        food = self.food
        head = Snake.Snake[0]
        if head==food:
            Snake.IncreaseLength()
            self.food=self.newFood()

    def game_intro(self):
        self.gameDisplay.fill(self.colors['white'])

        font = self.pygame.font.SysFont("comicsansms",60)
        text = font.render("Snake v1.0",True,(0,0,0))
        self.gameDisplay.blit(text,(200,150))

        font = self.pygame.font.SysFont("comicsansms",30)
        text = font.render("Start The Server..",True,(120,250,130))
        self.gameDisplay.blit(text,(190,350))

        text = font.render("Exit",True,(120,250,130))
        self.gameDisplay.blit(text,(510,350))

        self.pygame.display.update()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__del__()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    if(x>185 and x<310 and y>360 and y<420):
                        self.game_loop()
                        return
                    elif(x>510 and x<630 and y>360 and y<420):
                        return

    def game_loop(self):
        self.food = self.newFood()
        self.gameDisplay.fill(self.colors['white'])
        self.initPlayers(1)
        while 1:
            if self.CheckEvents():
                return
            self.UpdateScreenAndScore()
            for player in self.players:
                if player.Dead :
                    continue
                self.checkFood(player)
                player.AdvanceThePosition()
                if player.HitCondition():
                    self.endGame()
                    return
                self.FillPixelArray(player.Snake, player.color)
            self.FillPixelArray([self.food],self.colors['red'])
            self.pygame.display.update()
            self.clock.tick(7)

    def __del__(self):
        self.pygame.quit()
        print("Destructed the window")

def main():
    game = Game()
    game.game_intro()

if __name__ == '__main__':
    main()
