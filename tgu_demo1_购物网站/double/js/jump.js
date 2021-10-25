function jumptologinorhome() {
    var token = document.cookie.split(";")[0];
    $.ajax({
        url: "http://192.168.137.175/user/whetherlogin",
        ret: "0",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
            token: token,
        }),
        success: function(data) {
            if (data.ret != "0") {
                window.location.href = "http://192.168.137.175/login.html"
            } else {
                window.location.href = "http://192.168.137.175/home.html"
            }
        }
    })
}

function jumptomycart() {
    var token = document.cookie.split(";")[0];
    $.ajax({
        url: "http://192.168.137.175/user/whetherlogin",
        ret: "0",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
            token: token,
        }),
        success: function(data) {
            if (data.ret != "0") {
                window.location.href = "http://192.168.137.175/login.html"
            } else {
                window.location.href = "http://192.168.137.175/shoppingcar.html"
            }
        }
    })
}

function jumptomymills() {
    var token = document.cookie.split(";")[0];
    $.ajax({
        url: "http://192.168.137.175/user/whetherlogin",
        ret: "0",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
            token: token,
        }),
        success: function(data) {
            if (data.ret != "0") {
                window.location.href = "http://192.168.137.175/login.html"
            } else {
                window.location.href = "http://192.168.137.175/mymill.html"
            }
        }
    })
}

function jumptoindex() {
    window.location.href = "http://192.168.137.175/index.html"

}