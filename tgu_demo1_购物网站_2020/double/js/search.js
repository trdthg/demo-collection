// $("#searchinput").change(
function searchcue() {
    input = $("#searchinput").val()
    $.ajax({
        url: "http://192.168.137.175/user/search",
        ret: "0",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
            input: input,
        }),
        success: function(data) {
            $("#bottom").html(data.data)
            console.log(data.data);
            $("#bottom").append("<script src=\"\.\/js\/test.js\"><\/script>")

        }
    })
}
// )