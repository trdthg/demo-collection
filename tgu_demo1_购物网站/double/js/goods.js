// alert("1")
$(document).ready(function() {

    function showstyles() {
        var thisURL = document.URL;
        var itemid = thisURL.split('?')[1];
        var itemid = itemid.split("=")[1];
        // 获取了itemid
        $.ajax({
            url: "http://192.168.137.175/user/jumptoitem",
            type: "POST",
            ret: '0',
            dataType: "json",
            data: JSON.stringify({
                itemid: itemid,
            }),
            success: function(data) {
                if (data.ret == "0") {
                    $(".left img").attr("src", data.data2.image)
                    $(".left img").attr("id", data.data2.id)
                    $("#change p").text(data.data2.name)
                    $("#price2").text(data.data2.price)
                    console.log(data)
                    $("#change").append(data.data)
                    $("#bottom").append("<script src=\".\/js\/test2.js\"><\/script>")
                    $("#bottom").append("<script src=\".\/js\/test3.js\"><\/script>")
                } else {
                    console.log(data)
                    alert("没有此物")
                }
            }
        })
    }

    function showthisstyle() {
        var thisURL = document.URL;
        var styleid = thisURL.split('?')[1];
        var styleid = styleid.split("=")[1];
        // 获取了itemid
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
                    $(".left img").attr("src", data.data2.image)
                    $(".left img").attr("id", data.data2.id)
                    $("#change p").text(data.data2.name)
                    $("#price2").text(data.data2.price)
                    console.log(data)
                    $("#change").append(data.data)
                    $("#bottom").append("<script src=\".\/js\/test2.js\"><\/script>")
                    $("#bottom").append("<script src=\".\/js\/test3.js\"><\/script>")


                } else {
                    console.log(data)
                    alert("没有此物")
                }
            }
        })
    }

    function itemorstyle() {
        var thisURL = document.URL;
        var text = thisURL.split('?')[1];
        var text = text.split("=")[0];
        if (text == "itemid") {
            showstyles()
        } else if (text == "styleid") {
            showthisstyle()
        }
    }
    itemorstyle()
        // $("img").click(function() {
        //     alert("111")
        // })


    // $("a").click(function() {
    //     $(".left img").attr("src", "sss")
    //     $("#change p:first").text($(this).text())
    //     $("#change p:first").text($(this).text())
    //     alert("1")
    // })


})