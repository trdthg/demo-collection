from django.db import models

# Create your models here.

# 用户表
class User(models.Model):

    # 账号
    account = models.CharField(max_length=30)
    # 密码
    password = models.CharField(max_length=30)
    # 总销量
    money = models.CharField(max_length=255,null=True, blank=True) 

# 用户详细信息表
class Userinfo(models.Model):

    # 昵称
    name = models.CharField(max_length=255,null=True, blank=True)
    # 联系方式
    phone = models.CharField(max_length=255,null=True, blank=True)
    # 性别
    sex = models.CharField(max_length=10,null=True, blank=True)
    # 用户头像
    # image = models.CharField(max_length=255,null=True, blank=True)
    image = models.ImageField(upload_to="double/userimage", blank=True)
    path = models.CharField(max_length=255,null=True, blank=True)
    # 账户外键  与User一对一
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    @property  
    def face_image_url(self):  # 这一段很关键要加上
        if self.face_image and hasattr(self.face_image, 'url'):
            return self.face_image.url
    

# 店铺表
class Mill(models.Model):

    # 店铺名称
    name = models.CharField(max_length=255,null=True, blank=True)
    # 宣传图片
    image = models.CharField(max_length=255,null=True, blank=True)
    # 店铺介绍
    desc = models.CharField(max_length=255,null=True, blank=True)

    # 店铺外键 与User多对一
    user = models.ForeignKey(User, on_delete=models.PROTECT)


# # 商品销量表  鸽了
# class Salesvolumn(models.Model):

#     # item = models.ForeignKey(Item, on_delete=models.PROTECT)
#     # style = models.ForeignKey(Style, on_delete=models.PROTECT)

#     # # 总销量
#     salesvolumn = models.PositiveIntegerField()
#     style = models.ForeignKey(Style, on_delete=models.PROTECT)

 # 商品表
class Item(models.Model):

    # 商品图片  与第一种规格相同
    image = models.CharField(max_length=255,null=True, blank=True)
    # 商品名称
    name = models.CharField(max_length=255,null=True, blank=True)
    # 商品价格  与第一种规格相同
    price = models.CharField(max_length=255,null=True, blank=True)
    # 商品描述
    desc = models.CharField(max_length=99999999, null=True, blank=True)

    amount = models.CharField(max_length=255,null=True,blank=True)


    # 外键 与店铺多对一
    mill = models.ForeignKey(Mill, on_delete=models.PROTECT)
    # 店铺外键 与User多对一
    # 外键 与商品多对多
    # salesvolumn = models.ManyToManyField(Style, through='Salesvolumn')
    # salesvolumn = models.ForeignKey(Salesvolumn, on_delete=models.PROTECT)
    # 商品样式表
class Style(models.Model):

    # 规格名称
    style = models.CharField(max_length=255,null=True, blank=True)
    # 规格图片
    image = models.ImageField(upload_to="double/itemimage", blank=True,null=True)

    # 规格价格
    price = models.CharField(max_length=255,null=True, blank=True)
    
    # 商品的唯一ID
    unipueid = models.CharField(max_length=255,null=True,blank=True)
    # 销量
    amount = models.CharField(max_length=255,null=True,blank=True)

    # 外键
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.SET_NULL)
    # 店铺外键 与User多对一




# 购物车
class Cart(models.Model):
    # 直接把样式内容搬过来

    # 规格名称
    name = models.CharField(max_length=255,null=True, blank=True)
    # 规格图片
    image = models.CharField(max_length=255,null=True, blank=True)
    # 规格价格
    price = models.CharField(max_length=255,null=True, blank=True)
    oldprice = models.CharField(max_length=255,null=True, blank=True)
    
    # 购买数量
    amount = models.CharField(max_length=255,null=True, blank=True)
    # 是否选中
    ret = models.CharField(max_length=3 ,null=True, blank=True)
    

    # 小计:放到js里主动计算 
    # 操作:urls路由处理

    # 外键 与User一对一，与规格也是一对一
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    style = models.ForeignKey(Style, on_delete=models.PROTECT)


# class Itemname(models.Model):
class Keyword(models.Model):
    word = models.CharField(max_length=20,null=True, blank=True)
    itemname = models.CharField(max_length=20,null=True, blank=True)
    item = models.ForeignKey(Item, null=True, blank=True, on_delete=models.SET_NULL)


    


