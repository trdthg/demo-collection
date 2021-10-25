$("#add").click(function() {

    function addtomyshoppingcar() {
        var token = document.cookie.split(";")[0];
        var styleid = $(".left img").attr("id")
        $.ajax({
            url: "http://192.168.137.175/user/addtomyshoppingcar",
            ret: "0",
            type: "POST",
            dataType: "json",
            data: JSON.stringify({
                token: token,
                styleid: styleid,
                amount: $("#btn").val(),
                // itemname = $(".right p:first").text()
            }),
            success: function(data) {
                alert(data.msg)
                if (data.ret == 1) {
                    window.location.href = "http://192.168.137.175/login.html"
                }

            }
        })
    }
    addtomyshoppingcar()
})