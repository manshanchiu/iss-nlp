// DOM Elements

const fileInput = document.querySelector("#file-input");
const previewImage = document.querySelector("#preview-image");
const recognizeBtn = document.querySelector("#recognize-btn");
const extractedText = document.querySelector("#extracted-text");
const sheetInput = document.querySelector("#sheet-input");
const retrievedItem = document.querySelector("#retrieved-item");

let resultFile = "";
let _socket = null;

const myMessageBlock = `<li class="clearfix">
<div class="message-data text-right">
  <span class="message-data-time">{{time}}, Today</span>
  <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="avatar">
</div>
<div class="message other-message float-right">{{message}}</div>
</li>`

const botResponseBlock = `<li class="clearfix">
<div class="message-data">
  <span class="message-data-time">{{time}}, Today</span>
</div>
<div class="message my-message">{{message}}</div>
</li>`

// initSocket()

// File Upload Handler
function handleFileUpload() {
  const file = fileInput.files[0];
  const reader = new FileReader();

  reader.addEventListener("load", (event) => {
    previewImage.src = event.target.result;
  });

  reader.readAsDataURL(file);
}

// Event Listeners
// fileInput.addEventListener("change", handleFileUpload);
// recognizeBtn.addEventListener("click", handleOCR);

async function sendMessage(message) {
  const input = {
    message
  };
  await _socket.send(JSON.stringify(input));
}

function initSocket() {
  console.log("Initializing WebSocket connection");
  const socket = new WebSocket(`ws://${config.host}:${config.port}`);


  socket.onopen = (event) => {
    console.log("WebSocket connected");
    document
      .getElementsByClassName("status-icon success")[0]
      .classList.add("show");
    document
      .getElementsByClassName("status-icon error")[0]
      .classList.remove("show");
    listenToAll(socket)
  };


  socket.onerror = (event) => {
    console.log("WebSocket error:", event);
    document
      .getElementsByClassName("status-icon success")[0]
      .classList.remove("show");
    document.getElementsByClassName("status-icon error")[0].classList.add("show");
  };

  socket.onclose = (event) => {
    console.log("WebSocket closed:", event);
    document
      .getElementsByClassName("status-icon success")[0]
      .classList.remove("show");
    document.getElementsByClassName("status-icon error")[0].classList.add("show");
    _socket = null
    setTimeout(initSocket,1000)
  };
}

function listenToAll(socket) {
  _socket = socket
  socket.onmessage = (event) => {
    // Display gpt result
    document.getElementById("loading-overlay").style.display = "none";
    console.log(event);
    let result = JSON.parse(event.data);
    const m = result["message"];
    $("#message_box").append(botResponseBlock.replace("{{message}}",m).replace("{{time}}",getDisplayTime()))
    scrollToBottom()
  };
}

function scrollToBottom() {
  $(".chat-history")[0].scrollTo(0, $(".chat-history")[0].scrollHeight);
}

initSocket()

$("#submit").on("click",function() {
  if ($("#message").val() != "") {
      document.getElementById("loading-overlay").style.display = "block";
      sendMessage($("#message").val())
      $("#message_box").append(myMessageBlock.replace("{{message}}",$("#message").val()).replace("{{time}}",getDisplayTime()))
      scrollToBottom()
      $("#message").val("")
  }
});

document.addEventListener("keydown", function(event) {
  let key = event.key;
  if (key == "Enter") {
      $("#submit").click();
  }
});

const getDisplayTime = () => {
  let date = new Date();
  const result = date.toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "numeric",
    hour12: true,
   });
  return result;
}
