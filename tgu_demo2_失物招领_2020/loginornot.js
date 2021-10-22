var loginornot=0;
var whatistheaccount="0";
var password="0";
function changeloginornot(value) {
    loginornot=value;
}
function ifloginornot() {
    return loginornot;
}
function changeaccount(value) {
    whatistheaccount=value;
    //alert(whatistheaccount);
}
function gettheaccount() {
    return whatistheaccount;
}
function getpassword() {
    return password;
}
function changepassword(p) {
    password=p;
}