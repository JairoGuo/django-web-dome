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
                    $("#newsTitle").val("");
                    $("#newsFormModal").modal("hide");
                    // hide_stream_update();
                },
                error: function (data) {
                    alert(data.responseText);
                },
            });
        }

    });

    // 新闻列表点赞功能
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

    var item;
    var newsId;

    // 显示新闻内容 --------------------------------
    $("div.newcontent").on("click", ".news-header", function () {

        // 每一次查看新闻内容初始展开评论

        if ($("#comment").hasClass("active")) {
            $("#comment").removeClass("active");
            $("#comment-content").removeClass("active");
        }
        $("#reply-content").text("");


        item = $(this).closest('.item');
        newsId = $(item).attr("news-id");
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
                $(".newsview #title").text(data.news_title);
                $(".newsview #newscontent").text(data.news_conent);
                $(".newsview #news-like-count").text(data.news_like_count);
                $(".newsview #news-comment-count").text(data.news_cocmment_count);
                $("#news-like").removeClass("inline");
                $("#news-like").removeClass("outline");
                $("#news-like").addClass(data.news_like_flag);
                $("#news-comment").removeClass("inline");
                $("#news-comment").removeClass("outline");
                $("#news-comment").addClass(data.news_comment_flag);

            }
        });

        $.ajax({
            url: '/news/get-replies/',
            data: {'newsId': newsId},
            cache: false,
            success: function (data) {
                $("#comment-content-item").html(data.replies_html);
            }
        });
        if ($("#comment").hasClass("active")) {
            $("#comment-switch").text("收缩评论");
        } else {
            $("#comment-switch").text("展开评论");
        }


    });


    $('.ui.accordion')
        .accordion()
    ;


    // 评论展开
    $('.ui.accordion').click(function () {
        if ($("#comment").hasClass("active")) {
            $("#comment-switch").text("收缩评论");
        } else {
            $("#comment-switch").text("展开评论");
        }
    });


    // 新闻显示内的点赞功能
    $("#news-conten-like").click(function () {

        if (currentUser === "") {
            alert("请登录后再点赞！");
            return;

        }
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

                $("#news-like-count").text(data.likers_count);

                if ($(".likes .heart", item).hasClass("inline")) {
                    $(".likes .heart", item).removeClass("inline");
                    $(".likes .heart", item).addClass("outline");
                } else {
                    $(".likes .heart", item).removeClass("outline");
                    $(".likes .heart", item).addClass("inline");
                }

                if ($("#news-like").hasClass("inline")) {
                    $("#news-like").removeClass("inline");
                    $("#news-like").addClass("outline");
                } else {
                    $("#news-like").removeClass("outline");
                    $("#news-like").addClass("inline");
                }
            }
        });
    });

    // 新闻列表评论
    $("div.newcontent").on("click", "#news-comment", function () {

        if (currentUser === "") {
            alert("请登录后再评论！");
            return;
        }

        if ($("#comment").hasClass("active")) {
            $("#comment").removeClass("active");
            $("#comment-content").removeClass("active");
        }
        $("#reply-content").text("");

        item = $(this).closest('.item');
        newsId = $(item).attr("news-id");
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

        var news_user;

        $.ajax({
            url: '/news/content/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".newsview #title").text(data.news_title);
                $(".newsview #newscontent").text(data.news_conent);
                $(".newsview #news-like-count").text(data.news_like_count);
                $("#news-like").removeClass("inline");
                $("#news-like").removeClass("outline");
                $("#news-like").addClass(data.news_like_flag);


            }
        });

        $.ajax({
            url: '/news/get-replies/',
            data: {'newsId': newsId},
            cache: false,
            success: function (data) {
                $("#comment-content-item").html(data.replies_html);
            }
        });
        $("#comment").click();
        // $("#reply-content").text("@"+$(item).attr("news-user")+": ");


    });

    // 新闻显示内评论功能
    $("#news-conten-comment").click(function () {

        if (currentUser === "") {
            alert("请登录后再评论！");
            return;
        }
        $("#comment-switch").text("展开评论");
        $("#comment").click();

    });


    // 发表评论
    $("#postReply").click(function () {


        if ($("#reply-content").val() === '') {
            alert("请输入评论的内容！");
            return;
        }
        if (currentUser === "") {
            alert("请登录后再发布评论！");
        } else {
            // Ajax call after pushing button, to register a News object.
            // let payload = {
            //     'newsId': newsId,
            //     // 'csrf_token': csrftoken,
            //     'reply-content': $("#reply-content").serialize()
            // };
            $.ajax({
                url: '/news/post-reply/',
                // data: payload,
                data: $("#postReplyForm").serialize() + "&newsId=" + newsId,
                // data: $("#postReplyForm").serialize(),
                type: 'POST',
                cache: false,
                success: function (data) {

                    $("#news-reply-count", item).text(data.replies_count);
                    $(".newsview #news-comment-count").text(data.replies_count);

                    $("#reply-content").val("");
                    if ($("#news-reply-count-icon", item).hasClass("outline")) {
                        $("#news-reply-count-icon", item).removeClass("outline");
                        $("#news-reply-count-icon", item).addClass("inline");
                    }

                    $.ajax({
                url: '/news/get-replies/',
                data: {'newsId': newsId},
                cache: false,
                success: function (data) {
                    $("#comment-content-item").html(data.replies_html);
                }
            });

                    // hide_stream_update();
                },
                error: function (data) {
                    alert(data.responseText);
                },
            });


        }

    });


});
