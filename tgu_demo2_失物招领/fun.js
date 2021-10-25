function loadme() {
    var data = new Array;
    $.ajax({
        type: "post",
        url: "./loadme.php",
        data: {
            account: gettheaccount(),
            password: getpassword(),
        },
        success: function(da) {
            //进行的函数
            //let data = JSON.parse(obj);
            data = eval('(' + da + ')');
            console.log(data);
            //console.log(obj);
            console.log(data["name"]);
            $("#myaccount").text(data.account);
            $("#myname").text(data.name);
            $("#myphone").text(data.phone);
        }
    })
}

function changecolor(obj) {

    $.post("changecolor.php", {
            account: gettheaccount(),
            password: getpassword(),
            id: obj,
        },
        function(info) {
            console.log(info);
            console.log("asdfasdf");
        }
    );
}

function showmylostthings() {
    var x = document.getElementsByClassName("account");
    var i;
    for (i = 0; i < x.length; i++) {
        //alert(x[i].innerHTML );
        if (x[i].innerHTML + "" == gettheaccount() + "") {
            //alert(x[i]);
            x[i].parentElement.style.display = "block";
        }
    }
}

function login() {
    var n, p;
    n = $("#number").val();
    p = $("#password").val();

    $.post("login.php", {
            number: n,
            password: p,
        },
        function(account) {
            if (account != "0") {
                //alert("1111111");
                $("#outsideWindow").css("display", "none");
                $(".register").css("display", "none");
                $("#rightTop2").css("display", "none");
                $("#rightTop3").css("display", "inline-block");
                changeloginornot(1);
                changeaccount(account);
                changepassword(p);
                loadme();
            } else {
                alert("密码错误");
            }
        }
    );

}

function register() {
    //alert("mot");
    var n, p, na, ph;
    n = $("#number2").val();
    p = $("#password2").val();
    na = $("#name2").val();
    ph = $("#phone2").val();
    if (n && p && na && ph) {
        //alert(n);alert(na);
        $.post("register.php", {
                number2: n,
                password2: p,
                name2: na,
                phone2: ph,
            },
            function(account) {
                //alert(loginStatus);
                if (account != "0") {
                    //alert("1111111");
                    $("#outsideWindow").css("display", "none");
                    $(".register").css("display", "none");
                    $("#rightTop2").css("display", "none");
                    $("#rightTop3").css("display", "inline-block");
                    changeloginornot(1);
                    changeaccount(account);
                    changepassword(p);
                    loadme();
                } else if (account == "0") { alert("有和你账号重名的用户,换个号吧") }
            }
        );
    } else { alert("是不是点错了,输全再注册") }
}

function publiclostthing() {
    var lostname, lostplace, losttime, subject;
    lostname = $("#lostname").val();
    lostplace = $("#lostplace").val();
    losttime = $("#losttime").val();
    subject = $("#subject").val();
    if (losttime && lostplace && lostname && subject) {
        $.post("publiclostthing.php", {
            ltname: lostname,
            ltplace: lostplace,
            lttime: losttime,
            ltsubject: subject,
            password: getpassword(),
            account: gettheaccount(),
        }, function(value) {
            console.log(value);
            if (value == 1) {
                alert("🐕发布成功🐕\n您可以通过点击自己的失物框改变为已找回状态\n╰（￣▽￣）╭");
                $(function() {
                    console.log("------**********开始了************---------");
                })
            } else alert("请按F5刷新页面,重新登陆");
        })
    } else {
        alert("请填写完整");
    }
}

function changename() {
    var newname;
    newname = $("#changename_text").val();
    if (newname) {
        $.post("changename.php", {
            newname: newname,
            password: getpassword(),
            account: gettheaccount(),
        }, function(data) {
            if (data == "1") {
                alert("修改成功");
                $("#myname").text(newname);
            } else {
                alert("修改失败");
            }
        })
    }
}

function changephone() {
    var newphone;
    newphone = $("#changephone_text").val();
    if (newphone) {
        $.post("changephone.php", {
            newphone: newphone,
            password: getpassword(),
            account: gettheaccount(),
        }, function(data) {
            //alert(data);
            if (data == "1") {
                alert("修改成功");
                $("#myphone").text(newphone);
            } else {
                alert("修改失败");
            }
        })
    }
}