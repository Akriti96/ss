import socket
from threading import Thread
from tkinter import *
from tkinter import ttk

IP_ADDRESS = "127.0.0.1"
PORT = 8000
SERVER = None

bufferSize = 4096
nameEntry = None
listBox = None
chatBox  = None
labelChat = None
textMessage = None
playerName=None
fileEntry =None

def recieveMsg():
    global nameEntry,listBox,chatBox ,labelChat,textMessage,SERVER,bufferSize,fileEntry 
    while True:
        chunk= SERVER.recv(bufferSize)
        print("msg from server: ",chunk.decode("utf-8"))    
        try:
            if ('tiul' in chunk.decode() and "1.0," not in chunk.decode()):
                letter_list=chunk.decode().split(',')
                listBox.insert(letter_list[0],letter_list[0]+":"+ letter_list[1]+":"+letter_list[3]+" "+letter_list[5])
                print(letter_list[0],letter_list[1],letter_list[2],letter_list[3],letter_list[4],letter_list[5])
                print("l:: ",letter_list)
            else:
                chatBox.insert(END,"\n" +chunk.decode("utf-8"))
                chatBox.see("end")
                # print(chunk.decode("utf-8"))           
        except:
            pass
        
def sendMsg():
    global nameEntry
    global SERVER
    global fileEntry
    global chatBox
     
    msgToSend= fileEntry.get()
    SERVER.send(msgToSend.encode("utf-8"))
    chatBox.insert(END,"\n"+"You>"+msgToSend)
    chatBox.see("end")
    fileEntry.delete(0,'end')

def connectWithClient():
    global nameEntry,listBox,chatBox ,labelChat,textMessage,SERVER,bufferSize,fileEntry 
    
    # 1:Yamuna   1=0  Yamuna=1
    text=listBox.get(ANCHOR)
    print("text: ",text)
    list_item=text.split(":")
    msg="connect "+list_item[1]
    SERVER.send(msg.encode('ascii'))

def disConnectWithClient():
    global nameEntry,listBox,chatBox ,labelChat,textMessage,SERVER,bufferSize,fileEntry 
    
    # 1:Yamuna   1=0  Yamuna=1

    text=listBox.get(ANCHOR)
    print("text: ",text)
    list_item=text.split(":")
    msg="disconnect "+list_item[1]
    SERVER.send(msg.encode('ascii'))

def quitServer():
    global SERVER
    SERVER.close()

def getFileSize():
    pass

def showClientList():
    global listBox,SERVER
    listBox.delete(0,"end")
    SERVER.send("show list".encode('ascii'))
    print("show_list sent to serever")

def connectToServer():
    global SERVER,nameEntry
    clientName= nameEntry.get()
    SERVER.send(clientName.encode("utf-8"))
    print("{} is Connected to sever".format(clientName))

def openChatWindow():
    global nameEntry,listBox,chatBox,labelChat,textMessage,fileEntry
    window = Tk()
    window.title("Messenger")
    window.geometry("550x400")

    namelabel = Label(window, text="Enter your name", font=("Helvetica", 12))
    namelabel.place(x=10,y=10)

    nameEntry = Entry(window, width=20, font=("Helvetica", 12))
    nameEntry.place(x=140,y=10)
    nameEntry.focus()

    connect = Button(window, text="Connect to server", font=("Helvetica",10),command=connectToServer)
    connect.place(x=350,y=10)

    line = ttk.Separator(window,orient="horizontal")
    line.place(x=0,y=40, relwidth=1, height=0.25)

    activeuser = Label(window, text="Active Users", font=("Helvetica", 12))
    activeuser.place(x=10, y = 50)

    listBox = Listbox(window, height = 6, width=58, activestyle="dotbox", font=("Helvetica", 12))
    listBox.place(x=10,y=70)

    sc1 = Scrollbar(listBox)
    sc1.place(relheight=1, relwidth=0.02, relx = 0.98)
    sc1.config(command=listBox.yview)

    connectuser = Button(window, text="Connect to user", font=("Helvetica",10),command=connectWithClient)
    connectuser.place(x=230,y=190)

    disconnect = Button(window, text="Disconnect from User", font=("Helvetica",10),command=disConnectWithClient)
    disconnect.place(x=340,y=190)

    refresh = Button(window, text="Refresh", font=("Helvetica",10),command=showClientList)
    refresh.place(x=480,y=190)

    chatwindow = Label(window, text="Chat Window", font=("Helvetica", 12))
    chatwindow.place(x=10, y=210)
    
    chatBox = Text(window, height = 6, width=58, font=("Helvetica", 12))
    chatBox.place(x=10,y=230)

    sc2 = Scrollbar(chatBox)
    sc2.place(relheight=1, relwidth=0.02, relx = 0.98)
    sc2.config(command=chatBox.yview)

    attach = Button(window, text="Attach File and Send", font=("Helvetica",10))
    attach.place(x=10,y=350)

    fileEntry= Entry(window, width =25, font = ("Calibri",12))
    fileEntry.pack()
    fileEntry.place(x=160,y=352)
    

    send = Button(window, text="Send", font=("Helvetica",10),command=sendMsg)
    send.place(x=380,y=350)

    filePath = Label(window,text="", fg="blue", bg="yellow", font=("Helvetica",12))
    filePath.place(x=10,y=380)

    window.mainloop()

def setup():
    global SERVER, PORT, IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS,PORT))
    
    receive_thread=Thread(target=recieveMsg)
    receive_thread.start()
    
    openChatWindow()

setup()
