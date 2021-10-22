class USER {
	constructor() {
		this.username="";
		this.id="";
		this.tocken="";
		this.avatar="";
	}
	sign_in(username,id,tocken,avatar){
		this.username=username;
		this.id=id;
		this.tocken=tocken;
		this.avatar=avatar;
	}
}
var user=new USER();