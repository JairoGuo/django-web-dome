$(function () {
    const emptyMessage = '没有未读通知';
    const notice = $('#notifications');

    function CheckNotifications() {
        $.ajax({
            url: '/notifications/latest-notifications/',
            cache: false,
            success: function (data) {
                if (!data.includes(emptyMessage)) {
                    // notice.addClass('button');
                    $("i", notice).append("<div class=\"floating ui red empty label circular mini\"></div>");
                    // $("i", notice).removeClass("outline");

                }
            },
        });
    }

    CheckNotifications();  // 页面加载时执行

    function update_social_activity(id_value) {
        const newsToUpdate = $('[news-id=' + id_value + ']');
        $.ajax({
            url: '/news/update-interactions/',
            data: {'id_value': id_value},
            type: 'GET',
            cache: false,
            success: function (data) {
                $(".like-count", newsToUpdate).text(data.likes);
                $(".reply-count", newsToUpdate).text(data.replies);
            },
        });
    }

    notice.click(function () {
        if (notice.popup("is visible")==true) {
            notice.popup("hide");
            // alert("AA");
            CheckNotifications();
        } else {
            // notice.popover('dispose');
            $.ajax({
                url: '/notifications/latest-notifications/',
                cache: false,
                success: function (data) {

                    notice
                        .popup({

                            // inline: true,
                            // position: 'bottom center',
                            on: "click",
                            // title: "通知",
                            // context: "body",
                            // content: data,
                            html: data,

                        })
                    ;
                    notice.popup("show");


                    // $(".item", notice).text(data);

                    // $("i", notice).remove("<div class=\"floating ui red empty label circular mini\"></div>")




                },
            });
        }
        return false;  // 不是False
    });

    // WebSocket连接，使用wss(https)或者ws(http)
    const ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const ws_path = ws_scheme + '://' + window.location.host + '/ws/notifications/';
    const ws = new ReconnectingWebSocket(ws_path);

    // 监听后端发送过来的消息
    ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        switch (data.key) {
            case "notification":
                if (currentUser !== data.actor_name) {  // 消息提示的发起者不提示
                    // notice.addClass('btn-danger');
                    $("i", notice).append("<div class=\"floating ui red empty label circular mini\"></div>");

                }
                break;

            case "social_update":
                if (currentUser !== data.actor_name) {
                    // notice.addClass('btn-danger');
                    $("i", notice).append("<div class=\"floating ui red empty label circular mini\"></div>");

                    update_social_activity(data.id_value);
                }
                break;

            case "additional_news":
                if (currentUser !== data.actor_name) {
                    // notice.addClass('btn-danger');

                    $('#news-update-message').show();
                }
                break;

            default:
                console.log('error', data);
                break;
        }
    };
});
