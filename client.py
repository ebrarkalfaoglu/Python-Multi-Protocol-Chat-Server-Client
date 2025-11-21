import socket
import threading
import tkinter as tk

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #client socket creation
client.connect(("127.0.0.1", 55555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK': #if message is NICK
                client.send(nickname.encode('ascii')) #send nickname

            elif message.startswith("PMFROM:"): #if private message
                parts = message.split(' ', 2)
                sender = parts[1]
                private_message = parts[2]
                print(f"[PM from {sender}] {private_message}") #print private message 
            else:
                print(message) #print message
        except:
            print("An error occurred!")
            client.close() #close connection
            break

def write():
    while True:
        message = input(" ")
        if message.startswith("/pm"):
            try:
                parts = message.split(' ', 2) 
                target = parts[1]
                private_message = parts[2]
                final_message = f"[PM to {target}] {nickname}: {private_message}"
                client.send(final_message.encode('ascii')) #send private message

            except:
                print("Incorrect PM format. Use: /pm <nickname> <message>")
        else: 
            client.send(message.encode('ascii')) #send message


receive_thread = threading.Thread(target=receive) #thread for receiving messages
receive_thread.start()

write_thread = threading.Thread(target=write) #thread for sending messages
write_thread.start()

