# distributed_lab3
A simple tcp chat server in python.
Give the port number as an argument when running the server.

<h6>To join a room:</h6>

|Client sends                                           | Server responds|
|:-------------------------------------------------------|:--------------|
|JOIN_CHATROOM: [chatroom name]<br>CLIENT_IP: [0 if TCP]<br>PORT: [0 if TCP]<br>CLIENT_NAME: [string Handle to identifier client user]|JOINED_CHATROOM: [chatroom name]<br>SERVER_IP: [IP address of chat room]<br>PORT: [port number of chat room]<br>ROOM_REF: [integer that uniquely identifies chat room on server]<br>JOIN_ID: [integer that uniquely identifies client joining]|

<h6>To leave a room:</h6>

|Client sends                                           | Server responds|
|:-------------------------------------------------------|:--------------|
|LEAVE_CHATROOM: [ROOM_REF]<br>JOIN_ID: [integer previously provided by server on join]<br>CLIENT_NAME: [string Handle to identifier client user]|LEFT_CHATROOM: [ROOM_REF]<br>JOIN_ID: [integer previously provided by server on join]|

<h6>To disconnect from the server:</h6>

|Client sends                                           | Server responds|
|:-------------------------------------------------------|:--------------|
|DISCONNECT: [0 if TCP]<br>PORT: [0 id TCP]<br>CLIENT_NAME: [string handle to identify client user]||

<h6>To send a message to a chatroom:</h6>

|Client sends                                           | Server responds|
|:-------------------------------------------------------|:--------------|
|CHAT: [ROOM_REF]<br>JOIN_ID: [integer identifying client to server]<br>CLIENT_NAME: [string identifying client user]<br>MESSAGE: [string terminated with '\n\n']|CHAT: [ROOM_REF]<br>CLIENT_NAME: [string identifying client user]<br>MESSAGE: [string terminated with '\n\n']|

<h6>Error messages will be sent from the server as:</h6>
ERROR_CODE: [integer]<br>ERROR_DESCRIPTION: [string describing error]






