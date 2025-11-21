Ebrar Kalfaoğlu
2021556040
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
<img width="671" height="211" alt="image" src="https://github.com/user-attachments/assets/979f7331-6651-41d2-ab0a-4e8c93b2e188" />

<img width="960" height="416" alt="image" src="https://github.com/user-attachments/assets/86559ac1-a39d-41ec-b466-b942a2921f54" />

<img width="957" height="396" alt="image" src="https://github.com/user-attachments/assets/fcfbf076-9c78-4346-af64-d8b16b23fb0d" />




