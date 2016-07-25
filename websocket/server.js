// Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>

// npm install socket.io
// npm install --save express

var port = 9999;
var clients = {};

var express = require('express');
var app = express();

var http = require('http');
var https = require('https');
var server = http.createServer(app);

server.listen(port);
var io = require('socket.io').listen(server);

app.get('/', function(req, res){
//    res.sendFile(__dirname + '/index.html');
    res.writeHead(200);
    res.end();
});

io.sockets.on('connection', function(socket){
    addClient(socket);
    socket.emit('subscribe', socket.id);

    socket.on('disconnect', function(){
        removeClient(socket);
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

// Add client to dictionary
addClient = function(socket){
    clients[socket.id] = socket;
    logMessage('Added ' + socket.id + ' into dict');
};

// Remove client from dictionary
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
