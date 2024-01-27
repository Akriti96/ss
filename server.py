import socket
from threading import Thread
from tkinter import *
from tkinter import ttk
import time

IP_ADDRESS = "127.0.0.1"
PORT = 8000
SERVER = None
Buffer_size=4096


# client = ip_ad + port 
clients={}

def removeClient(client_name):
    try:
        if client_name in clients:
            del clients[client_name]
   
    except KeyError:
        pass
    
def sendTextMessage(client_name,message):
    global clients
    
    other_client_name= clients["client_name"]["connected_with"]
    # other client ip_ad and port
    other_client_socket=clients[other_client_name]["client"]
    final_message=client_name + " > "+ message
    other_client_socket.send(final_message.encode("utf-8"))
    
    
def handleErrorMessage(client):
    messgae='''
    You need to connect with one of the client first to chat or share files, Click on referesh to see all avaialble users
    '''
    client.send(messgae.encode("utf-8"))

def handleShowLists(client):
    global clients
    counter = 0
    for c in clients:
        # print(c)
        counter +=1
        client_address = clients[c]["address"][0]
        connected_with = clients[c]["connected_with"]
        message =""
        if(connected_with):
            message = f"{counter},{c},{client_address}, connected with {connected_with},tiul,\n"
        else:
            message = f"{counter},{c},{client_address}, Available,tiul,\n"
        client.send(message.encode())
        time.sleep(1)
        
def  handleClientConnection(message,client,client_name):
    global clients,Buffer_size
    print("message: ",message)
    entered_client_name=message[8:].strip()
    if (entered_client_name in clients):
        if(not clients[client_name]["connected_with"]):
            clients[entered_client_name]["connected_with"]=client_name
            clients[client_name]["connected_with"]=entered_client_name
            
            other_client_socket=clients[entered_client_name]["client"]
            greet_Msg= f"hello, {entered_client_name} {client_name} connected with you"
            other_client_socket.send(greet_Msg.encode("utf-8"))
            
            #still pending
            msg = f"You are successfully connected with {entered_client_name}"
            client.send(msg.encode())
            
        else:
            other_client_name = clients[client_name]["connected_with"]
            msg = f"You are already connected with {other_client_name}"
            client.send(msg.encode())   
            
def  handleClientDisConnect(message,client,client_name):
    #still pending
   print("message: ",message)
   global clients
   entered_client_name = message[11:].strip()
   if(entered_client_name in clients):
        clients[entered_client_name]["connected_with"] = ""
        clients[client_name]["connected_with"]  = ""

        other_client_socket = clients[entered_client_name]["client"]

        greet_message = f"Hello, {entered_client_name} you are successfully disconnected with {client_name} !!!"
        other_client_socket.send(greet_message.encode())

        msg = f"You are successfully disconnected with {entered_client_name}"
        client.send(msg.encode())
                        
        
def handleMessages(client,message,client_name):
    # print("message: ",message)
    if(message == 'show list'):
        handleShowLists(client)
    elif (message[:7] == "connect"):
        handleClientConnection(message,client,client_name)
    elif (message[:10] == 'disconnect'):
        handleClientDisConnect(message,client,client_name)
    else:
        connected= clients[client_name]["connected_with"]
        # print("c:",connected)
        if(connected):
            sendTextMessage(client_name,message)
        else:
            handleErrorMessage(client)
    
def handleClient(client,client_name):
    global clients, SERVER,Buffer_size
    welMsg="Welcome, You are now connected to server\nClick on Refersh button to get all client list\n"
    client.send(welMsg.encode())
    while True:
        try:
            Buffer_size=clients[client_name]["file_size"]
            chunk= client.recv(Buffer_size)
            message= chunk.decode().strip().lower()
            print("Msg from client:  ",message)
            # print("messages:  ",message)
            if(message):
                handleMessages(client,message,client_name)
            else:
                removeClient(client_name)
                  
        except:
            pass

def acceptConnections():
    global SERVER
    global clients,Buffer_size
    
    while True:
        client,addr= SERVER.accept()
        client_name= client.recv(Buffer_size).decode().lower()
        clients[client_name]={
            "client":client,
            "address":addr,
            "connected_with":"",
            "file_name":"",
            "file_size":4096,
        }
        # print(f"Conncetion is built with {client_name}")
        print("Data of Clients:   ",clients)
        thread= Thread(target=handleClient,args=(client,client_name))
        thread.start()
        
        
def setup():
    global SERVER, PORT, IP_ADDRESS
    print("Server started...")

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS,PORT))

    SERVER.listen()
    
    acceptConnections()

setup()