let chatSocket = null;

function connect() {
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/");

    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket.");
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data);

    switch (data.type) {
    // ...
    case "user_list":
        for (let i = 0; i < data.users.length; i++) {
            onlineUsersSelectorAdd(data.users[i]);
        }
        break;
    case "user_join":
        chatLog.value += data.user + " joined the room.\n";
        onlineUsersSelectorAdd(data.user);
        break;
    case "user_leave":
        chatLog.value += data.user + " left the room.\n";
        onlineUsersSelectorRemove(data.user);
        break;
    // scroll 'chatLog' to the bottom
    chatLog.scrollTop = chatLog.scrollHeight;
};


    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}
connect();
chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) return;
    chatSocket.send(JSON.stringify({
        "message": chatMessageInput.value,
    }));
    chatMessageInput.value = "";
};