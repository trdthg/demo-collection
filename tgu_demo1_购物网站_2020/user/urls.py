from django.urls import path

from . import views

urlpatterns = [

    # 身份验证
    path('userinfo', views.listuserinfo),


    path('login', views.login),

    path('register', views.register),

    path('whetherlogin', views.whetherlogin),

    path('test', views.displaygoods),

    path('test2', views.showthisstyle),

    # 个人主页区
    path('showmyinfo', views.showmyinfo),

    path('uploaduserimage', views.uploaduserimage),

    path('changeinfo', views.changeinfo),

    # 购物车区
    path('addtomyshoppingcar', views.addtomyshoppingcar),

    path('showmyshoppingcar', views.showmyshoppingcar),

    path('deletefrommyshoppingcar', views.deletefrommyshoppingcar),

    path('modifyamount', views.modifyamount),

    path('buy', views.buy),

    # 商品显示区
    path('displayall', views.listallitems),

    path('jumptoitem', views.jumptoitem),

    path('jumptostyle', views.jumptostyle),

    # 商家页面区
    path('showmymoney', views.sowmymoney),
    path('showmymill', views.showmymill),
    path('showmyitem', views.showmyitem),
    path('showmystyle', views.showmystyle),
    
    path('createnewmill', views.createnewmill),
    path('deletethismill', views.deletethismill),
    path('updatenewstyles', views.updatenewstyles),
    path('deletethisitem', views.deletethisitem),
    path('addnewstyle', views.addnewstyle),
    path('deletethisstyle', views.deletwthisstyle),

    path('modifystylename', views.modifystylename),
    path('modifystyleprice', views.modifystyleprice),
    path('modifystyleimage', views.modifystyleimage),

    path('search', views.search),
    path('search2', views.search2),
    path('attention', views.attention),


]