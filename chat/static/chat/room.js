$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var chatsock = new WebSocket(ws_scheme + '://' + window.location.host + '/msg' + window.location.pathname);

    var $table = $('table');
    var $header = $('nav');
    var $formIntro = $('#intro');
    var $tableWrapper = $('#table-wrapper');
    var $window = $(window);
    
    chatsock.onmessage = function(message) {
        var data = JSON.parse(message.data);
        var $ele = $('<tr></tr>')

        $ele.append(
            $("<td></td>").text(data.timestamp)
            )
        $ele.append(
            $("<td></td>").text(data.handle)
            )
        $ele.append(
            $("<td></td>").text(data.message)
            )
        
        $table.append($ele);
        scrollToBottom();
    };

    $('form').on("submit", function(event) {
        var message = {
            handle: $('#handle').val(),
            message: $('#message').val(),
        }
        chatsock.send(JSON.stringify(message));
        $("#message").val('').focus();
        return false;
    });

    $window.on('resize', function(){
        var introHeight = 0;
        $formIntro.children().each(function(){
            introHeight += $(this).outerHeight(true);
        });
        var height = $(this).height() - $header.outerHeight(true) - introHeight;
        $tableWrapper.height(height);
    });

    function scrollToBottom () {
        $tableWrapper.animate({ scrollTop: $tableWrapper.prop("scrollHeight")}, 1000);
    };

    $window.trigger('resize');
    scrollToBottom();
});