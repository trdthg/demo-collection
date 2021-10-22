function load_card(card,data){
	var card_link=card.getElementsByClassName("card_link")[0]
	var card_link_a=card_link.getElementsByTagName("a")[0];
	card_link_a.innerText=data.card_title;
	card_link_a.setAttribute("href",data.card_link);
	var card_outline=card.getElementsByClassName("card_outline")[0];
	card_outline.innerText=data.card_outline;
	for(var i=0;i<data.card_tags.length;i++){
		var card_tags=card.getElementsByClassName("card_tags")[0];
		card_tags.innerHTML+="<span><a href='#'>"+data.card_tags[i]+"</a></span>";
	}
	var card_release_time=card.getElementsByClassName("card_release_time")[0];
	card_release_time.innerHTML=data.card_release_time;
	var card_auther=card.getElementsByClassName("card_auther")[0];
	card_auther.innerHTML=data.card_auther;
}
var include_path = "html/single_page/";

function top_level_path() {
	var str = window.location.href;
	var main_path_name = "Forum-1";
	var index = str.indexOf(main_path_name);
	index += main_path_name.length;
	return str.substring(0, index);
}
(function set_include_path() {
	include_path = top_level_path() + "/" + include_path;
	console.log(include_path);
})()