const form = document.querySelector("#chat-form")
form.addEventListener("submit", sendMessage)
function sendMessage(e) {
    e.preventDefault()
    let _message = document.getElementById("message").value
    console.log(_message);
}