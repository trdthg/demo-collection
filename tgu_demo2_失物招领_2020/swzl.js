$(document).ready(function() {

    //各种页面切换
    function loadAll() {
        /*$('.btn').unbind('click').click(function(){
            console.log("在触发点击事件之前先把之前绑定的点击事件解除掉")
        })*/


        $(".middleSquare").unbind('click').dbclick(function() {
            var id = $(this).attr("id");
            changecolor(id);
            $("#" + id + " .expandContentTop").text = "已找回 []~(￣▽￣)~*";
            reload();
            $("#rightMiddle1").css("display", "block");
            $(".middleSquare").css("display", "none");
            showmylostthings();

        });

        $("#registerButton1").unbind('click').click(function() {
            login();
        })
        $("#registerButton3").unbind('click').click(function() {
            register();
        })
        $("#pbulicmylost111").unbind('click').click(function() {
            publiclostthing();
            reload();
        })
        $("#changename").unbind('click').click(function() {
            changename();
        })
        $("#changephone").unbind('click').click(function() {
            changephone();
            //alert("1");
        })

        $("#rightTop2Btn").click(function() {
            $("#outsideWindow").css("display", "block");
            $("#outsideWindow1").css("display", "block");
            $("#register1").css("display", "block");
        })
        $("#registerButton2").click(function() {
            $("#register1").css("display", "none");
            $("#register2").css("display", "block");
        })
        $("#false1").click(function() {
            $("#outsideWindow").css("display", "none");
            $(".register").css("display", "none");
        })
        $("#false2").click(function() {
            $("#outsideWindow").css("display", "none");
            $(".register").css("display", "none");
        })

        $(".expand").click(function() {
            $("#outsideWindow").css("display", "block");
        })



        $("#L1").click(function() {
            $(".rightMiddle").css("display", "none");
            $("#rightMiddle1").css("display", "block");
            reload();
        });
        $("#L2").click(function() {
            $(".rightMiddle").css("display", "none");
            $("#rightMiddle1").css("display", "block");
            $(".middleSquare").css("display", "none");

            showmylostthings();
        });


        $("#L3").unbind("click").click(function() {
            if (ifloginornot() == 0) {
                $(".middleSquare").css("display", "none");
                //alert(ifloginornot());
                alert("您尚未登陆");
            } else {
                //alert(ifloginornot());
                $(".rightMiddle").css("display", "none");
                $("#rightMiddle3").css("display", "block");
            }
        });
        $("#L4").unbind("click").click(function() {
            $(".rightMiddle").css("display", "none");

            $("#rightMiddle4").css("display", "block");
        });

        $(".middleSquare").mouseenter(function() {
            $(".expandContentMiddle").css("display", "none");
            $(".expandContentMiddle").css("visibility", "hidden");
            $(".expandContentHide").css("display", "block");
            $(".expandContentHide").css("visibility", "visible");
        })
        $(".middleSquare").mouseleave(function() {
            $(".expandContentMiddle").css("display", "block");
            $(".expandContentMiddle").css("visibility", "visible");
            $(".expandContentHide").css("display", "none");
            $(".expandContentHide").css("visibility", "hidden");
        })
    }

    function reload() {
        $.post("./swzl.php", {
                dothis: "loadall"
            },
            function(data) {
                $("#rightMiddle1").empty();
                var t = "<div id=\"middleLeft\"></div>\
            <div id=\"middleRight\"><b>CSDN失物招领网</b></div>"
                $("#rightMiddle1").append(t);
                $("#rightMiddle1").append(data);
                loadAll();
            });
    }

    reload();



})