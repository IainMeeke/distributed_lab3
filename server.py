import hashlib
import socket
import sys
from threading import Thread
from Queue import Queue
import os

HOST = '' #host becomes any address the machine happens to have
PORT = int(sys.argv[1]) #get the port from the command line arguments and convert to int
STUDENT_ID = '39e95f0efebef82542626bd6c3c28765726768817d45d38b2d911b26eb5d0b37'
POOL_SIZE = 20


class Worker(Thread):
    """individual thread that handles the clients requests"""
    def __init__(self, tasks,messageParser):
        Thread.__init__(self)
        self.tasks = tasks #each task will be an individual connection
        self.messageParser = messageParser
        self.daemon = True
        self.start()

    def run(self):
        #run forever
        while True:
            conn = self.tasks.get() #take a connection from the queue
            self.messageParser(conn)


class ThreadPool:
    """pool of worker threads all consuming tasks"""
    def __init__(self,num_thread,chat_server):
        self.tasks = Queue(num_thread)
        self.chat_server = chat_server
        for _ in range(num_thread):
            Worker(self.tasks,chat_server.messageParser)

    def add_tasks(self, conn):
        #put a new connection on the queue
        self.tasks.put((conn))


class ChatServer:
    """a chat server with several chat rooms"""

    def __init__(self,port,num_thread):
        self.users_in_rooms = {} #stores all rooms and the clients in those rooms [RoomId : [clientId,clientId1.....]]
        self.rooms = {}
        self.users = {} #keeps a list of all users who have used the chatserver in form [JoinID:Name]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((HOST,port))
        except socket.error , msg:
            print 'binding failed, error: ' + str(msg[0])
            sys.exit()
        print 'succesful bind'
        #init a thread pool:
        self.pool = ThreadPool(num_thread,self)

    def listen(self):
        self.socket.listen(5)
        print 'listening now'

        #keep the server alive
        while True:
            connection, addr = self.socket.accept() #blocking call to wait for a connection
            print 'connected with ' + addr[0] + ' port: ' + str(addr[1])
            self.pool.add_tasks(connection)

    def messageParser(self,conn):
        while conn:
            data = conn.recv(2048)
            if data == "KILL_SERVICE\n":
                os._exit(0)

            elif data.startswith("JOIN_CHATROOM") and data.endswith("\n"):
                reply = self.joinRoom(data,conn)

            else:
                reply = ''#any other message

            conn.sendall(reply)
        self.tasks.task_done()

    def joinRoom(self,data,conn):
        text = data.splitlines()
        room_name = text[0].split(":")[1]
        client_name = text[3].split(":")[1]
        room_id = int(hashlib.md5(room_name).hexdigest(), 16)
        client_id  = int(hashlib.md5(client_name).hexdigest(), 16)

        if client_id not in self.users:
            self.users[client_id] = client_name

        if room_id not in self.users_in_rooms:
            self.users_in_rooms[room_id] = {}
            self.rooms[room_id] = room_name

        self.users_in_rooms[room_id][client_id] = conn


        return "JOINED_CHATROOM: " + str(room_name) + "\n" +"SERVER_IP: iainmeeke.xyz\nPORT: "+str(PORT)+"\nROOM_REF: "+str(room_id)+"\nJOIN_ID: "+str(client_id)+"\n"









def main():
    server = ChatServer(PORT,POOL_SIZE)
    server.listen()

if __name__ == "__main__":
    main()



