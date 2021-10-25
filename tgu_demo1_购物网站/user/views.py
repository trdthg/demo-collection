from django.shortcuts import render
from . import models
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from user.models import User
from user.models import Userinfo
from user.models import Item
from user.models import Style
from user.models import Cart
from user.models import Mill
from user.models import Keyword
# 生成Token
import os
import base64
import random
import time
import json
import base64
import hashlib
import hmac
import jieba
import jieba.analyse
# from asys.settings import MEDIA_ROOT

def listallitems2(request):
    # 返回一个 QuerySet 对象 ，包含所有的表记录
    # 每条表记录都是是一个dict对象，
    # key 是字段名，value 是 字段值
    qs = models.Item.objects.values('id','image', 'name', 'price', 'mill__name')
    # qs =list(qs)
    # return HttpResponse(qs)

        #     <div class="salevol">销量：2333</div>
    retStr = ''
    i=0
    # 保证从所选页面循环30此
    page = 1
    i = 1
    for item in  qs:
        if i<page: 
            i += 1
            continue
        # user = User.objects.filter(account=account).values()
        # userid = user[0]['id']
        retStr += f'<div class="goods" id={item["id"]}>'
        for name,value in item.items():
            
            if name=='image':
                retStr += f'<img src="{value}" alt="{value}"> ' 
            elif name=='name':
                retStr += f'<div class= "goodsname"> {value}</div>' 
            elif name=='price':
                retStr += f'<div class="price">&yen;{value}</div>'
            elif name=='mill__name':
                retStr += f'<div class="sellername"> <svg t="1605618008222" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2963" width="16" height="16"><path d="M889.583614 155.560962c-1.786693-7.514137-2.490727-11.777231-4.848424-15.61463l-0.001024-0.002046h-0.001023c-4.973268-7.223518-13.295817-11.962449-22.728654-11.96245h-700.596356c-9.432837 0-17.756409 4.738931-22.728654 11.96245h-0.001023l-0.001023 0.002046c-2.358721 3.837398-3.061732 8.100492-4.848425 15.61463-1.786693 7.514137-69.845765 292.554032-69.845765 292.554032v7.653307c0 46.38954 26.00835 86.708827 63.960731 106.651019v301.108872c0 17.662265 14.3181 31.980365 31.980365 31.980365h703.567014c17.662265 0 31.980365-14.3181 31.980365-31.980365V562.41932c37.95238-19.942191 63.960731-60.261479 63.960731-106.651019v-7.653307c-0.002047 0-68.062142-285.039895-69.848835-292.554032zM383.78485 831.54885V703.627389h255.842922v127.921461H383.78485z m319.80263-159.901827c0-17.662265-14.3181-31.980365-31.980366-31.980365H351.804485c-17.662265 0-31.980365 14.3181-31.980366 31.980365v159.901827H191.902658v-256.287038c28.062126-2.434445 53.350069-14.914688 72.362075-33.897017 21.267373 21.233604 50.384527 34.342156 82.45699 34.342156 32.072463 0 61.189617-13.107529 82.458013-34.342156 21.055548 21.022803 49.807383 34.072003 81.502246 34.329876v0.011256l0.068561 0.001024c0.148379 0 0.294712-0.005117 0.443092-0.005117 0.147356 0.001023 0.294712 0.005117 0.442068 0.005117l0.068562-0.001024v-0.011256c31.715329-0.257873 61.470003-13.30605 82.525551-34.329876 21.268396 21.233604 50.384527 34.342156 82.458014 34.342156 32.072463 0 61.189617-13.107529 82.45699-34.342156 19.012006 18.98233 44.299949 31.461549 72.362074 33.897017v256.287038H703.58748v-159.901827z m132.265396-159.911036c-29.943986 0-54.220902-24.536836-54.220902-54.801117 0-15.131629-12.108782-27.370371-27.080776-27.370371-14.971993 0-27.080775 12.238742-27.080775 27.370371 0 30.264281-24.276916 54.801117-54.220902 54.801117-29.943986 0-54.220902-24.536836-54.220902-54.801117 0-15.131629-12.108782-27.370371-27.080776-27.370371-14.971993 0-27.080775 12.238742-27.080775 27.370371 0 30.264281-24.276916 54.801117-54.220902 54.801117-29.943986 0-54.220902-24.536836-54.220902-54.801117 0-15.131629-12.108782-27.370371-27.080776-27.370371-14.971993 0-27.080775 12.238742-27.080775 27.370371 0 30.264281-24.276916 54.801117-54.220902 54.801117-29.943986 0-54.220902-24.536836-54.220902-54.801117 0-15.131629-12.108782-27.370371-27.080775-27.370371-14.971993 0-27.080775 12.238742-27.080776 27.370371 0 30.264281-24.276916 54.801117-54.220902 54.801117s-57.494459-33.68724-57.494459-63.951521l62.50559-255.842922h640.513955l64.508199 255.842922c-0.00307 30.264281-29.67588 63.951521-59.619865 63.951521z" p-id="2964" fill="#d81e06"></path></svg>{value}</div>'
        retStr += '<div class="salevol">销量：2333</div>'           
        retStr += '</div>'
        if i==page+30:
            i=1
            break
    return JsonResponse({'ret':0, 'data':retStr})
def listallitems(request):
    retStr = ''
    qs = Item.objects.values('id','image', 'name', 'price', 'mill','amount')
    for item in qs:
        
        itemname = item['name']  #主页显示
        
        mill = Mill.objects.get(id=item['mill'])
        millname = mill.name
        
        itemid = Item.objects.get(name=itemname)
        # item = Style.objects.get(id=itemid.id)
        styles = Style.objects.filter(item=itemid).values()
        for style in styles:
            styleprice = style['price']
            imagepath = style['image'].split("/")[1] + "/" + style['image'].split("/")[2] 
            retStr += f'<div class="goods" id={item["id"]}>'
            retStr += f'<img src={imagepath} alt="无图">' 
            retStr += f'<div class= "goodsname"> {itemname}</div>' 
            retStr += f'<div class="price">&yen;{styleprice}</div>'
            retStr += f'<div class="sellername"> <svg t="1605618008222" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2963" width="16" height="16"><path d="M889.583614 155.560962c-1.786693-7.514137-2.490727-11.777231-4.848424-15.61463l-0.001024-0.002046h-0.001023c-4.973268-7.223518-13.295817-11.962449-22.728654-11.96245h-700.596356c-9.432837 0-17.756409 4.738931-22.728654 11.96245h-0.001023l-0.001023 0.002046c-2.358721 3.837398-3.061732 8.100492-4.848425 15.61463-1.786693 7.514137-69.845765 292.554032-69.845765 292.554032v7.653307c0 46.38954 26.00835 86.708827 63.960731 106.651019v301.108872c0 17.662265 14.3181 31.980365 31.980365 31.980365h703.567014c17.662265 0 31.980365-14.3181 31.980365-31.980365V562.41932c37.95238-19.942191 63.960731-60.261479 63.960731-106.651019v-7.653307c-0.002047 0-68.062142-285.039895-69.848835-292.554032zM383.78485 831.54885V703.627389h255.842922v127.921461H383.78485z m319.80263-159.901827c0-17.662265-14.3181-31.980365-31.980366-31.980365H351.804485c-17.662265 0-31.980365 14.3181-31.980366 31.980365v159.901827H191.902658v-256.287038c28.062126-2.434445 53.350069-14.914688 72.362075-33.897017 21.267373 21.233604 50.384527 34.342156 82.45699 34.342156 32.072463 0 61.189617-13.107529 82.458013-34.342156 21.055548 21.022803 49.807383 34.072003 81.502246 34.329876v0.011256l0.068561 0.001024c0.148379 0 0.294712-0.005117 0.443092-0.005117 0.147356 0.001023 0.294712 0.005117 0.442068 0.005117l0.068562-0.001024v-0.011256c31.715329-0.257873 61.470003-13.30605 82.525551-34.329876 21.268396 21.233604 50.384527 34.342156 82.458014 34.342156 32.072463 0 61.189617-13.107529 82.45699-34.342156 19.012006 18.98233 44.299949 31.461549 72.362074 33.897017v256.287038H703.58748v-159.901827z m132.265396-159.911036c-29.943986 0-54.220902-24.536836-54.220902-54.801117 0-15.131629-12.108782-27.370371-27.080776-27.370371-14.971993 0-27.080775 12.238742-27.080775 27.370371 0 30.264281-24.276916 54.801117-54.220902 54.801117-29.943986 0-54.220902-24.536836-54.220902-54.801117 0-15.131629-12.108782-27.370371-27.080776-27.370371-14.971993 0-27.080775 12.238742-27.080775 27.370371 0 30.264281-24.276916 54.801117-54.220902 54.801117-29.943986 0-54.220902-24.536836-54.220902-54.801117 0-15.131629-12.108782-27.370371-27.080776-27.370371-14.971993 0-27.080775 12.238742-27.080775 27.370371 0 30.264281-24.276916 54.801117-54.220902 54.801117-29.943986 0-54.220902-24.536836-54.220902-54.801117 0-15.131629-12.108782-27.370371-27.080775-27.370371-14.971993 0-27.080775 12.238742-27.080776 27.370371 0 30.264281-24.276916 54.801117-54.220902 54.801117s-57.494459-33.68724-57.494459-63.951521l62.50559-255.842922h640.513955l64.508199 255.842922c-0.00307 30.264281-29.67588 63.951521-59.619865 63.951521z" p-id="2964" fill="#d81e06"></path></svg>{millname}</div>'
            retStr += f'<div class="salevol">销量：{item["amount"]}</div>'           
            retStr += f'</div>'
            break
        # style = Style.objects.get(item=item['id']) 
        # styleprice = style.price
        # styleimage = style.im

    return JsonResponse({'ret':0, 'data':retStr})
def search(request):
    if request.method=="POST":
        info = json.loads(request.body.decode())
        inputo = info['input']
        if inputo=="":
            return JsonResponse({'ret':'0','msg':'您未输入'})
        temp = inputo
        inputo = jieba.analyse.textrank(inputo,topK=20, withWeight=True, allowPOS=('n','nr','ns'))
        if inputo == []: 
            inputo = [(temp,1.0)]
        retStr = ''
        for inputkeyword in inputo:
            for word in inputkeyword:
                print(word)
                if type(word)==type(""):
                    keywords = Keyword.objects.filter(word__contains=word).values()
                    for keyword in keywords:
                        item = Item.objects.get(name=keyword['itemname'])
                        styles = Style.objects.filter(item=item).values()
                        for style in styles:
                            styleprice = style['price']
                            imagepath = style['image'].split("/")[1] + "/" + style['image'].split("/")[2] 
                            retStr += f'<div class="goods" id={item.id}>'
                            retStr += f'<img src={imagepath} alt="无图">' 
                            retStr += f'<div class= "goodsname"> {item.name}</div>' 
                            retStr += f'<div class="price">&yen;{styleprice}</div>'
                            retStr += f'<div class="sellername"> <svg t="1605618008222" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2963" width="16" height="16"><path d="M889.583614 155.560962c-1.786693-7.514137-2.490727-11.777231-4.848424-15.61463l-0.001024-0.002046h-0.001023c-4.973268-7.223518-13.295817-11.962449-22.728654-11.96245h-700.596356c-9.432837 0-17.756409 4.738931-22.728654 11.96245h-0.001023l-0.001023 0.002046c-2.358721 3.837398-3.061732 8.100492-4.848425 15.61463-1.786693 7.514137-69.845765 292.554032-69.845765 292.554032v7.653307c0 46.38954 26.00835 86.708827 63.960731 106.651019v301.108872c0 17.662265 14.3181 31.980365 31.980365 31.980365h703.567014c17.662265 0 31.980365-14.3181 31.980365-31.980365V562.41932c37.95238-19.942191 63.960731-60.261479 63.960731-106.651019v-7.653307c-0.002047 0-68.062142-285.039895-69.848835-292.554032zM383.78485 831.54885V703.627389h255.842922v127.921461H383.78485z m319.80263-159.901827c0-17.662265-14.3181-31.980365-31.980366-31.980365H351.804485c-17.662265 0-31.980365 14.3181-31.980366 31.980365v159.901827H191.902658v-256.287038c28.062126-2.434445 53.350069-14.914688 72.362075-33.897017 21.267373 21.233604 50.384527 34.342156 82.45699 34.342156 32.072463 0 61.189617-13.107529 82.458013-34.342156 21.055548 21.022803 49.807383 34.072003 81.502246 34.329876v0.011256l0.068561 0.001024c0.148379 0 0.294712-0.005117 0.443092-0.005117 0.147356 0.001023 0.294712 0.005117 0.442068 0.005117l0.068562-0.001024v-0.011256c31.715329-0.257873 61.470003-13.30605 82.525551-34.329876 21.268396 21.233604 50.384527 34.342156 82.458014 34.342156 32.072463 0 61.189617-13.107529 82.45699-34.342156 19.012006 18.98233 44.299949 31.461549 72.362074 33.897017v256.287038H703.58748v-159.901827z m132.265396-159.911036c-29.943986 0-54.220902-24.536836-54.220902-54.801117 0-15.131629-12.108782-27.370371-27.080776-27.370371-14.971993 0-27.080775 12.238742-27.080775 27.370371 0 30.264281-24.276916 54.801117-54.220902 54.801117-29.943986 0-54.220902-24.536836-54.220902-54.801117 0-15.131629-12.108782-27.370371-27.080776-27.370371-14.971993 0-27.080775 12.238742-27.080775 27.370371 0 30.264281-24.276916 54.801117-54.220902 54.801117-29.943986 0-54.220902-24.536836-54.220902-54.801117 0-15.131629-12.108782-27.370371-27.080776-27.370371-14.971993 0-27.080775 12.238742-27.080775 27.370371 0 30.264281-24.276916 54.801117-54.220902 54.801117-29.943986 0-54.220902-24.536836-54.220902-54.801117 0-15.131629-12.108782-27.370371-27.080775-27.370371-14.971993 0-27.080775 12.238742-27.080776 27.370371 0 30.264281-24.276916 54.801117-54.220902 54.801117s-57.494459-33.68724-57.494459-63.951521l62.50559-255.842922h640.513955l64.508199 255.842922c-0.00307 30.264281-29.67588 63.951521-59.619865 63.951521z" p-id="2964" fill="#d81e06"></path></svg>{item.mill.name}</div>'
                            retStr += f'<div class="salevol">销量：{item.amount}</div>'           
                            retStr += f'</div>'
                            break
        return JsonResponse ({'ret':'0','msg':'成功','data':retStr})
def search2(request):
    if request.method=="POST":
        info = json.loads(request.body.decode())
        inputo = info['input']
        items = Item.objects.filter(name__contains=inputo).values()
        retStr = ''
        for item in items:
            retStr += f'<div class="cue" onclick="changeinput(\'{item["name"]}\')">{item["name"]}</div>'
        return JsonResponse({'ret':'0','msg':'正常','data':retStr})
def listuserinfo(request):

    qs = models.Userinfo.objects.values('name', 'phone','sex', 'user__account' )
    retStr = ''
    for item in  qs:
        for name, value   in item.items():
            retStr += f'{value}'
    return HttpResponse(retStr)

# 身份验证
def login(request):
    """
    添加解析记录
    :param request:
    :return:
    """
    if request.method == 'POST':
        # 获取表单内容
        info = json.loads(request.body.decode())
        # info = request.params['data'] 
        # account = request.POST.get('account')
        # password = request.POST.get('password')
        # 看是否有对应用户
        account = info['account']
        password = info['password']
        # return JsonResponse({'account':account, 'password':password})
        try:
            # 根据 id 从数据库中找到相应的客户记录 
            
            user = User.objects.get(account=info['account'])
        except User.DoesNotExist:
            return JsonResponse({
                'ret': '1',
                'msg': '客户不存在'
            })
        user = User.objects.filter(account=account).values()
        if user[0]['password'] != password :
            return JsonResponse({'ret':'1', 'msg':'密码错误'})
        exp=60 # token有效期 秒
        salt='suigfiugawdilgabDgew372834bhshfvcj' 
        headers = {
            'exp': int(time.time() + exp)  # 过期时间戳
        }
        first = base64.urlsafe_b64encode(json.dumps(headers, separators=(',', ':')).encode('utf-8').replace(b'=', b'')).decode('utf-8').replace('=', '')
        payload = {
            'author': 'trdthg',
            'account': account
        }
        second = base64.urlsafe_b64encode(json.dumps(payload, separators=(',', ':')).encode('utf-8').replace(b'=', b'')).decode('utf-8').replace('=', '')
        # 拼接前两部分
        first_second = f'{first}.{second}'
        # 对前面两部分签名呀
        third = base64.urlsafe_b64encode(hmac.new(salt.encode('utf-8'), first_second.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8').replace('=','')
        # 拼接签名和前两部分，就叫做token啦
        token = '.'.join([first, second, third])
        
        return JsonResponse({'ret': 0, 'msg': '登陆成功', 'token': token} )
def whetherlogin(request):
    if request.method == 'POST':
        try:
            info = json.loads(request.body.decode())
            token = info['token']
        except:
            # return HttpResponse('http://localhost/login.html')
            # return render(request,'http://localhost/login.html')
            return JsonResponse({'ret': '1', 'msg': '1你没token, 😠!'})
        if token == "":
            # return render(request,'http://localhost/login.html', )
            # return HttpResponseRedirect('http://localhost/login.html')
            return JsonResponse({'ret': '1', 'msg': '2你没token, 😠!'})


        salt='suigfiugawdilgabDgew372834bhshfvcj'
        try:
            headers = token.split(".")[0]
            payload = token.split(".")[1]
            sign = token.split(".")[2]
        except:
            return JsonResponse({'ret': '1', 'msg': '3你没token, 😠(ノ｀Д)ノ!'})
        headers_payload = f"{headers}.{payload}"
        new_sign = base64.urlsafe_b64encode(hmac.new(salt.encode('utf-8'), headers_payload.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8').replace('=','')
        if new_sign == sign :
            if isinstance(payload, str):
                payload = payload.encode('ascii') 
                rem = len(payload) % 4 
            if rem > 0:
                payload += b'=' * (4 - rem)
                # 上面这一部分是解密的部分数据补全格式
            payload_data = base64.urlsafe_b64decode(payload) # 解码
            data = json.loads(payload_data) # 加载payload信息为可以通过get方法获取里面的值
            account = data.get("account") # 获取token里面的payload部分中的uid数据信息
            return JsonResponse({'ret': '0', 'account': account, 'msg': '你有token', 'token': token})
        else:
            # return render(request,'http://localhost/login.html')
            # return HttpResponse('http://localhost/login.html')
            return JsonResponse({'ret':'1', 'msg':'token失效'})
    return JsonResponse({'ret':'1', 'msg':'不支持的请求方式'})
def innerwhetherlogin(request):
    # 用于内部其他函数的前置登陆状态判断
    if request.method == 'POST':
        try:
            info = json.loads(request.body.decode())
            token = info['token']
        except:
            # return HttpResponse('http://localhost/login.html')
            # return render(request,'http://localhost/login.html')
            return {'ret': '1', 'msg': '你没token, 😠!'}
        if token == "":
            # return render(request,'http://localhost/login.html', )
            # return HttpResponseRedirect('http://localhost/login.html')
            return {'ret': '1', 'msg': '你没token, 😠!'}


        salt='suigfiugawdilgabDgew372834bhshfvcj'
        headers = token.split(".")[0]
        payload = token.split(".")[1]
        sign = token.split(".")[2]
        headers_payload = f"{headers}.{payload}"
        new_sign = base64.urlsafe_b64encode(hmac.new(salt.encode('utf-8'), headers_payload.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8').replace('=','')
        if new_sign == sign :
            if isinstance(payload, str):
                payload = payload.encode('ascii') 
                rem = len(payload) % 4 
            if rem > 0:
                payload += b'=' * (4 - rem)
                # 上面这一部分是解密的部分数据补全格式
            payload_data = base64.urlsafe_b64decode(payload) # 解码
            data = json.loads(payload_data) # 加载payload信息为可以通过get方法获取里面的值
            account = data.get("account") # 获取token里面的payload部分中的uid数据信息
            return {'ret': '0', 'account': account, 'msg':'正常'}
        else:
            # return render(request,'http://localhost/login.html')
            # return HttpResponse('http://localhost/login.html')
            return {'ret':'1', 'msg':'token失效'}
    return {'ret':'1', 'msg':'不支持的请求方式'}
def innerwhetherlogin2(request):
      # 做个上传头像让我当场炸裂了
    # token传递 与data传递都有大问题
    try:
        token = request.POST.get("token")
        token = str(token)
    except:
        return {'ret': '0', 'msg':'sss'}
    salt='suigfiugawdilgabDgew372834bhshfvcj'
    headers = token.split(".")[0]
    payload = token.split(".")[1]
    sign = token.split(".")[2]
    headers_payload = f"{headers}.{payload}"
    new_sign = base64.urlsafe_b64encode(hmac.new(salt.encode('utf-8'), headers_payload.encode('utf-8'), hashlib.sha256).digest()).decode('utf-8').replace('=','')
    if new_sign == sign :
        if isinstance(payload, str):
            payload = payload.encode('ascii') 
            rem = len(payload) % 4 
        if rem > 0:
            payload += b'=' * (4 - rem)
            # 上面这一部分是解密的部分数据补全格式
        payload_data = base64.urlsafe_b64decode(payload) # 解码
        data = json.loads(payload_data) # 加载payload信息为可以通过get方法获取里面的值
        account = data.get("account") # 获取token里面的payload部分中的uid数据信息
        return {'ret': '0', 'account': account,'msg':'成功'}
    else:
        # return render(request,'http://localhost/login.html')
        # return HttpResponse('http://localhost/login.html')
        return {'ret':'1', 'msg':'token失效'}
def attention(request):
    response = innerwhetherlogin(request)

    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':request['msg']})
    # else:
        # return JsonResponse({'ret':'1', 'msg':response['msg']})
    if request.method == 'POST':
        account = response['account']
        # user = User.objects.filter(account=account).values()
        user = User.objects.get(account=account) 
        carts = Cart.objects.filter(user=user).values()
        retStr = ''
        
        for cart in carts:
            style = Style.objects.get(id=cart['style_id'])
            cart3 = Cart.objects.get(id=cart['id'])
            cart3.price = style.price
            cart3.save()
            if int(cart3.price) < int(cart["oldprice"]):
                item = style.item
                retStr += item.name + "("+style.style+")"
                retStr += " "
            cart2 = Cart.objects.get(id=cart['id'])
            cart2.oldprice = cart2.price
            cart2.save()
        return JsonResponse({'ret':'0','data':retStr})

def displaygoods(request):

    if request.method == 'POST':
        try:
            info = json.loads(request.body.decode())
            goodsname = info['goodsname']
        except: 
            return HttpResponse('━━(￣ー￣*|||━━')
        retStr = ''
        qs = models.Item.objects.values('id', 'name', 'image', 'price', 'mill__id')
        i = 0
        # item = Item.objects.get(name=goodsname)
        for item in  qs:
            for name,value in item.items():
                if name=='name' and value==goodsname :
                    i=1
                    # 现在对应的item为该商品的列
                    # 现在要找到外键id指向该商品的所有style
                    # <a href="" >
                    #     <img  width="40" height="40" ><i>A型</i>
                    # </a>
                    qs = models.Style.objects.values('style', 'item__id')
                    for style in qs:
                        for name, value in style.items():
                            if style['item__id'] == item['id']:
                                if name == 'style':
                                    retStr += f'<a href="" ><img width="40" height="40" ><i>{value}</i></a>'
                    return JsonResponse({'name':item['name'], 'price': item['price'], 'id': item['mill__id'], 'allstyle': retStr})
        if i==0:
            return JsonResponse({'msg':'没有该商品'})
def showthisstyle(request):
    # 传入style对应的item的id,以及该style的name
    if request.method == 'POST':
        try:
            info = json.loads(request.body.decode())
            goodsname = info['goodsname']
            itemid = info['itemid']
        except: 
            return HttpResponse('━━(￣ー￣*|||━━')
        
        retStr = ''
        qs = models.Style.objects.values('id', 'style', 'image', 'price', 'item__id')
        for style in qs:
            if str(style['item__id'])==itemid+'' and style['style']==goodsname :
                return JsonResponse({'ret':'0','itemid':style['item__id'], 'stylename':style['style'], 'imagepath':style['image'], 'price':style['price']})
        return HttpResponse("没有该商品")
    else:
        return HttpResponse("gun")

# 个人信息页
def showmyinfo(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':'您未登录'})
    else:
        if request.method == 'POST':
            try:
                info = json.loads(request.body.decode())
            except: 
                return JsonResponse({'ret':'1', 'msg':'您未登录'})
            account = response['account']
            user = User.objects.filter(account=account).values()
            userid = user[0]['id']
            
            if account != '' :
                retStr = ''
                qs = models.User.objects.values()
                for user in qs:
                    if user['account']==account:
                        # userinfo = Userinfo.objects.get(user=user['user__id'])
                # user = User.objects.filter(account=account).values()
                        userinfo = Userinfo.objects.filter(user=user['id']).values()
                        return JsonResponse({'ret':'0', 'account':account, 'password':user['password'], 'name':userinfo[0]['name'], 'phone':userinfo[0]['phone'], 'sex':userinfo[0]['sex'], 'image':userinfo[0]['image'] })
                # user = User.objects.get(account=account)
                # userid = user.user
                # userinfo = Userinfo.objects.get(user=str('user_id'))

                # for userinfo in qs:
                #     if userinfo['user__id']==
                return JsonResponse({'ret':'1', 'msg':'没有此人'})
            else:
                return JsonResponse({'ret':'1', 'msg':'您未登录'})
def uploaduserimage(request):

    response = innerwhetherlogin2(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':response['msg']})
    else:
        # if request.method == 'POST':
            account = response['account']
            user = User.objects.filter(account=account).values()
            userid = user[0]['id']
            user = User.objects.get(account=account)

            try:
                image = request.FILES.get('file')
                # image = info['image']# file_content = image.read()# file_content = image.decode("utf-8")
            except:
                return JsonResponse({'ret':'1','msg':'您未上传你的头像'})
            userinfo = Userinfo.objects.get(user=user)
            # userinfo = Userinfo.objects.get(phone='777')
            # path = default_storage.save('news/'+image.name,ContentFile(image.read()))# 保存文件
            # image_url = os.path.join('double/userimage/%s.log' % int(time.strftime("%Y%m%d%H%M%S"))).replace('\\', '/')
            # with open(image_url, 'wb') as f:
            #         f.write(image)  # 打开路径将结果写入到文件中
            userinfo.image = image
            userinfo.path = image.name
            user = User.objects.get(account=account)
            
            # userinfo.image = "SSSSSSSSSSSSSSSSSSSSSS"
            userinfo.save()
            return JsonResponse({'ret':'0', 'msg':'上传成功了', 'data':image.name})
        # else:
        #     return JsonResponse({'ret':'1', 'msg':'不支持的类型'})       
def uploaduserimage2(request):
    # 失败品
    # 失败者
    # 废物
    # 垃圾
    # 一坨***
    if request.method == 'POST':
            try:
                info = json.loads(request.body.decode())
            except: 
                return JsonResponse({'ret':'1', 'msg':'您未登录'})
            # user = User.objects.filter(account='111').values()
            user = User.objects.get(account='111')
            img = info['img']
            for image in img:
                # image_data = base64.b64decode(image)
                image_data =image
                image_url = os.path.join('double/userimage/%s.log' % int(time.strftime("%Y%m%d%H%M%S"))).replace('\\', '/')
                with open(image_url, 'wb') as f:
                    f.write(image_data)  # 打开路径将结果写入到文件中
                # 然后将图片路径保存到数据库
                # Userinfo.objects.create(image=image_url,user=user)
                userinfo = Userinfo.objects.get(phone='777')
                userinfo.image = image_url
                userinfo.save()
            return JsonResponse({'ret':'0', 'msg':'成功上传'})
def changeinfo(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':'您未登录'})
    else:
        if request.method == 'POST':
            try:
                info = json.loads(request.body.decode())
            except: 
                return JsonResponse({'ret':'1', 'msg':'您未登录'})
            account = response['account']
            user = User.objects.filter(account=account).values()
            userid = user[0]['id']
            
            newname = info['newname']
            newphone = info['newphone']
            newpassword1 = info['newpassword1']
            newpassword2 = info['newpassword2']
            
            retStr = ''
            qs = models.User.objects.values()
            for user in qs:
                if user['account']==account:
                    userid = user['id']
                    # userinfo = Userinfo.objects.filter(user=user['id']).values()
                    if newname != '' and newphone != '' and newpassword1 != '' and newpassword2 != '' :
                        return JsonResponse({'ret':'2', 'msg':'您未填写信息'})
                    if newpassword1!=newpassword2:
                        return JsonResponse({'ret':'2', 'msg':'前后密码不一致'})

                    userinfo = Userinfo.objects.get(user=userid)
                    if newname != '':
                        userinfo.name = newname
                    if newphone != '':
                        userinfo.phone = newphone
                    user = User.objects.get(account=account)
                    if newpassword1 != '' and newpassword2 != '' and newpassword1==newpassword2:
                        user.password = newpassword2
                    userinfo.save()
                    user.save()
                    return JsonResponse({'ret':'0', 'msg':'修改完成'})
def register(request):
    if request.method == 'POST':
        try:
            info = json.loads(request.body.decode())
            name = info['name']
            password = info['password']
            confirm = info['confirm']
        except:
            return JsonResponse({'ret':'1', 'msg':'发生错误'})
        if password != confirm :
            return JsonResponse({'ret':'1', "msg":'输入密码不一致'})
        # 随机生成11位数作为账号
        while True:
            account = random.randint(10000000000,99999999999)
            # account = str(account)
            try:
                user = User.objects.get(account=account)
            except:
                record = User.objects.create(account=str(account) ,password=str(password))
                A = User.objects.get(account = account)
                Userinfo.objects.create(name = str(name), user=A)
                return JsonResponse({'ret':'0', 'msg':f'注册成功, 请勿关闭此页面.请牢记您的用户名:{account}'})
            return JsonResponse({'ret':'2', 'msg':'没有此人oooomygod'})
        return JsonResponse({'ret':'1', 'msg':'不支持的类型'})

# 购物车
def addtomyshoppingcar(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':'您未登录'})
    else:
        if request.method == 'POST':
            try:
                info = json.loads(request.body.decode())
            except: 
                return JsonResponse({'ret':'2', 'msg':'您未登录'})
            # 根据传来的 账号 商家名 类型名 进行添加购物车内容
            account = response['account']
            user = User.objects.get(account=account)
            userid = user.id
            styleid = info['styleid']
            amount = info['amount']

            A = User.objects.get(account = account)
            B = Style.objects.get(id=styleid)
            try:
                C = Cart.objects.get(style=B,user=A)
                return JsonResponse({'ret':'2', 'msg':'禁止重复添加'})
            except:
            # style = Style.objects.filter(style=stylename).values()
                record = Cart.objects.create(name=B.style,
                                            image=B.image,
                                            price=B.price,
                                            oldprice=B.price,
                                            amount=amount,
                                            ret="0",
                                            user=A,
                                            style=B)
                return JsonResponse({'ret':'0', 'msg':'成功添加至购物车'})
        else:
            return JsonResponse({'ret':'2', 'msg':'不支持的类型'})
def showmyshoppingcar(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':'您未登录'})
    else:
        account = response['account']
        user = User.objects.filter(account=account).values()
        userid = user[0]['id']
        qs = Cart.objects.values('id', 'name', 'image', 'price', 'amount', 'user__id', 'style__id')
        # retStr = {}
        retStr = f''
        i=0
        bigsum=0
        for cart in qs:
            if cart['user__id']==userid:      
                # retStr['data'+str(i)] = cart
                sum = int(cart['price'])*int(cart['amount'])
                bigsum += sum
                retStr += f'<tr class="goods" id={cart["id"]}><td class="select"><form><input type="checkbox" name="vehicle" value="Bike"><br></form></td><td class="what"><a href="" ><img src={cart["image"].split("/")[1] + "/" + cart["image"].split("/")[2] } width="70" height="70" ><i>A型</i></a>{cart["name"]}</td><td class="price">￥{cart["price"]}</td><td class="number"><input  value={cart["amount"]} type="number" min="1" oninput="this.value=this.value.replace(/\D/g);"></td><td class="sum">￥{sum}</td><td class="operate">删除</td></tr>'
                i+=1
        if i==0:
            return JsonResponse({'ret':'1', 'msg':'没有东西'})
        # retStr = list[retStr]
        return JsonResponse({'ret': '0', 'data':retStr, 'i':i-1, 'bigsum':bigsum})
def deletefrommyshoppingcar(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':'您未登录'})
    # else:
    #     return JsonResponse({'ret':'1', 'msg':response['msg']})
    account = response['account']
    user = User.objects.filter(account=account).values()
    userid = user[0]['id']
    if request.method == 'POST':
        try:
            info = json.loads(request.body.decode())
            styleid = info['styleid']
        except: 
            return HttpResponse('━━(￣ー￣*|||━━')
        retStr = ''
        cart = Cart.objects.get(id=styleid)
        cart.delete()
        return JsonResponse({'ret':'0', 'msg':'成功删除'})
    else:
        return JsonResponse({'ret':'1', 'msg':'不支持此类型'})
def modifyamount(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':response['msg']})
    else:
        if request.method == 'POST':
            try:
                info = json.loads(request.body.decode())
            except: 
                return JsonResponse({'ret':'1', 'msg':response['msg']})
            account = response['account']

            cartid = info['cartid']
            newamount = info['newamount']
            user = User.objects.get(account=account)
            cart = Cart.objects.get(id=cartid)
            if cart.user == user:
                cart.amount = str(newamount)
                cart.save()
            return JsonResponse({'ret':'0', 'msg':'修改成功'})
        else:
            return JsonResponse({'ret':'1', 'msg':'不支持此类型'})
def buy(request):
    response = innerwhetherlogin2(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':response['msg']})
    else:
        if request.method == 'POST':
            # account = response['account']
            # user = User.objects.filter(account=account).values()
            # user = User.objects.get(account=account)

            cartids = request.POST.getlist("cartid")
            amounts = request.POST.getlist("amount")
            
            i=0
            for cartid in cartids:
                cart = Cart.objects.get(id=cartid)
                style = cart.style
                style.amount = str( int(style.amount) + int(amounts[i]) )
                style.save()
                
                # 商品总销量
                item = style.item
                item.amount = str(int(item.amount) + int(amounts[i]))
                item.save()
                
                # 商家总收益
                user = item.mill.user
                money = int(style.price) * int(style.amount)
                user.money = str(int(user.money) + money)
                user.save()

                # 从买家购物车清除
                cart.delete()
                i += 1
            return ({'ret':'0','msg':'购买成功'})
        else:
            return JsonResponse({'ret':'1', 'msg':'不支持此类型'})


# 商家管理页面
def sowmymoney(request):
    response = innerwhetherlogin(request)
    account = response['account']
    user = User.objects.get(account=account)
    return JsonResponse({'ret':'0','money':user.money})
def showmymill(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':'您未登录'})
    # else:
        # return JsonResponse({'ret':'1', 'msg':response['msg']})
    if request.method == 'POST':
        try:
            info = json.loads(request.body.decode())
        except:
            return HttpResponse('━━(￣ー￣*|||━━')
        account = response['account']
        # user = User.objects.filter(account=account).values()
        user = User.objects.get(account=account)
        mills = Mill.objects.filter(user=user).values()
        

        retStr = ''
        for mill in mills:
            retStr += f'<div class="mills" id="{mill["id"]}"><a href="./mymill-middle.html?id={mill["id"]}" target="middle"><div class="name" id="">{mill["name"]}</div></a><div class="delete" id="">x</div></div>'
        return JsonResponse({'ret':'0', 'data':retStr})
    else:
        return JsonResponse({'ret':'1', 'msg':'不支持此类型'})
def showmyitem(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':'您未登录000000000'})
    # else:     
    #     return JsonResponse({'ret':'1', 'msg':response['msg']})
    if request.method == 'POST':
        try:
            info = json.loads(request.body.decode())
            millid = info['millid']
            mill = Mill.objects.get(id=millid)
        except: 
            return HttpResponse('━━(￣ー￣*|||━━')
        account = response['account']
        user = User.objects.get(account=account)
        userid = user.id


        # if mill.user == user:
        retStr = ''
        items = Item.objects.filter(mill=mill).values()
        for item in items:
            retStr += f'<div class="items" id={item["id"]}><a href="./mymill-right.html?id={item["id"]}" target="right"><div class="name">{item["name"]}</div></a><div style="text-align: center; display: inline-block;">销量：{item["amount"]}</div><div class="delete" id="">x</div></div>'
        return JsonResponse({'ret':'0','data':retStr})
        # else :
            # return JsonResponse({'ret':'0', 'msg':'gun'})
    else:
        return JsonResponse({'ret':'1', 'msg':'不支持此类型'})
def showmystyle(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':'您未登录'})
    # else:
        # return JsonResponse({'ret':'1', 'msg':response['msg']})
    if request.method == 'POST':
        try:
            info = json.loads(request.body.decode())
            itemid = info['itemid']
            item = Item.objects.get(id=itemid)
            account = response['account']
        except:
            return HttpResponse('━━(￣ー￣*|||━━')
        # user = User.objects.filter(account=account).values()
        user = User.objects.get(account=account)
        # mill = Mill.objects.get(id=item.mill)
        if item.mill.user==user:

            retStr = ''
            styles = Style.objects.filter(item=item).values()
            for style in styles:    
                try:
                    imagepath = style['image'].split("/")[1] + "/" + style['image'].split("/")[2] 
                except: 
                    imagepath = ""
                #  headers = token.split(".")[0]
                retStr += f'<div class="goods" id={style["id"]}><div onclick="displaynone({style["id"]})"><svg t="1606475197985" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2948" width="200" height="200"><path d="M803.84 863.744c-8.704 0-16.896-3.584-23.552-10.24L512 585.728l-267.264 267.264c-6.656 6.656-14.336 10.24-23.04 10.24-12.288 0-25.088-7.168-39.424-21.504-14.848-14.848-21.504-27.648-21.504-39.936 0-8.704 3.584-16.384 10.752-23.04L438.272 512 170.496 244.224c-25.6-26.112 0-52.736 9.728-62.464 11.776-11.776 25.088-23.04 39.424-23.04 8.192 0 16.384 3.584 24.576 11.264L512 438.272l267.776-267.264c7.168-7.168 15.36-10.752 23.552-10.752 12.288 0 24.064 7.168 40.96 23.552 11.264 11.264 35.328 35.328 9.216 60.928L585.728 512l267.264 267.264c23.04 23.04 9.216 44.032-9.216 62.976-13.824 14.336-27.648 21.504-39.936 21.504z" fill="#bfbfbf" p-id="2949"></path></svg></div><input type="text" value={style["style"]}><input type="number" value={style["price"]} oninput="this.value=this.value.replace(/[+-]/g);"><div class="layui-form-item"><label class="layui-form-label">添加图片</label><div class="layui-input-block"><input type="hidden" id="img_url"><input type="file" onchange="showImg(this.id)" id="img_{style["id"]}"><img src="{imagepath}" alt="" id="img_{style["id"]}" style="width: 190px;height: 190px;"></div></div></div>'
            return JsonResponse({'ret':'0','data':retStr, 'msg':'正常'})
        else :
            return JsonResponse({'ret':'0', 'msg':'gun'})    
    else:
        return JsonResponse({'ret':'1', 'msg':'不支持此类型'})

def createnewmill(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':response['msg']})
    else:
        if request.method == 'POST':
            try:
                info = json.loads(request.body.decode())
            except: 
                return JsonResponse({'ret':'1', 'msg':response['msg']})
            account = response['account']
            user = User.objects.filter(account=account).values()
            userid = user[0]['id']
            newmillname = info['newmillname']

            A = User.objects.get(account = account)
            record = Mill.objects.create(name=newmillname,
                                        image='',
                                        desc='',
                                        user=A,
                                        )
            return JsonResponse({'ret':'0', 'msg':'成功创建店铺'})
        else:
            return JsonResponse({'ret':'2', 'msg':'不支持的类型'})
def createnewitem2(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':response['msg']})
    else:
        if request.method == 'POST':
            try:
                info = json.loads(request.body.decode())
            except: 
                return JsonResponse({'ret':'1', 'msg':'您未登录'})
            account = response['account']
            newitemname = info['newitemname']
            millid = info['millid']
            if newitemname=='':
                return JsonResponse({'ret':'1','msg':'不能为空'})
            A = User.objects.get(account=account)
            B = Mill.objects.get(id=millid)
            record = Item.objects.create(name=newitemname,
                                        desc='',
                                        mill=B,
                                        )
            return JsonResponse({'ret':'0', 'msg':'成功'})
        else:
            return JsonResponse({'ret':'2', 'msg':'不支持的类型'})
def updatenewstyles(request):

    response = innerwhetherlogin2(request)

    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':'您未登录'})
    # else:
        # return JsonResponse({'ret':'1', 'msg':response['msg']})
    if request.method == 'POST':
        account = response['account']
        # user = User.objects.filter(account=account).values()
        user = User.objects.get(account=account)

        millid = request.POST.get("millid")
        introname = request.POST.get("introname")
        introtext = request.POST.get("introtext")

        names = request.POST.getlist("name")
        prices = request.POST.getlist("price")

        images = request.FILES.getlist('image')

        # return JsonResponse({'ret':'0','data':image})
        # 创建item
        if introname=='' :
            return JsonResponse({'ret':'1','msg':'不能为空'})
        A = User.objects.get(account=account)
        B = Mill.objects.get(id=millid)
        record = Item.objects.create(name=introname,
                                    desc=introtext,
                                    amount="0",
                                    mill=B,
                                    )
        itemid = record.id
        item = Item.objects.get(id=itemid)
        # 添加关键词
        keywords = jieba.analyse.textrank(introname,topK=20, withWeight=True, allowPOS=('n','nr','ns'))
        for keyword in keywords:
            for word in keyword:
                print(keywords)
                if type(word) == type("str"):
                    Keyword.objects.create(word=word,
                                            itemname=introname,
                                            item = item)
        # 创建类型                            
        i=0
        for name in names:
            record = Style.objects.create(style=name,
                                        price=prices[i],
                                        amount="0",
                                        image=images[i],
                                        item=item,
                                        )
            i+=1
        
        return JsonResponse({'ret':'0', 'msg':'成功', 'id':itemid})
    else:
        return JsonResponse({'ret':'2', 'msg':'不支持的类型'})
def addnewstyle(request):
    response = innerwhetherlogin2(request)

    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':'您未登录'})
    # else:
        # return JsonResponse({'ret':'1', 'msg':response['msg']})
    if request.method == 'POST':
        account = response['account']
        # user = User.objects.filter(account=account).values()
        user = User.objects.get(account=account)

        itemid = request.POST.get('itemid')
        item = Item.objects.get(id=itemid)
        record = Style.objects.create(style='',
                                        price="0",
                                        amount="0",
                                        image='',
                                        item=item,
                                        )
        return ({'ret':'0','msg':'添加成功,请填写详细信息'})
    else:
        return JsonResponse({'ret':'2', 'msg':'不支持的类型'})

def deletethismill(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':response['msg']})
    else:
        if request.method == 'POST':
            try:
                info = json.loads(request.body.decode())
            except: 
                return JsonResponse({'ret':'1', 'msg':response['msg']})
            account = response['account']
            user = User.objects.get(account=account)
            millid = info['millid']
            mill = Mill.objects.get(id=millid)
            if mill.user == user:
                mill.delete()
                return JsonResponse({'ret':'0', 'msg':'成功删除'})
            else :
                return JsonResponse({'ret':'0', 'msg':'gun'})
                
        else:
            return JsonResponse({'ret':'1', 'msg':'不支持此类型'})
def deletethisitem(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':response['msg']})
    else:
        if request.method == 'POST':
            try:
                info = json.loads(request.body.decode())
            except: 
                return JsonResponse({'ret':'1', 'msg':response['msg']})
            account = response['account']
            user = User.objects.get(account=account)
            itemid = info['itemid']
            item = Item.objects.get(id=itemid)
            millid = info['millid']
            mill = Mill.objects.get(id=millid)
            if mill.user == user and item.mill==mill:
                item.delete()
                return JsonResponse({'ret':'0', 'msg':'成功删除'})
            else :
                return JsonResponse({'ret':'0', 'msg':'gun'})
                
        else:
            return JsonResponse({'ret':'1', 'msg':'不支持此类型'})
def deletwthisstyle(request):
    response = innerwhetherlogin2(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':response['msg']})
    else:
        if request.method == 'POST':
            # try:
            #     info = json.loads(request.body.decode())
            # except: 
            #     return JsonResponse({'ret':'1', 'msg':response['msg']})
            account = response['account']
            user = User.objects.get(account=account)

            styleid = request.POST.get("styleid")
            style = Style.objects.get(id=styleid)
            style.delete()
            return JsonResponse({'ret':'0', 'msg':'成功删除'})    
        else:
            return JsonResponse({'ret':'1', 'msg':'不支持此类型'})

def modifystylename(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':response['msg']})
    else:
        if request.method == 'POST':
            try:
                info = json.loads(request.body.decode())
            except: 
                return JsonResponse({'ret':'1', 'msg':response['msg']})
            account = response['account']
            user = User.objects.get(account=account)

            newname = info['newname']
            styleid = info['styleid']
            style = Style.objects.get(id=styleid)
            style.style = newname
            style.save()
            return JsonResponse({'ret':'0', 'msg':'成功更改'})    
        else:
            return JsonResponse({'ret':'1', 'msg':'不支持此类型'})
def modifystyleprice(request):
    response = innerwhetherlogin(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':response['msg']})
    else:
        if request.method == 'POST':
            try:
                info = json.loads(request.body.decode())
            except: 
                return JsonResponse({'ret':'1', 'msg':response['msg']})
            account = response['account']
            user = User.objects.get(account=account)

            newprice = info['newprice']
            styleid = info['styleid']
            style = Style.objects.get(id=styleid)
            style.price = str(newprice)
            style.save()
            return JsonResponse({'ret':'0', 'msg':'成功更改'})    
        else:
            return JsonResponse({'ret':'1', 'msg':'不支持此类型'})
def modifystyleimage(request):
    response = innerwhetherlogin2(request)
    if response['ret'] != '0':
        return JsonResponse({'ret':'1', 'msg':response['msg']})
    else:
        if request.method == 'POST':
           
            account = response['account']
            user = User.objects.get(account=account)

            prices = request.POST.get("price")
            styleid = request.POST['styleid']
            image = request.FILES.get('image')
            style = Style.objects.get(id=styleid)
            style.image = image
            style.save()
            return JsonResponse({'ret':'0', 'msg':'成功更改'})    
        else:
            return JsonResponse({'ret':'1', 'msg':'不支持此类型'})
            
# 主页跳转到商品页面
def jumptoitem(request):
    if request.method == 'POST':
        try:
            info = json.loads(request.body.decode())
            itemid = info["itemid"]
        except: 
            return HttpResponse('━━(￣ー￣*|||━━')
        retStr = ''
        # qs = models.Item.objects.values('id', 'name', 'image', 'price', 'mill__id')
        i = 0
        try:
            item = Item.objects.get(id=itemid)
        except:
            return JsonResponse({'ret':"1", 'msg':'没有此商品'})
        try: 
            styles = Style.objects.filter(item=itemid).values()
            # style2=style
        except:
            return JsonResponse({'ret':'1', 'msg':'没有相关类型'})
        for line in styles:
            retStr += f'<a id = {line["id"]}><img width="40" height="40" src={line["image"].split("/")[1] + "/" + line["image"].split("/")[2] } ><i>{line["style"]}</i></a>'
        # item = Item.objects.filter(id=itemid).values()
        retStr2 = {}
        # style = Style.objects.filter(item=itemid).values()
        for style in styles:

            retStr2['image'] = style['image'].split("/")[1] + "/" + style['image'].split("/")[2] 
        # retStr2['name'] = style[0]["style"]
            retStr2['name'] = item.name
            retStr2['introtext'] = item.desc
            retStr2['price'] = style["price"]
            retStr2['id'] = style["id"]
            break
        
        return JsonResponse({'ret':'0', 'msg':'正常', 'data':retStr, 'data2':retStr2 })
def jumptostyle(request):
    if request.method == 'POST':
        try:
            info = json.loads(request.body.decode())
            styleid = info["styleid"]
        except: 
            return HttpResponse('━━(￣ー￣*|||━━')
        retStr = ''
        try:
            style = Style.objects.get(id=styleid)
        except:
            return JsonResponse({'ret':"1", 'msg':'没有此商品'})
        try: 
            itemid = style.item.id
            item = Item.objects.get(id=itemid)
            style = Style.objects.filter(id=styleid).values()
        except:
            return JsonResponse({'ret':'1', 'msg':'没有相关类型吗'})
        retStr2 = {}
        # retStr2['name'] = style[0]['style']
        retStr2['name'] = item.name
        retStr2['image'] = style[0]['image'].split("/")[1] + "/" + style[0]['image'].split("/")[2] 
        retStr2['price'] = style[0]['price']
        retStr2['id'] = style[0]['id']
        style = Style.objects.filter(item=itemid).values()
        for line in style:
            retStr += f'<a  id = {line["id"]}><img width="40" height="40" src={line["image"].split("/")[1] + "/" + line["image"].split("/")[2]} ><i>{line["style"]}</i></a>'
        # return JsonResponse({'ret':'1', 'msg':'测试', 'data2':retStr2})
        return JsonResponse({'ret':'0', 'msg':'正常', 'data':retStr, 'data2':retStr2 })





        


