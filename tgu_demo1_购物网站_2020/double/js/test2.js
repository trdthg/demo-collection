$("a").click(function() {
    var styleid = $(this).attr("id")

    $.ajax({
        url: "http://192.168.137.175/user/jumptostyle",
        type: "POST",
        ret: '0',
        dataType: "json",
        data: JSON.stringify({
            styleid: styleid,
        }),
        success: function(data) {
            if (data.ret == "0") {
                console.log(data)
                window.location.href = "http://192.168.137.175/goods.html?styleid=" + styleid
            } else {
                console.log(data)
            }
        }
    })
})