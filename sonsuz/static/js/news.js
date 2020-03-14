$(function () {
    //从 cookie 里面获取 csrftoken
    let csrftoken = getCookie('csrftoken');
    //
    // 这个设置会让所有Ajax POST/DELETE请求在其请求头中都携带 X-CSRFToken 信息
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // 默认焦点
    $('#newsFormModal').on('shown.bs.modal', function () {
        $('#newsInput').trigger('focus')
    });


    // 关闭发布新闻模态框
    $("#postClose").click(function () {
        $("#newsFormModal").modal("hide");
    });

    // 发布新闻
    $("#postNews").click(function () {
        if ($("#newsTitle").val() === '') {
            alert("请输入新闻动态的标题！");
            return;
        }
        if ($("#newsInput").val() === '') {
            alert("请输入新闻动态的内容！");
            return;
        }
        if (currentUser === "") {
            alert("请登录后再发布新闻动态！");
        } else {
            // Ajax call after pushing button, to register a News object.
            $.ajax({
                url: '/news/post-news/',
                data: $("#postNewsForm").serialize(),
                type: 'POST',
                cache: false,
                success: function (data) {
                    $("div.newcontent").prepend(data);
                    $("#newsInput").val("");
                    $("#newsFormModal").modal("hide");
                    // hide_stream_update();
                },
                error: function (data) {
                    alert(data.responseText);
                },
            });
        }

    });

    //点赞模块
    $("div.newcontent").on("click", ".likes", function () {

        if (currentUser === "") {
            alert("请登录后再点赞！");
            return;

        }

        let item = $(this).closest('.item');

        let newsId = $(item).attr("news-id");
        let payload = {
            'newsId': newsId,
            'csrf_token': csrftoken
        };
        $.ajax({
            url: '/news/like/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".likes .like-count", item).text(data.likers_count);
                if ($(".likes .heart", item).hasClass("inline")) {
                    $(".likes .heart", item).removeClass("inline");
                    $(".likes .heart", item).addClass("outline");
                } else {
                    $(".likes .heart", item).removeClass("outline");
                    $(".likes .heart", item).addClass("inline");
                }
            }
        });
    });

    //新闻内容
    $("div.newcontent").on("click", ".news-header", function () {


        // 每一次查看新闻内容初始展开评论

        if ($("#comment").hasClass("active")) {
            $("#comment").removeClass("active");
            $("#comment-content").removeClass("active");
        }

        let item = $(this).closest('.item');

        let newsId = $(item).attr("news-id");
        let payload = {
            'newsId': newsId,
            'csrf_token': csrftoken
        };
        $('.newsview')
            .modal({
                blurring: true

            })
            .modal('show')
        ;

        $.ajax({
            url: '/news/content/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".newsview #title").html(data.news_title);

                $(".newsview #newscontent").html(data.news_conent);

            }
        });

    });


    //
    // $('#replyFormModal').on('show.bs.modal', function (event) {
    //     let button = $(event.relatedTarget); // Button that triggered the modal
    //     let recipient = button.data('who'); // Extract info from data-* attributes
    //     let newsid = button.data('newsid'); // Extract info from data-* attributes
    //     let modal = $(this);
    //     modal.find('.modal-title').text('新的回复到： ' + recipient);
    //     modal.find('.modal-body input.recipient').val(recipient);
    //     modal.find('.modal-body input.newsid').val(newsid);
    // });
    //
    // $("#postReply").click(function () {
    //     if ($("#reply-content").val() === '') {
    //         alert("请输入评论的内容！");
    //         return;
    //     }
    //     if (currentUser === "") {
    //         alert("请登录后再发布评论！");
    //     } else {
    //         // Ajax call after pushing button, to register a News object.
    //         $.ajax({
    //             url: '/news/post-reply/',
    //             data: $("#postReplyForm").serialize(),
    //             type: 'POST',
    //             cache: false,
    //             success: function (data) {
    //                 let li = $('[news-id=' + data.newsid + ']');
    //                 $(".reply .reply-count", li).text(data.replies_count);
    //                 $("#reply-content").val("");
    //                 $("#replyFormModal").modal("hide");
    //                 // hide_stream_update();
    //             },
    //             error: function (data) {
    //                 alert(data.responseText);
    //             },
    //         });
    //     }
    //
    // });
    //
    //
    // $("ul.stream").on("click", ".reply", function () {
    //     let li = $(this).closest('li');
    //     let newsId = $(li).attr("news-id");
    //     $.ajax({
    //         url: '/news/get-replies/',
    //         data: {'newsId': newsId},
    //         cache: false,
    //         success: function (data) {
    //             $("#replyListModal .modal-body").html(data.replies_html);
    //         }
    //     });
    // });
});
