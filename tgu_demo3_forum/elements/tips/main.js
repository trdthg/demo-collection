function add_tip(_node, str, mode) { // primary success info warning danger
	var  time_to_live=5000;
	var Anime_time=500;
	var tip_container = _node.getElementsByClassName("tip_container")[0];
	var mode_to_code = {
		primary: 1,
		success: 2,
		info: 3,
		warning: 4,
		danger: 5
	};
	var background_color = [
		"",
		"#337ab7",
		"#dff0d8",
		"#d9edf7",
		"#fcf8e3",
		"#f2dede",
	];
	var color = ["","white", "#5f5f5f", "#5f5f5f", "#5f5f5f", "#5f5f5f"];
	var div = "<div class='tip_content' style='display:none; background-color: " + background_color[mode_to_code[mode]] + ";color:" +
		color[mode_to_code[mode]] + ";'>";
	var _div = "</div>";
	var element = div + str + _div;
	var jquery_obj= $(element);
	$(tip_container).append(jquery_obj);
	jquery_obj.show(Anime_time);
	setTimeout(function(){jquery_obj.hide(Anime_time);setTimeout(function(){jquery_obj.remove()},Anime_time+500)},time_to_live);
}
// add_tip(document.getElementById("test"),23333,"primary")
// (function(){
// 	add_tip(document.getElementById("test"),23333,"primary");
// 	add_tip(document.getElementById("test"),23333,"primary");
// 	add_tip(document.getElementById("test"),23333,"primary");
// 	add_tip(document.getElementById("test"),23333,"primary");
// 	add_tip(document.getElementById("test"),23333,"primary");
// })()
