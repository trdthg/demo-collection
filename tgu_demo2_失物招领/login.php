<?php 
$num = isset($_POST['number']) ? htmlspecialchars($_POST['number']) : '';
$password = isset($_POST['password']) ? htmlspecialchars($_POST['password']) : '';
$xmlDoc = new DOMDocument();
$xmlDoc->load("account.xml");

$xml=simplexml_load_file("account.xml");
$n=count($xml->user);
//echo($num ." out". "<br>");
$nb=0;
for($i=0;$i<$n;$i++)
{
    global $num,$password,$i,$xml,$nb;
    //echo($num ."inner 1". "<br>");
    //echo($xml->user[$i]->number . "innerxml". "<br>");
    if($xml->user[$i]->number==$num && $xml->user[$i]->password==$password)$nb=1;
}
if($nb)
echo($num);
else echo("0");
?>