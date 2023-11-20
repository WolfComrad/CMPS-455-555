import socket
from _thread import *

server = "172.17.128.1" #172.26.32.1
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(5)
print("Waiting for a connection, Server Started")

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4]), int(str[5])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4]) + "," + str(tup[5])

pos = [(460,682,0,0,0,0), (460,130,0,0,0,0), (450,130,0,0,0,0), (460,130,0,0,0,0), (450,130,0,0,0,0)]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            print(data)
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                elif player == 2:
                    reply = pos[1]
                elif player == 3:
                    reply = pos[2]
                elif player == 4:
                    reply = pos[3]
                else:
                    reply = pos[4]

                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1