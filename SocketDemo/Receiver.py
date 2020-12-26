import socket
import socketHelper
import time
import random
import helper
import errorchecker as err
from Frame import *

Timeout = 4
FORMAT = "utf-8"

socketSendingToChannel = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketSendingToChannel.connect(('127.0.0.1',12346))
socketSendingToChannel.settimeout(5)
def receive():

    txt = []
    while True:
        print(10*"*")
        #trying to recv message from channel
        try:
            frame = socketSendingToChannel.recv(256).decode()
            if frame =="#":
                break
        except Exception as e:
            print('Nothing received')
            continue
        
        #checking error
        if(frame=='#' or err.Modulo2div(frame,err.generator)==0):
            ack = Frame("10101010","3","2")
            
            frame = frame[:-1]
            frame += '\n'
            txt.append(frame)
            print(f"[RECEIVED] message is {frame} which is fine 🤩🤩🤩")
        else:
            print(f"[RECEIVED] message is {frame} which is corrupted 😥😥😥")
            ack = Frame("10101011","3","2")

        
        ack = helper.serialize(ack)
        socketSendingToChannel.send(ack.encode())

        if frame =="#":
            break
    

        print(10*"*")
    with open('output.txt','w') as out:
        out.writelines(txt)
    socketSendingToChannel.close()

receive()