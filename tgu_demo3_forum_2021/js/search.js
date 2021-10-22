function search(link,search_limit,str,tag,index,fun){//请求地址，搜索数量限制，搜索内容，搜索标签，搜索页码,发回调函数
	var cards=3;
	var result=new Array();
	for(var i=0;i<search_limit;i++)
    $.get(link+"/card"+Math.ceil(Math.random()*cards)+".json",function(data){
		result.push(data);
		if(result.length==search_limit){fun(result);}
    })
		
}