var http = require('http');
var url = require('url');
var path = require('path');
var fs = require('fs');

var server = http.createServer(function(req, res) {
	var path = url.parse(req.url).pathname;
	console.log(path);
	if (path === '/sendDrawData') {
		var store = '';
		req.on('data', function(data) {
			store += data;
		});
		req.on('end', function(){
			store = JSON.parse(store);
			console.log(store);
			res.end("received");
		});
	}
	else if (path === '/') {
		fs.readFile('home.html', 'utf-8', function(err, data) {
			if (err) {
				console.error(err);
			}
			res.end(data);
		});
	}
	else if (path.length > 0){
		fs.readFile(path.substr(1), 'utf-8', function(err, data) {
			if (err) {
				console.error(err);
			}
			res.end(data);
		});
	}
	else{
		res.end("");
	}
});

server.listen('8080', '127.0.0.1');