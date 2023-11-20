import socket, sys
from _thread import *

server = "172.22.0.1" #!My local ip
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    
s.listen(4)
print("Waiting for a connection, Server Started")

def read_pos(str):
    str = str.split(", ")
    return int(str[0], int(str[1]))

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

#* Player's starting position *#
pos = [(460,682), (460,130)] #[(460,682), (460,130)]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode()) #!increase the size if error
            pos[player] = data
            
            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received: ", data)
                print("sending: ", reply)
                
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    
    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1