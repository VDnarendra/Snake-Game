from Objects import SnakeObj,Game
import socket ,select,os,sys,signal
try:
    from _thread import *
except :
    from thread import *

class GameServer(Game):
    """docstring for GameServer"""
    def __init__(self,server):
        super(GameServer, self).__init__()
        self.keys = []
        self.server = server
        self.food = self.newFood()

    def CheckLocalEvents(self):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                return True
        return False

    def CheckPlayerEvents(self,player):
        for event in self.keys:
            player.ChangeDirection(event,self.pygame)

    def getState(self):
        state = []
        for player in self.players:
            if player.Dead:
                state+= [player.Dead, [],player.score]
            else:
                state+= [player.Dead, player.Snake,player.score]
        state+=[self.food]
        return state

    def game_loop(self):
        self.gameDisplay.fill(self.colors['white'])
        while True:
            if self.CheckLocalEvents():
                self.__del__()
                return
            self.UpdateScreenAndScore()
            msg = self.getState()
            self.server.broadcast(str(msg))
            for player in self.players:
                if player in self.server.list_of_clients:
                    self.server.receiveKeys(player)
                self.CheckPlayerEvents(player)
                if player.Dead :
                    continue
                player.HitCondition()
                self.checkFood(player)
                player.AdvanceThePosition()
                self.FillPixelArray(player.Snake, player.color)
            self.FillPixelArray([self.food],self.colors['red'])
            self.pygame.display.update()
            self.clock.tick(7)

class Server(object):
    """docstring for Server"""
    def __init__(self):
        super(Server, self).__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.Port = 12345
        self.server.bind(('', self.Port))
        self.server.listen(4)
        self.list_of_clients = {}
        self.game = None
        self.ID=None

    def clientthread(self, conn, addr):
        while len(self.list_of_clients)==4:
            print('Server busy')
        ID,snake = self.game.getNewID()
        self.SEND(conn,'Welcome to this Snake Game! Your ID: '+str(ID))
        self.RECEIVE(conn)
        state = self.game.getState()
        self.SEND(conn, str(state))
        self.list_of_clients[snake] = conn

    def receiveKeys(self,snake):
        conn = self.list_of_clients[snake]
        try:
            message = self.RECEIVE(conn)
            if message and 'EXIT' not in message:
                keys = eval(message)
                self.game.keys = keys
            else:
                snake.Dead = True
                print('tried',snake.ID,message)
                conn.close()
                self.__remove(conn)
                return
        except Exception as e:
            snake.Dead = True
            conn.close()
            self.__remove(conn)

    def broadcast(self, message):
        l=[]
        for player,client in self.list_of_clients.items():
            try:
                self.SEND(client, message)
            except:
                client.close()
                l+=[player]
        for i in l:
            self.__remove(i)

    def __remove(self, connection):
        if connection in self.list_of_clients:
            del self.list_of_clients[connection]

    def SEND(self,conn,msg):
        msg+='|'
        conn.send(msg.encode())

    def RECEIVE(self,conn):
        message= b''
        while not message.endswith(b'|'):
            message+=conn.recv(2048)
        return message.split(b'|')[-2].decode()

    def start(self):
        self.game = GameServer(self)
        self.game.initPlayers(4)
        start_new_thread(self.game.game_intro,())
        while True:
            conn, addr = self.server.accept()
            start_new_thread(self.clientthread,(conn,addr))

    def __del__(self):
        self.server.close()
        os.kill(os.getpid(),signal.SIGKILL)

def main():
    server = Server()
    server.start()
    return

if __name__ == '__main__':
    main()
