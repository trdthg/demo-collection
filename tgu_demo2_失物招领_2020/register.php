<?php 
$number2 = isset($_POST['number2']) ? htmlspecialchars($_POST['number2']) : '';
$password2 = isset($_POST['password2']) ? htmlspecialchars($_POST['password2']) : '';
$name2 = isset($_POST['name2']) ? htmlspecialchars($_POST['name2']) : '';
$phone2 = isset($_POST['phone2']) ? htmlspecialchars($_POST['phone2']) : '';

$tryfindaccount=simplexml_load_file("account.xml");
$n=count($tryfindaccount->user);
//echo($num ." out". "<br>");
$nb=0;
for($i=0;$i<$n;$i++)
{
    global $number2,$password,$i,$tryfindaccount,$nb;
    //echo($num ."inner 1". "<br>");
    //echo($xml->user[$i]->number . "innerxml". "<br>");
    if($tryfindaccount->user[$i]->number==$number2)$nb=1;
}
if($nb==1){echo ("0");}
else
{$xml =new DOMDocument();
$xml->load('account.xml'); //读取XML文件

$user=$xml->createElement("user");
$num=$xml->createElement("number");
$pas=$xml->createElement("password");
$nam=$xml->createElement("name");
$pho=$xml->createElement("phone");

$num->nodeValue=$number2;
$pas->nodeValue=$password2;
$nam->nodeValue=$name2;
$pho->nodeValue=$phone2;

$user->appendchild($num);
$user->appendchild($pas);
$user->appendchild($nam);
$user->appendchild($pho);

$xml->getElementsByTagName("note")->item(0)->appendchild($user);


//$xml->getElementsByTagName("user")->item(0)->getElementsByTagName("number")->item(0)->nodeValue="$number2";
//$xml->getElementsByTagName("user")->item(0)->getElementsByTagName("password")->item(0)->nodeValue="$password2";
//$xml->getElementsByTagName("user")->item(0)->getElementsByTagName("name")->item(0)->nodeValue="$name2";
//$xml->getElementsByTagName("user")->item(0)->getElementsByTagName("phone")->item(0)->nodeValue="$phone2";

$xml->save("account.xml");
echo ($number2);}
?>
