<?php

$account = isset($_POST['account']) ? htmlspecialchars($_POST['account']) : '';
$password = isset($_POST['password']) ? htmlspecialchars($_POST['password']) : '';
$id = isset($_POST['id']) ? htmlspecialchars($_POST['id']) : '';
//安全验证
$proving = new DOMDocument();
$proving=simplexml_load_file("account.xml");
$n=count($proving->user);
//echo($num ." out". "<br>");
$nb=0;
for($i=0;$i<$n;$i++)
{
    global $account,$password,$i,$proving,$nb;
    //echo($num ."inner 1". "<br>");
    //echo($xml->user[$i]->number . "innerxml". "<br>");
    if($proving->user[$i]->number==$account && $proving->user[$i]->password==$password)
    {$nb=1;/*echo("nb");*/}
    //echo($account."   ".$password."  ".$id."\n");
    //echo($proving->user[$i]->number."   ".$proving->user[$i]->password."  ".$id."\n");
}
if($nb)
{
    //修改颜色执行
    //echo("123456789");
    $xml =new DOMDocument();
    $xml->load('user.xml'); //读取XML文件

    $proving2 = new DOMDocument();
    $proving2=simplexml_load_file("user.xml");
    $n2=count($proving2->span);

    for($i=0;$i<$n2;$i++){
        $temp = $xml->getElementsByTagName("span")->item($i);
        //获取div的账户
        $temp_account = $temp->getElementsByTagName("div")->item("0")->nodeValue;
        //获取div的id
        foreach( $proving2->span[$i]->attributes() AS $a => $b ){
            if($a=="id"){
               if($b == $id && $account == $temp_account){
                //如果匹配,则修改颜色和内容
                $temp_Top = $temp->getElementsByTagName("div")->item("2")->nodeValue="已找回 []~(￣▽￣)~*";
                $temp_Top_attribute = $temp->getElementsByTagName("div")->item("2")->setAttribute("class","expandContentTop expandContentTop2");
                
               }
            }
        }
        
        var_dump ($temp_id);
        //与 用户点击的的div的id 和 用户登录账户对比
        //if()
    }
    $xml->save("user.xml");
}
?>