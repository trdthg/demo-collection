<?php

$num = isset($_POST['account']) ? htmlspecialchars($_POST['account']) : '';
$password = isset($_POST['password']) ? htmlspecialchars($_POST['password']) : '';
$xmlDoc = new DOMDocument();
$xmlDoc->load("account.xml");

$xml=simplexml_load_file("account.xml");
$n=count($xml->user);
//echo($num ." out". "<br>");
$nb=0;
$i=0;
for(;$i<$n;$i++)
{
    global $num,$password,$i,$xml,$nb;
    //echo($num ."inner 1". "<br>");
    //echo($xml->user[$i]->number . "innerxml". "<br>");
    if($xml->user[$i]->number==$num && $xml->user[$i]->password==$password){
        $nb=1;
        break;
    }
}
if($nb){
    $arr = array('account'=>$num,'name'=>"".$xml->user[$i]->name,'phone'=>"".$xml->user[$i]->phone);
    echo json_encode($arr);
}

else {

}
?>