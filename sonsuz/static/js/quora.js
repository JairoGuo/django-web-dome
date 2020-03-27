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


    $(".question-vote").click(function () {

        let span = $(this);
        let questionId = $(this).closest("#question-content").attr("question-id");
        let vote = null;
        if ($(this).hasClass("up")) {
            vote = "U";
        } else {
            vote = "D";
        }
        $.ajax({
            url: '/quora/question/vote/',
            data: {
                'questionId': questionId,
                'value': vote
            },
            type: 'post',
            cache: false,
            success: function (data) {
                // $('.question-vote').removeClass('basic');
                // $('.question-vote').addClass('basic');
                if (vote === "U") {
                    if (span.hasClass("basic")) {
                        $('.question-vote').removeClass('basic');
                        $('.question-vote').addClass('basic');
                        $(span).removeClass("basic");


                    } else {
                        $('.question-vote').removeClass('basic');
                        $('.question-vote').addClass('basic');
                        $(span).addClass("basic");

                    }
                    // $(span).removeClass("basic");
                }
                if (vote === "D") {
                    if (span.hasClass("basic")) {
                        $('.question-vote').removeClass('basic');
                        $('.question-vote').addClass('basic');
                        $(span).removeClass("basic");
                    } else {
                        $('.question-vote').removeClass('basic');
                        $('.question-vote').addClass('basic');
                        $(span).addClass("basic");

                    }
                }
                $("#questionVotes-u").text(data.votes[0]);
                $("#questionVotes-d").text(data.votes[1]);
            }
        });
    });

    $(".answer-vote").click(function () {
        // Vote on an answer.
        let span = $(this);
        let answerId = $(this).closest("#answer-content").attr("answer-id");
        vote = null;
        if ($(this).hasClass("up")) {
            vote = "U";
        } else {
            vote = "D";
        }
        $.ajax({
            url: '/quora/answer/vote/',
            data: {
                'answerId': answerId,
                'value': vote
            },
            type: 'post',
            cache: false,
            success: function (data) {

                if (vote === "U") {
                    if (span.hasClass("basic")) {
                        $('.answer-vote', span.closest("#answer-content")).removeClass('basic');
                        $('.answer-vote', span.closest("#answer-content")).addClass('basic');
                        $(span).removeClass("basic");
                    } else {
                        $('.answer-vote', span.closest("#answer-content")).removeClass('basic');
                        $('.answer-vote', span.closest("#answer-content")).addClass('basic');
                        $(span).addClass("basic");

                    }
                }

                if (vote === "D") {

                    if (span.hasClass("basic")) {
                        $('.answer-vote', span.closest("#answer-content")).removeClass('basic');
                        $('.answer-vote', span.closest("#answer-content")).addClass('basic');
                        $(span).removeClass("basic");
                    } else {
                        $('.answer-vote', span.closest("#answer-content")).removeClass('basic');
                        $('.answer-vote', span.closest("#answer-content")).addClass('basic');
                        $(span).addClass("basic");
                    }
                }

                $("#answerVotesU-" + answerId).text(data.votes[0]);
                $("#answerVotesD-" + answerId).text(data.votes[1]);
            }
        });
    });

    $(".acceptAnswer").click(function () {
        // Mark an answer as accepted.
        var span = $(this);
        var answerId = $(this).closest(".answer").attr("answer-id");
        $.ajax({
            url: '/quora/accept-answer/',
            data: {
                'answerId': answerId
            },
            type: 'post',
            cache: false,
            success: function (data) {
                $("#acceptAnswer-" + answerId).removeClass("accepted");
                $("#acceptAnswer-" + answerId).prop("title", "点击接受回答");
                $("#acceptAnswer-" + answerId).addClass("accepted");
                $("#acceptAnswer-" + answerId).prop("title", "该回答已被采纳");
            }
        });
    });


});
