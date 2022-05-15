const express = require("express");
const app = express();
const http = require("http");
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);
var fs = require("fs");
var cameraBuffer = Buffer.from("");
var screenBuffer = Buffer.from("");

var timer = null;
var recordtime;

app.use(express.static("./"));

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

io.on("connection", function (socket) {
  console.log("open");
  peerSocket = socket;
  socket.on("open", socketOpen);
  socket.on("disconnect", socketClose);
  socket.on("camerablob", getCameraBlob);
  socket.on("screenblob", getScreenBlob);
  socket.on("startRecording", startRecording);
  socket.on("endRecording", endRecording);
});

function socketOpen() {
  console.log("open");
}

function socketClose(reason) {
  console.log("close: ", reason);
}

function startRecording() {
  console.log("start recording");
  cameraBuffer = Buffer.from("");
  screenBuffer = Buffer.from("");
  recordtime = 0;
  timer = setInterval(() => {
    recordtime += 10;
    console.log(
      "have recorded",
      Math.floor(recordtime / 60),
      "minute",
      recordtime % 60,
      "second"
    );
  }, 10000);
}

function getCameraBlob(event) {
  cameraBuffer = Buffer.concat([cameraBuffer, event.blob]);
}

function getScreenBlob(event) {
  screenBuffer = Buffer.concat([screenBuffer, event.blob]);
}

function endRecording() {
  console.log("end recording");
  clearInterval(timer);
  fs.writeFileSync("webm/camera.webm", cameraBuffer);
  fs.writeFileSync("webm/screen.webm", screenBuffer);
  fs.writeFileSync("mp4/camera.mp4", cameraBuffer);
  fs.writeFileSync("mp4/screen.mp4", screenBuffer);
}

server.listen(3000, () => {
  console.log("listening on *:3000");
});
