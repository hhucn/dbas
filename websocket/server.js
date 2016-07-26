// Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>

// npm install socket.io
// npm install --save express

var port = 9999;
var clients = {};

var express = require('express');
var app = express();
var url = require('url');

var http = require('http');
var https = require('https');
var server = http.createServer(app);

server.listen(port);
var io = require('socket.io').listen(server);


app.get('/publish/notification', function(req, res){
    var params = getDictOfParams(req['url']);
    try {
        clients[params['socket_id']].emit('publish', {'msg': params['msg'].replace('%20', ' '), 'type': 'notifications'});
        res.writeHead(200);
    } catch (e) {
        logMessage('  No socket for socket_id ' + params['socket_id']);
        res.writeHead(400);
    }
    res.end();
});

io.sockets.on('connection', function(socket){
    addClient(socket);
    socket.emit('subscribe', socket.id);

    socket.on('disconnect', function(){
        removeClient(socket);
    });
});

// Console logger
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
    logMessage('Removed ' + socket.id + ' from dict');
};

// Parses url
getDictOfParams = function(url){
    logMessage(url);
    var param = url.substr(url.indexOf('?')+1);
    var params = param.split('&');
    var dict = {};
    var split = '';
    params.forEach(function(entry) {
        split = entry.split('=');
        if (split[0] == 'socket_id')
            split[1] = '/#' + split[1];
        dict[split[0]] = split[1];
        logMessage('  ' + split[0] + ': ' + split[1]);
    });
    return dict;
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
