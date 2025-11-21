# Python-Multi-Protocol-Chat-Server-Client

This project provides a **multi-user**, **multi-protocol**, real-time chat system built in Python.  
It includes:

- A **TCP Chat Server**
- An **HTTP Server** (for serving logs & static files)
- A **WebSocket Server** (for real-time monitoring)
- A **console-based TCP Client**

All servers run simultaneously and work together.

---

## 📌 Features

### ✅ TCP Chat Server
- Multi-user communication  
- Nickname validation (automatic conflict resolution)  
- Global broadcast messages  
- Private messaging using: `/pm <nickname> <message>`  
- Join/leave notifications  
- Rate limiting (prevents sending messages faster than 1 per second)  
- Message & event logging to **CSV**  
- Real-time server monitoring (active connections, message count)  

---

### 🌐 HTTP Server (Port 8080)
- Serves `chat_log.csv` and other static files  
- Useful for viewing logs in the browser  

---

### 🔌 WebSocket Server (Port 8765)
- Real-time monitoring interface  
- Echo-style message response (extendable)  

---

### 🖥️ Client Application
- Console-based chat client  
- Sends/receives global messages  
- Private messaging support  
- Nickname selection  
- Error handling  

---

### ScreenShots
! ![description](image.png)



