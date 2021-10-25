    $(".goods").click(function() {
        var itemid = $(this).attr("id")

        $.ajax({
            url: "http://192.168.137.175/user/jumptoitem",
            type: "POST",
            ret: '0',
            dataType: "json",
            data: JSON.stringify({
                itemid: $(this).attr("id"),
            }),
            success: function(data) {
                if (data.ret == "0") {
                    console.log(data)
                    window.location.href = "http://192.168.137.175/goods.html?itemid=" + itemid
                } else {
                    console.log(data)
                }
            }
        })
    })