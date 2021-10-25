<?php
$account = isset($_POST['account']) ? htmlspecialchars($_POST['account']) : '';
$password = isset($_POST['password']) ? htmlspecialchars($_POST['password']) : '';
$newphone = isset($_POST['newphone']) ? htmlspecialchars($_POST['newphone']) : '';
//安全验证
//echo("jdsljfdlajf");
$xml=simplexml_load_file("account.xml");
$n=count($xml->user);
//echo($num ." out". "<br>");
$nb=0;
for($i=0;$i<$n;$i++)
{
    global $account,$password,$i,$xml,$nb;
    //echo($num ."inner 1". "<br>");
    //echo($xml->user[$i]->number . "innerxml". "<br>");
    if($xml->user[$i]->number==$account && $xml->user[$i]->password==$password){
        $nb=1;
        break;
    }
}
if($nb){
    $xmlDoc = new DOMDocument();
    $xmlDoc->load("account.xml");
    for($i=0;$i<$n;$i++){
        global $newphone;
        $temp = $xmlDoc->getElementsByTagName("user")->item($i);
        //获取div的账户
        $temp_account = $temp->getElementsByTagName("number")->item("0")->nodeValue;
        
        if($account == $temp_account){
            //如果匹配,则修改姓名
            $temp->getElementsByTagName("phone")->item("0")->nodeValue=$newphone;
            echo("1");
            break;
        }    
    }
    $xmlDoc->save("account.xml");
}else echo("0");
?>