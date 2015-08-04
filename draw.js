var canvas = document.getElementById("drawingPad");
var context = canvas.getContext("2d");
var isMouseDown = false;
var mouseX = 0;
var mouseY = 0;
var track = [];
var strokes = [];
var startTime = 0;
var maxMusicNum = 10;

context.strokeStyle = "#000000"; // drawing black lines.

// make sure the canvas' background is actually white for saving.
context.fillStyle = "#ffffff";
context.fillRect(0,0,canvas.width,canvas.height);

// when the user presses their mouse down on the canvas.
canvas.addEventListener("mousedown",function (evt) {
    isMouseDown = true;

    if (evt.x != undefined && evt.y != undefined)
    {
        mouseX = evt.x;
        mouseY = evt.y;
    }
    else
    {
        mouseX = evt.layerX;
        mouseY = evt.layerY;
    }
    mouseX -= canvas.offsetLeft;
    mouseY -= canvas.offsetTop;
    //alert("coordinates" + evt.layerX - canvas.offsetLeft - canvas.offsetLeft + ", " + evt.layerY - canvas.offsetTop);

    context.beginPath();
    context.moveTo(mouseX, mouseY);
    track = [];
    startTime = Date.now()
    track.push(mouseX, mouseY, 0);
});

// when the user lifts their mouse up anywhere on the screen.
window.addEventListener("mouseup",function (evt) {
    if (isMouseDown){
        //alert(track.join(' '));
        strokes.push(track);
        track = [];
    }
        
    isMouseDown = false;
    
});

// as the user moves the mouse around.
canvas.addEventListener("mousemove",function (evt) {
    if (isMouseDown) {
        if (evt.x != undefined && evt.y != undefined)
        {
            mouseX = evt.x;
            mouseY = evt.y;
        }
        else
        {
            mouseX = evt.layerX;
            mouseY = evt.layerY;
        }
        mouseX -= canvas.offsetLeft;
        mouseY -= canvas.offsetTop;

        context.lineTo(mouseX, mouseY);
        context.stroke();
        track.push(mouseX, mouseY, Date.now() - startTime);
    }
});

// swatch interactivity
// var palette = document.getElementById("palette");
// var swatches = palette.children;
// var currentSwatch; // we'll keep track of what swatch is active in this.

// for (var i = 0; i < swatches.length; i++) {
//     var swatch = swatches[i];
//     if (i == 0) {
//         currentSwatch = swatch;
//     }

//     // when we click on a swatch...
//     swatch.addEventListener("click",function (evt) {

//         this.className = "active"; // give the swatch a class of "active", which will trigger the CSS border.
//         currentSwatch.className = ""; // remove the "active" class from the previously selected swatch
//         currentSwatch = this; // set this to the current swatch so next time we'll take "active" off of this.

//         context.strokeStyle = this.style.backgroundColor; // set the background color for the canvas.
//     });
// }

//select music number
var musicNum = document.getElementById("music_number");
var opt = 1;
var option;
for (opt = 1; opt < maxMusicNum; ++opt) {
    option = document.createElement('option');
    option.setAttribute('value', opt.toString());
    option.innerText = opt.toString();
    option.textContent = opt.toString();
    //alert(option.getAttribute('value'));
    musicNum.appendChild(option);
}

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
    this.setAttribute("download","drawing-" + now + ".jpg");
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
    saveBtn2.setAttribute('download', 'fuckyou.txt');
//    window.open('data:text/txt;charset=utf-8,' + encodeURIComponent(output.join("\n")));
//    window.URL.revokeObjectURL(url);

});