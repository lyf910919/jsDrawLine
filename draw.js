var canvas = document.getElementById("drawingPad");
var context = canvas.getContext("2d");
var isMouseDown = false;
var mouseX = 0;
var mouseY = 0;
var track = [];
var strokes = [];
var startTime = 0;
var maxMusicNum = 10;
var curMusicNum = 1;
var userName = "";

context.strokeStyle = "#000000"; // drawing black lines.

// make sure the canvas' background is actually white for saving.
context.fillStyle = "#ffffff";
context.fillRect(0,0,canvas.width,canvas.height);

//set first music
var player = document.getElementById("player");
player.setAttribute("src", "music/"+curMusicNum+".mp3");
var musicNumber = document.getElementById("music_number");
musicNumber.innerText="Music Playing: 1/10";
musicNumber.textContent="Music Playing: 1/10";

//when name input button clicked
function saveName(evt) {
    userName = document.getElementById("user_name").value;
    if (userName === "") {
        alert("请先输入你的名字，点击确定保存~~~");
    }
    else {
        var uname = document.getElementById("name_input");
        uname.setAttribute("class", "btn btn-primary btn-md disabled");
    }
}
var nameInput = document.getElementById("name_input");
nameInput.addEventListener("click", saveName);

//pack data to be sent to server
function packData() {
    //store strokes
    var output = [];
    var i = 0;
    for (i = 0; i < strokes.length; ++i){
        output.push(strokes[i].join(" "));
    }

    //make sure user name is not empty
    if (userName === "") {
        alert("请先输入你的名字，点击确定保存~~~");
        return -1;
    }

    //store image
    output = output.join("\n");
    var imgData = canvas.toDataURL("image/jpeg");
    var data = {
        strokes: output,
        img: imgData,
        musicNumber: curMusicNum,
        userName: userName
    }
    return data;
}

//when next music button clicked
function send(){
    if (curMusicNum == maxMusicNum) {
        var nextMusic = document.getElementById("next_music");
        nextMusic.setAttribute("class", "btn btn-primary btn-lg disabled");
    }
    //alert('comming to next music!');
    //save tracks
    var userData = packData();
	if (userData === -1) {
        return -1;
    }
    //alert(JSON.stringify(userData));
    $.ajax({
        type: "POST",
        url: "saveJson.php",
        dataType: "json",
        contentType: "application/json; charset=UTF-8",
        data: JSON.stringify(userData),
        success: function(response) {
            alert(response);
        },
        error: function(err) {
            alert(err.responseText);
        }
    });
    curMusicNum = curMusicNum + 1;
    if (curMusicNum === maxMusicNum) {
        var btn = document.getElementById("next_music");
        btn.innerText="Done";
        btn.textContent="Done";
    }
    player.setAttribute("src", "music/"+curMusicNum+".mp3");
    musicNumber.innerText="Music Playing: "+curMusicNum+"/"+maxMusicNum;
    musicNumber.textContent="Music Playing: "+curMusicNum+"/"+maxMusicNum;
    context.fillRect(0,0,canvas.width,canvas.height);
    strokes = [];

}


// when the user presses their mouse down on the canvas.
function downDraw(evt) {
        
    isMouseDown = true;

    if (evt.x != undefined && evt.y != undefined)
    {
        mouseX = evt.x;
        mouseY = evt.y;
    }
    else
    {
        mouseX = evt.pageX;
        mouseY = evt.pageY;
    }
    mouseX -= canvas.offsetLeft;
    mouseY -= canvas.offsetTop;
    //alert("coordinates" + evt.layerX - canvas.offsetLeft - canvas.offsetLeft + ", " + evt.layerY - canvas.offsetTop);

    context.beginPath();
    context.moveTo(mouseX, mouseY);
    track = [];
    startTime = Date.now()
    track.push(mouseX, mouseY, 0);
}

canvas.addEventListener("mousedown", downDraw);
canvas.addEventListener("touchstart", downDraw);

// when the user lifts their mouse up anywhere on the screen.
function upDraw(evt) {
    if (isMouseDown){
        //alert(track.join(' '));
        strokes.push(track);
        track = [];
    }
        
    isMouseDown = false;
    
}
window.addEventListener("mouseup", upDraw);
window.addEventListener("touchend", upDraw);

// as the user moves the mouse around.
function moveDraw(evt) {
    if (isMouseDown) {
        if (evt.x != undefined && evt.y != undefined)
        {
            mouseX = evt.x;
            mouseY = evt.y;
        }
        else
        {
            mouseX = evt.pageX;
            mouseY = evt.pageY;
        }
        mouseX -= canvas.offsetLeft;
        mouseY -= canvas.offsetTop;

        context.lineTo(mouseX, mouseY);
        context.stroke();
        track.push(mouseX, mouseY, Date.now() - startTime);
    }
}
canvas.addEventListener("mousemove", moveDraw);
canvas.addEventListener("touchmove", moveDraw);


// when the clear button is clicked
var clearBtn = document.getElementById("clear");
clearBtn.addEventListener("click",function(evt) {
    canvas.width = canvas.width; // this is all it takes to clear!

    // make sure the canvas' background is actually white for saving.
    context.fillStyle = "#ffffff";
    context.fillRect(0,0,canvas.width,canvas.height);
    strokes = [];
});

// when the save image button is clicked
var saveBtn = document.getElementById("save_image");
saveBtn.addEventListener("click",function (evt) {
    // we'll save using the new HTML5 download attribute to save the image. 
    // we'll give the image a name of draw-[timestamp].jpg

    var now = new Date().getTime(); // get today's date in milliseconds.
    var dataUri = canvas.toDataURL("image/jpeg");  // get the canvas data as a JPG.

    // change the a href and download attributes so it'll save.
    var fileName = curMusicNumber + '.jpg';
    this.setAttribute("download", fileName);
    this.setAttribute("href",dataUri);

    // in older browsers you may need to substitute those last two lines of code with this:
    // window.open(dataUri,"_blank");
});

// when the save track button is clicked
var saveBtn2 = document.getElementById("save_track");
saveBtn2.addEventListener("click", function (evt) {
    var output = [];
    var i = 0;
    for (i = 0; i < strokes.length; ++i){
        output.push(strokes[i].join(" "));
    }
    var blob = new Blob([output.join("\n")], {type: 'text/plain'});
    //saveAs(blob, 'filename.txt')
    var url = window.URL.createObjectURL(blob);
    saveBtn2.href = url;

    //set file name to the music selected
    var fileName = musicNum.value + '.txt';
    saveBtn2.setAttribute('download', fileName);
//    window.open('data:text/txt;charset=utf-8,' + encodeURIComponent(output.join("\n")));
//    window.URL.revokeObjectURL(url);

});

