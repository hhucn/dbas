// Tobias Krauthoff

// npm install socket.io
// npm install --save express

var port = 3000;
var time = 10000;
var clients = {};

var express = require('express');
var app = express();

var http = require('http');
var https = require('https');
var server = http.createServer(app);

server.listen(port);
var io = require('socket.io').listen(server);

app.get('/', function(req, res){
    res.sendFile(__dirname + '/index.html');
});

io.sockets.on('connection', function(socket){
    logMessage('user ' + socket.id + ' connected');
    sendStatusMessage(socket, 'chat_message', 'user ' + socket.id + ' connected');
    addClient(socket);

    socket.on('disconnect', function(){
        removeClient(socket);
        logMessage('user ' + socket.id + ' disconnected');
        sendStatusMessage(socket, 'chat_message', 'user ' + socket.id + ' disconnected');
    });

    socket.on('chat_message', function(msg){
        logMessage('emitting message: ' + msg);
        sendMessage(socket, 'chat_message', msg);
    });
});

sendMessage = function(socket, key, msg){
    var time = new Date().today() + ' ' + new Date().timeNow();
    var span_time = '<span class="time">(' + time + ')</span> ';
    var span_id = '<span class="id">' + socket.id + '</span>: ';
    var span_msg = '<span class="msg">' + msg + '</span>';
    for (var socket_id in clients) {
        clients[socket_id].emit(key, span_time + span_id + span_msg);
    }
};

sendStatusMessage = function(socket, key, msg){
    var time = new Date().today() + ' ' + new Date().timeNow();
    var span= '<span class="status">(' + time + ') ' +  msg + '</span>';
    for (var socket_id in clients) {
        clients[socket_id].emit(key, span);
    }
};

logMessage = function(msg){
    var time = new Date().today() + ' ' + new Date().timeNow();
    console.log(time + ' ' + msg);
};

addClient = function(socket){
    clients[socket.id] = socket;
    logMessage('Added ' + socket.id + ' into dict');
};

removeClient = function(socket){
    delete clients[socket.id];
    logMessage('Removed ' + socket.id + ' into dict');
};

// For todays date;
Date.prototype.today = function () {
    return ((this.getDate() < 10)?"0":"") + this.getDate() + "."
        + (((this.getMonth()+1) < 10)?"0":"") + (this.getMonth()+1) + "."
        + this.getFullYear();
};

// For the time now
Date.prototype.timeNow = function () {
     return ((this.getHours() < 10)?"0":"") + this.getHours() + ":"
        + ((this.getMinutes() < 10)?"0":"") + this.getMinutes() + ":"
        + ((this.getSeconds() < 10)?"0":"") + this.getSeconds();
};
