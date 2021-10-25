// class="replace" load_name="???"
var include_path = "elements/";

function load_all(fun) {
	var arr = document.getElementsByClassName("replace");
	for (var i = 0; arr.length;) {
		new replace(arr[i]).load(fun);
	}
}
class replace {
	constructor(_node) {
		this.node = _node;
	}
	_loadCss(url) {
		var load_position = $("#loadCss").get(0);
		var link = document.createElement('link');
		link.type = 'text/css';
		link.rel = 'stylesheet';
		link.href = url;
		load_position.appendChild(link);
	}
	_loadScript(url) {
		var load_position = $("#loadJs").get(0);
		var script = document.createElement("script");
		script.type = "text/javascript";
		script.src = url;
		load_position.appendChild(script);
	}
	load(fun) {
		$(this.node).removeClass("replace"); //移除类
		var load_name = $(this.node).attr("load_name");
		var _node = this.node;
		var path = include_path + load_name + "/";
		$.get(path + "main.html", function(data) {
			_node.innerHTML = data;
			fun();
		})
		var check ;
		if($("#_check").get(0)==undefined){
			$("body").append($('<div id="loadCss" style="display: none;"></div>\
						<div id="loadJs" style="display: none;"></div>\
						<div id="_check" style="display: none;"></div>'));
		}
		var check=$("#_check").get(0);
		if (check.getElementsByTagName(load_name).length == 0) {
			var __node = document.createElement(load_name);
			console.log(__node);
			check.appendChild(__node);
			this._loadCss(path + "main.css");
			this._loadScript(path + "main.js");
		}
	}
}

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
