var http = require('http');
var url = require('url');
var path = require('path');
var fs = require('fs');
//redirect log
var fs = require('fs');
var util = require('util');
var log_file = fs.createWriteStream(__dirname + '/debug.log', {flags : 'w'});
var log_stdout = process.stdout;

console.log = function(d) { //
  log_file.write(util.format(d) + '\n');
  log_stdout.write(util.format(d) + '\n');
};

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
			//console.log(store);
			res.end("received");
			var musicNumber = store.musicNumber;
			var strokes = store.strokes;
			var img = store.img;
			var name = store.userName;
			//console.log(img);

			//save image
			var regex = /^data:.+\/(.+);base64,(.*)$/;
			var matches = img.match(regex);
			var ext = matches[1];
			var data = matches[2];
			var buffer = new Buffer(data, 'base64');
			fs.writeFileSync('img/'+name+'_'+musicNumber+'.'+ext, buffer);
		
			//save strokes
			fs.writeFileSync('stroke/'+name+'_'+musicNumber+'.txt', strokes);
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
		fs.readFile(path.substr(1), function(err, data) {
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

server.listen('9111', '127.0.0.1');