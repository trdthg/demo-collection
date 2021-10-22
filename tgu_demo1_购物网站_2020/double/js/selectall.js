function clearall() {
    var index = 0;
    var del = $(".operate");
    if (confirm("真的要清空吗？？？？")) {
        while (del[index]) {
            if ((del[index].parentNode).getElementsByTagName("input")[0].checked == 1)
                del[index].click();
            index++;
        }
    }
    wincow.location.href = document.URL;
}


function submit() {

    var cache = document.getElementsByClassName("goods");
    var i = 0;
    var data = new FormData();
    while (cache[i]) {
        console.log(cache[i].getElementsByTagName("input")[0].checked);
        if (cache[i].getElementsByTagName("input")[0].checked == 1) {
            data.append("cartid", cache[i].id);
            data.append("amount", cache[i].getElementsByTagName("input")[1].value);

            //console.log(data[n - 1].number);
        }
        i++;
    }
    var token = document.cookie.split(";")[0];
    data.append("token", token)
    $.ajax({
        url: "http://192.168.137.175/user/buy",
        type: "POST",
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            window.location.href = document.URL
        }
    })

}


function selectall() {
    if (document.getElementById("selectingall").checked == 1) {
        var cache = document.getElementsByClassName("goods")
        for (var i = 0; cache[i]; i++) {
            cache[i].getElementsByTagName("input")[0].checked = 1;
        }
    } else {
        var cache = document.getElementsByClassName("goods")

        for (var i = 0; cache[i]; i++) {
            cache[i].getElementsByTagName("input")[0].checked = 0;
        }
    }
}



function refresh() {
    var flag = 1;
    var goods = document.getElementsByClassName("goods")
    for (var i = 0; goods[i]; i++) {
        flag = flag && goods[i].getElementsByTagName("input")[0].checked;
    }
    if (flag) { document.getElementById("selectingall").checked = 1; } else { document.getElementById("selectingall").checked = 0; }
    console.log("changed");
    // setTimeout(refresh(), 9999);
}
$("input").click(function() { setTimeout(refresh(), 100); })
refresh();

$(".number>input").change(function() {
    var token = document.cookie.split(";")[0];

    var cartid = this.parentNode.parentNode.id;
    var newamount = $(this).val();
    $.ajax({
        url: "http://192.168.137.175/user/modifyamount",
        ret: "0",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
            token: token,
            cartid: cartid,
            newamount: newamount,
        }),
        success: function(data) {
            alert(data.msg)
        }

    })
})

function buy() {
    var token = document.cookie.split(";")[0];

    $.ajax({
        url: "http://192.168.137.175/user/buy",
        ret: "0",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
            token: token,
            cartid: cartid,
            amount: amount,
        }),
        success: function(data) {
            alert(data.msg)
        }

    })
}