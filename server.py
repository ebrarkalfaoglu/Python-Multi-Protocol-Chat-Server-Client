import socket
import threading
import random
import http.server
import socketserver
import asyncio
import websockets
import csv
import datetime
import time


host = '127.0.0.1' #localhost
port =  55555


server =socket.socket(socket.AF_INET, socket.SOCK_STREAM) #internet socket
server.bind((host,port)) #binding host and port
server.listen() #listening for connections

clients = [] #list of clients
nicknames = [] #list of nicknames
message_count = 0 #message counter
connection_count = 0 #connection counter
last_message_time = {} #dictionary to track last message time per client

def check_rate_limit(nickname):
    now = time.time()
    if nickname in last_message_time:
        if now - last_message_time[nickname] < 1:  # 1 second rate limit
            return True
    last_message_time[nickname] = now
    return False

def monitoring():
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #current timestamp
        print("\nSERVER STATUS")
        print(f"Time: {now}")
        print(f"Active Connections: {connection_count}")
        print(f"Messages Processed: {message_count}\n")
        time.sleep(60) #wait for 60 seconds

def log_message(sender, recipient, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #current timestamp
    with open("chat_log.csv", "a", newline='', encoding = "ascii") as file:
        writer = csv.writer(file) #CSV writer
        writer.writerow([timestamp, sender, recipient, message])

def client_list(): #function to print client list
    if nicknames:
        user_list = ", ".join(nicknames)
    else:
        user_list = ""   
    message = f"Client_List {user_list}".encode('ascii')
    for client in clients:  
        try:
            client.send(message) #sending client list to all clients
        except:
            pass   

def http_server(): #HTTP server function
    http_port = 8080 #HTTP server port
    handler = http.server.SimpleHTTPRequestHandler 
    with socketserver.TCPServer(("", http_port), handler) as httpd:
        print(f"HTTP server running at http://localhost:{http_port}")
        httpd.serve_forever() #running HTTP server

async def websocket_handler(websocket, path): #WebSocket handler function 
    await websocket.send("Connected to WebSocket server!") #sending message to client
    async for message in websocket:
        print(f"[WebSocket] Received: {message}")
        await websocket.send(f"Echo: {message}") #echoing received message

def websocket_server(): #WebSocket server function
    websocket_port = 8765 #WebSocket server port
    print(f"[WebSocket] Server is listening on port {websocket_port}")

    async def start():
        async with websockets.serve(websocket_handler, "0.0.0.0", websocket_port):
            await asyncio.Future()  # Sonsuza kadar çalıştır

    asyncio.run(start())

def control_nickname(nickname): #controling nickname uniqueness
    original = nickname
    if nickname.startswith("*"):
        nickname = nickname[1:]  # Remove leading asterisk

    while nickname in nicknames:
        suffix = random.randint(100, 999)
        nickname = f"{original}{suffix}"
    return nickname
   

def broadcast(message, sender_nick = "SERVER"): #broadcast message to all clients
    global message_count
    message_count += 1
    text = message.decode('ascii')
    log_message(sender_nick, "ALL", text) #logging broadcast message
    for client in clients:
        client.send(message)

def send_private(sender_nick, target_nick, message): #sending private message
    global message_count
    message_count += 1
    if target_nick not in nicknames:
        sender = clients[nicknames.index(sender_nick)]
        sender.send(f"User {target_nick} not found.".encode('ascii'))
        return
    target = clients[nicknames.index(target_nick)]
    private_message = f"[Private] {sender_nick}: {message}"
    log_message(sender_nick, target_nick, message) #logging private message
    target.send(private_message.encode('ascii')) 

def type_message(client, message, sender_nick): #determining message type
    global message_count
    message_count += 1
    if check_rate_limit(sender_nick):
        warning = "[Server]: You are sending messages too quickly. Please wait a moment.".encode('ascii')
        client.send(warning)
        return
    
    message = message.decode('ascii')

    if message.lower().strip() in ["exit", "/exit"]:
        remove_client(client)
        return
    
    if message.startswith("/pm "):
        try:
            parts = message.split(' ', 2)
            target_nick = parts[1]
            text = parts[2]
            send_private(sender_nick, target_nick, text)
        except:
            client.send("[Server]: /pm nickname message".encode('ascii'))
            return
    log_message(sender_nick, "ALL", message) #logging message
    broadcast(f"{sender_nick}: {message}".encode('ascii'), sender_nick)       

def remove_client(client): #removing client from lists
    global connection_count
    if client in clients:
        index = clients.index(client)
        nickname = nicknames[index]
        clients.remove(client)
        nicknames.remove(nickname)
        client.close()
        connection_count -= 1

        log_message(nickname, "SERVER", "left the chat") #logging client leaving
        broadcast(f"{nickname} left the chat.".encode('ascii'))
        

def handle(client): #handling messages from clients
    while True:
        try:
            message = client.recv(1024)
            sender_nick = nicknames[clients.index(client)]
            type_message(client, message, sender_nick)  
        except:
            index = clients.index(client)
            clients.remove(client)  #removing client
            client.close()  #closing connection
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode('ascii')) #broadcasting that client has left
            nicknames.remove(nickname) #removing nickname
            break

def receive(): #listening function
    global connection_count
    while True:    
        client, address = server.accept() #accepting connection
        print(f"Connected with {str(address)}")
        connection_count += 1

        client.send('NICK'.encode('ascii')) #requesting nickname
        nickname = client.recv(1024).decode('ascii')

        nickname = control_nickname(nickname) #controlling nickname uniqueness
        nicknames.append(nickname) #adding nickname to list
        clients.append(client) #adding client to list

        print(f"Nickname of the client is {nickname}") 
        log_message(nickname, "SERVER", "joined the chat") #logging client joining 
        broadcast(f"{nickname} joined the chat!".encode('ascii')) #broadcasting that client has joined
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,)) #thread for handling client
        thread.start()

if __name__ == "__main__":
    threading.Thread(target=receive, daemon=True).start()
    threading.Thread(target=http_server, daemon=True).start()
    threading.Thread(target=websocket_server, daemon=True).start()

    print("All servers are running...")
    while True:
        time.sleep(1)
