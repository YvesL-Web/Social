$(document).on('submit', '#chat-form', function (e) {
    e.preventDefault();
    let _message = $("#message").val();
    let _to_user = $("#to_user").val();
    $.ajax({
        type: 'POST',
        url:"",
        data: {
            message: _message,
            to_user: _to_user,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function (success) {
            console.log(success)
            let _html =
                '<div class="row g-0">\
              <div class="col-md-3 offset-md-9">\
                <div class="chat-bubble right-bubble">'+ _message + '</div>\
              </div>\
            </div>\
            '
            $(".chat-panel").append(_html)
        }
    });
    document.getElementById("message").value = ""
});

$(document).ready(function(){
    setInterval(function(){
        $(".chat-panel").load('send_message/' + " .chat-panel" )
    },5000)
})