// called from base_js.html
//preloadImage("{{profile_image|safe}}", 'id_profile_image')

function onFriendRequestSent() {
    location.reload();
}

function onFriendRequestCancelled() {
    location.reload();
}

function onFriendRemoved() {
    location.reload();
}

function onFriendRequestAccepted() {
    location.reload();
}

function onFriendRequestDeclined() {
    location.reload();
}


var sendFriendRequestBtn = document.getElementById("id_send_friend_request_btn")
if (sendFriendRequestBtn != null) {
    sendFriendRequestBtn.addEventListener("click", function () {
        //sendFriendRequest("{{id}}", onFriendRequestSent)
    })
}

var cancelFriendRequestBtn = document.getElementById("id_cancel_friend_request_btn")
if (cancelFriendRequestBtn != null) {
    cancelFriendRequestBtn.addEventListener("click", function () {
        //cancelFriendRequest("{{id}}", onFriendRequestCancelled)
    })
}

var removeFriendBtn = document.getElementById("id_unfriend_btn")
if (removeFriendBtn != null) {
    removeFriendBtn.addEventListener("click", function () {
        //removeFriend("{{id}}", onFriendRemoved)
    })
}

function triggerAcceptFriendRequest(friend_request_id) {
    //acceptFriendRequest(friend_request_id, onFriendRequestAccepted)
}

function triggerDeclineFriendRequest(friend_request_id) {
    //declineFriendRequest(friend_request_id, onFriendRequestDeclined)
}