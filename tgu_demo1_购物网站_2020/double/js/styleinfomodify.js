$(".goods > input[type=\"text\"]").change(function() {
    var token = document.cookie.split(";")[0];
    styleid = $(this.parentNode).attr('id')
    var newname = $(this).val();
    $.ajax({
        url: "http://192.168.137.175/user/modifystylename",
        ret: "0",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
            styleid: styleid,
            token: token,
            newname: newname,
        }),
        success: function(data) {
            alert(data.msg)
        }

    })
})

$('.goods > input[type=\"number\"]').change(function() {
    var token = document.cookie.split(";")[0];
    var newprice = $(this).val();
    styleid = $(this.parentNode).attr('id')

    $.ajax({
        url: "http://192.168.137.175/user/modifystyleprice",
        ret: "0",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
            styleid: styleid,
            token: token,
            newprice: newprice,
        }),
        success: function(data) {
            alert(data.msg)
        }

    })
})

function updateimage(styleid) {
    //$("#updateimage").click(function() {
    var token = document.cookie.split(";")[0];
    var formData = new FormData
    formData.append('token', token)
    console.log(styleid)
    formData.append('image', $("#img_" + styleid)[0].files[0])
    formData.append('styleid', styleid)

    $.ajax({
            url: "http://192.168.137.175/user/modifystyleimage",
            ret: "0",
            type: "POST",
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            success: function(data) {
                alert(data.msg)
            }

        })
        //})
}