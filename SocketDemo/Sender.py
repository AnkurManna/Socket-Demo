import socket
import socketHelper
import time
import random
import helper
import errorchecker as err
FORMAT = 'utf-8'
CLIENT = "192.168.56.1"

Timeout = 4
socketSendingToChannel = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketSendingToChannel.connect(('127.0.0.1',12345))
socketSendingToChannel.settimeout(5)
def isValid(msg):
    if err.Modulo2div(msg,err.generator)==0:
        return True
    else:
        return False

def send(msg):


    

    print("------------Connection is established------------")
    print("--------------------Ready to Send ----------------")
    current = 0
    while(current < len(msg)):
        print(10*"*")
        #canSend = True
        serial = helper.serialize(msg[current])
        print(f"sending {current}th frame serial: {serial}")
        socketSendingToChannel.send(serial.encode())
        #socketSendingToChannel.send(serial.encode('utf-8'))
        #canSend = False

        if(serial=="#"):
            print("sending complete")
            break
        
        
        ack ="null"
        try:
            ack = socketSendingToChannel.recv(1024).decode()
        except Exception as e:
            print('[NO AKNO]Timeout ⌚⌚⌚..Sender needs to resend')
            continue
        
        print(ack)
        if(isValid(ack)):
            print(f"[SENT] {current}th frame has been sent ✨✨✨")
            current +=1 
        else:
            print(f"[NOT SENT] {current}th frame hasn't  been sent 😰😰😰")
            continue
        
    socketSendingToChannel.close()


print('Showing STOP AND WAIT Protocol')
framelists = helper.geninput("input.txt",3)
#print(framelists)
send(framelists)