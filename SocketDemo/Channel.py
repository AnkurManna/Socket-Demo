import socket
import socketHelper
import threading
import random
import time
import helper
from errorchecker import *
sampleSpace = 20
thresoldProbability = 3
thresoldErrorProne = 2
#Setting up Channel 
Timeout = 4
HEADER = 45
FORMAT = 'utf-8'
errt = [0]
PORT = 4000
HOST = socket.gethostbyname(socket.gethostname())

socketSendingToSender = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketSendingToSender.bind(('',12345))
socketSendingToSender.listen(5)
socketSendingToSender.settimeout(5)
print(f"binded to 12345")

#connection with reciever
socketSendingToReceiver = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socketSendingToReceiver.bind(('',12346))
socketSendingToReceiver.listen(5)
socketSendingToReceiver.settimeout(5)

c1, addr1 = socketSendingToSender.accept()
c2, addr2 = socketSendingToReceiver.accept()

while True:
    
    print('------------------------------------------------')
    sentData = c1.recv(1024).decode()
    print(f"{sentData} is received from sender") 
    
    if(sentData =="#"):
        c2.send(sentData.encode())
        break
   
        
    
    p1 = random.randint(0,sampleSpace)

    if(p1>=thresoldProbability):
        
        p2 = random.randint(0,sampleSpace)
        sentData = Crc(sentData,generator,no_of_bits)
        
        if p2<= thresoldErrorProne:
            print("injecting error")
            sentData = helper.injectError(sentData,errt)
        #delay
        time.sleep(1)
        c2.send(sentData.encode())
        print(f"sending frame ")
        
    else:

        print("Not sending frames")
        continue
    
    try: 
        ack = c2.recv(1024).decode()
    
    except Exception as e:
        print("Timeout ... waiting for sender to send")
        continue
    
    
    
    p2 = random.randint(0,sampleSpace)

    if(p2>=thresoldProbability):
        
        p3 = random.randint(0,sampleSpace)
        if p3<= thresoldErrorProne:
            
            errt = [1,0,3]
            #ack = helper.injectError(ack,errt)
        
        #delay
        time.sleep(1)
        
    else:

        print("")
    c1.send(ack.encode())
    
c1.close()
c2.close()  
  


    

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        #inject bit/brust error
        #add delay
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == "!DISCONNECTED":
                connecected = False
            print(f"[{addr} {msg}]")
            conn.send("Msg received".encode(FORMAT))
    
    conn.close()

#To get Channel in action
def start():
    Channel.listen()
    print(f"Channel is listening {HOST}") 
    while True:
        #conn is stored to send message through same connection
        #addr is actual address of sender/reciever
        conn , addr = Channel.accept()
        dedicated_thread = threading.Thread(target=handle_client,args=(conn,addr))
        dedicated_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1} ")





