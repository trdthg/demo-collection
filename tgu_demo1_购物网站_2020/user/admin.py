from django.contrib import admin

# Register your models here.
from .models import User
from .models import Userinfo
from .models import Style
from .models import Cart
from .models import Item
from .models import Mill
from .models import Keyword

admin.site.register(User)
admin.site.register(Userinfo)
admin.site.register(Style)
admin.site.register(Cart)
admin.site.register(Item)
admin.site.register(Mill)
admin.site.register(Keyword)