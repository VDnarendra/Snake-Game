from Engine.Objects import SnakeObj,Game
import socket ,select, sys

IP_ADD = '127.0.0.1'

class GameClient(Game):
    """docstring for GameClient"""
    def __init__(self,server):
        super(GameClient, self).__init__()
        self.MyIPAddreas = socket.gethostname()
        self.server = server

    def CheckEvents(self):
        source = self.pygame
        REQ = [source.K_LEFT, source.K_RIGHT, source.K_UP, source.K_DOWN]
        keys = []
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                self.__del__()
                return 'None'
            if event.type == self.pygame.KEYDOWN:
                if event.key in REQ:
                    keys += [ event.key ]
        return keys

    def update(self,state):
        state = eval(state)
        for i,player in enumerate(self.players):
            player.Dead = state[3*i]
            player.Snake = state[(3*i)+1]
            player.score = state[(3*i)+2]
        self.food = state[-1]

    def game_loop(self):
        self.update(self.server.RECEIVE())
        self.gameDisplay.fill(self.colors['white'])
        while True:
            self.UpdateScreenAndScore()
            self.server.sendKeys()
            self.update(self.server.RECEIVE())
            for player in self.players:
                if player.Dead :
                    continue
                self.FillPixelArray(player.Snake, player.color)
            self.FillPixelArray([self.food],self.colors['red'])
            self.pygame.display.update()
            self.clock.tick(7)

class Client(object):
    """docstring for Client"""
    def __init__(self):
        super(Client, self).__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.IP_address = IP_ADD
        self.Port = 12345
        self.server.connect((self.IP_address, self.Port))
        self.game = None
        self.ID=None

    def start(self):
        msg = self.RECEIVE()
        self.ID = int(msg.split(' ')[-1])
        self.game = GameClient(self)
        self.game.initPlayers(4)
        self.SEND(' ')
        self.game.game_loop()

    def sendKeys(self):
        keys = self.game.CheckEvents()
        if 'None' not in keys:
            self.SEND(str(keys))
        else:
            self.SEND('EXIT')
            self.__del__()

    def SEND(self,msg):
        msg+='|'
        self.server.send(msg.encode())

    def RECEIVE(self):
        message= b''
        while not message.endswith(b'|'):
            message+=self.server.recv(2048)
        return message.split(b'|')[-2].decode()

    def __del__(self):

        self.server.close()

def main():
    client = Client()
    client.start()
    return

if __name__ == '__main__':
    main()
