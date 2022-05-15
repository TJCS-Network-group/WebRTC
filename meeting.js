
var socket = io();
var video = document.getElementById('video');
var screenVideo = document.getElementById('screen');
var startButton = document.getElementById('startbutton');
var stopButton = document.getElementById('stopbutton');
var cameraStreaming = false;
var screenStreaming = false;

var localStream = null;
var screenStream = null;

var width = 500;
var height = null;
let peer = null;
var dc = null;

const SLICE_SIZE = 10000;


let cameraRecorder = null;
let screenRecorder = null;

let cameraBuffer = [];
let screenBuffer = [];


let cameraRecorderOption = {
  type: 'video',
  mimeType: 'video/webm;codecs=vp8',
  timeSlice: 10000,
  frameRate: 15,

  ondataavailable: function (blob) {
    console.log(blob)

    sendBlob("camerablob", blob);
    // socket.emit("camerablob", { blob });
    // invokeSaveAsDialog(blob);
  },
}

let screenRecorderOption = {
  type: 'video',
  mimeType: 'video/webm;codecs=vp8',
  timeSlice: 100,
  frameRate: 15,
  ondataavailable: function (blob) {
    console.log(blob)
    sendBlob("screenblob", blob);

    // socket.emit("screenblob", { blob });
  },
}


let cameraOption = {
  audio: true,
  video: {
    width: 640,
    height: 480,
    facingMode: "user"
  }
}

let screenOption = {
  audio: true,
  video: {
    width: 1280,
    height: 720,
  }
}


function sendBlob(type, blob) {
  // socket.emit(type, { blob })
  let blobSize = blob.size;
  var sliceCount = Math.ceil(blob.size / SLICE_SIZE);

  // if (!socket.connected) {
  //   console.log(type, "stored in buffer");
  //   if (type == "screenblob") {
  //     screenBuffer.push(blob);
  //   }
  //   else if (type == "camerablob") {
  //     cameraBuffer.push(blob);
  //   }
  //   return;
  // }

  for (let i = 0; i < sliceCount; i++) {
    let start = i * SLICE_SIZE;
    let end = start + SLICE_SIZE;
    if (end > blobSize) {
      end = blobSize;
    }
    let newBlob = blob.slice(start, end);
    socket.emit(type, { blob: newBlob });
  }

}

socket.on('connection', function () {
  console.log("connected");
  // console.log("send buffer");
  // if (screenBuffer.length != 0) {
  //   for (var blob in screenBuffer) {
  //     socket.emit("screenblob", { blob })
  //   }
  //   screenBuffer = [];
  // }
  // if (cameraBuffer.length != 0) {
  //   for (var blob in cameraBuffer) {
  //     socket.emit("camerablob", { blob })
  //   }
  //   cameraBuffer = [];
  // }
});

socket.on('open', socketOpen);
socket.on('disconnect', socketClose);



navigator.mediaDevices.getUserMedia(cameraOption)
  .then(function (stream) {
    localStream = stream;
    video.srcObject = stream;
    video.muted = true;
    video.play();
  })
  .catch(function (err) {
    console.log("An error occured! " + err);
  });

navigator.mediaDevices.getDisplayMedia(screenOption)
  .then(function (stream) {
    screenStream = stream;
    screenVideo.srcObject = stream;
    screenVideo.muted = true;
    screenVideo.play();
  });

video.addEventListener('canplay', function (ev) {
  if (!cameraStreaming) {
    height = video.videoHeight / (video.videoWidth / width);

    video.setAttribute('width', width);
    video.setAttribute('height', height);
    cameraStreaming = true;
  }
}, false);

screenVideo.addEventListener('canplay', function (ev) {
  if (!screenStreaming) {
    height = screenVideo.videoHeight / (screenVideo.videoWidth / width);

    screenVideo.setAttribute('width', width);
    screenVideo.setAttribute('height', height);
    screenStreaming = true;

  }
}, false);

startButton.addEventListener('click', function (ev) {
  if (!localStream || !screenStream || !socket) {
    alert('尚未准备好');
  }

  socket.emit('startRecording');
  cameraRecorder = new RecordRTC(localStream, cameraRecorderOption);
  screenRecorder = new RecordRTC(screenStream, screenRecorderOption);
  cameraRecorder.startRecording();
  screenRecorder.startRecording();

})


stopButton.addEventListener('click', function (ev) {
  cameraRecorder.stopRecording();
  screenRecorder.stopRecording();
  socket.emit('endRecording');
})

function socketOpen() {
  console.log("open");

}

function socketClose(reason) {
  console.log("close: ", reason);
}


