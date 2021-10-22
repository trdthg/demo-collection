<?php
$ltname = isset($_POST['ltname']) ? htmlspecialchars($_POST['ltname']) : '';
$ltplace = isset($_POST['ltplace']) ? htmlspecialchars($_POST['ltplace']) : '';
$lttime = isset($_POST['lttime']) ? htmlspecialchars($_POST['lttime']) : '';
$ltsubject = isset($_POST['ltsubject']) ? htmlspecialchars($_POST['ltsubject']) : '';
$account = isset($_POST['account']) ? htmlspecialchars($_POST['account']) : '';
$password = isset($_POST['password']) ? htmlspecialchars($_POST['password']) : '';

$xml =new DOMDocument();
$xml->load('user.xml');

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
    if($proving->user[$i]->number==$account && $proving->user[$i]->password==$password)$nb=1;
}
if($nb)
{
        //获取姓名和手机号
    $xmlDoc=simplexml_load_file("account.xml");
    $n=count($xmlDoc->user);
    $name=0;
    $phone=0;
    //echo($num ." out". "<br>");
    for($i=0;$i<$n;$i++)
    {
        global $account,$i,$xmlDoc,$name,$phone;
        //echo($num ."inner 1". "<br>");
        //echo($xml->user[$i]->number . "innerxml". "<br>");
        if($xmlDoc->user[$i]->number==$account)
        {
            $name=$xmlDoc->user[$i]->name;
            $phone=$xmlDoc->user[$i]->phone;
            break;
        }
    }



    //5挂4
    //创建子节点/添加元素
    $root5_1=$xml->createElement("div");
    $root5_2=$xml->createElement("div");
    $root5_3=$xml->createElement("div");
    $root5_4=$xml->createElement("div");
    $root5_1->setAttribute("class","expandContentMiddle1");
    $root5_2->setAttribute("class","expandContentMiddle2");
    $root5_3->setAttribute("class","expandContentMiddle2");
    $root5_4->setAttribute("class","expandContentBottom");

    //为节点赋值
    $root5_1->nodeValue = "丢失物品: " . $ltname ;
    $root5_2->nodeValue = "丢失地点: " . $ltplace;
    $root5_3->nodeValue = "丢失时间: " . $lttime;
    $root5_4->nodeValue = "联系人: " . $name ." ". "联系电话: " . $phone;
    //挂载节点
    $root4_1=$xml->createElement("div");
    $root4_2=$xml->createElement("div");
    $root4_1->appendchild($root5_1);
    $root4_1->appendchild($root5_2);
    $root4_1->appendchild($root5_3);
    $root4_1->appendchild($root5_4);

    //4挂3
    //创建子节点/添加元素
    $root4_1->setAttribute("class","expandContentMiddle");
    $root4_2->setAttribute("class","expandContentHide");
    $root4_2->setAttribute("id","expandContentHide-1");

    //为节点赋值
    $root4_2->nodeValue = "详细信息: " . $ltsubject;

    //挂载节点
    $root3_1=$xml->createElement("div");
    $root3_2=$xml->createElement("div");
    $root3_2->appendchild($root4_1);
    $root3_2->appendchild($root4_2);

    //3挂2
    //创建子节点/添加元素
    $root3_1->setAttribute("class","expandContentTop expandContentTop1");
    $root3_2->setAttribute("class","expandContent");

    //为节点赋值
    $root3_1->nodeValue = "丢失 (º﹃º )";

    //挂载节点
    $root2_1=$xml->createElement("div");
    $root2_2=$xml->createElement("div");
    $root2_2->appendchild($root3_1);
    $root2_2->appendchild($root3_2);

    //2挂1
    //创建子节点/添加元素
    $root2_1->setAttribute("class","account");
    $root2_2->setAttribute("class","expand1");

    //为节点赋值
    $root2_1->nodeValue = $account;

    //挂载节点
    $root1 = $xml->createElement("span");
    $root1->appendchild($root2_1);
    $root1->appendchild($root2_2);
    //1挂0
    //创建子节点/添加元素
    $root1->setAttribute("class","middleSquare");
    $root1->setAttribute("id",time()."".$account);

    //为节点赋值

    //挂载节点
    $xml->getElementsByTagName("root")->item(0)->appendchild($root1);


    //保存文件
    $xml->save("user.xml");
    echo ("1");
}
else echo("0");


?>