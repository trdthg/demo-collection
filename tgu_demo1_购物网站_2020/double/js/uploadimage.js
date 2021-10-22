$("#submit2").click(function() {
    var formData = new FormData();
    var token = document.cookie.split(";")[0];
    formData.append("token", token);
    formData.append("file", $("#file")[0].files[0]);
    $.ajax({
        url: "http://192.168.137.175/user/uploaduserimage",
        type: "POST",
        data: formData,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            alert(data.msg)
        }
    })
})