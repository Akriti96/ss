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
        
