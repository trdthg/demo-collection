from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.conf.urls import url
from user.views import listallitems
from django.shortcuts import render
# from asys.settings import MEDIA_ROOT
def newweb(request):
    return HttpResponseRedirect('http://localhost/index.html')
def test():
    return HttpResponse("ssssss")
def test2(request):
    return render(request,'index.html')
urlpatterns = [
    path('admin/', admin.site.urls),

    path('test/', newweb),

    path('user/', include('user.urls')),
    
    path('goods/', include('user.urls')),

    # path('goods.html/<int:itemid>', include('user.urls')),

    # url(r'^goods.html/(\d+)/$', test() )

] +  static("/", document_root="./double")

# re_path(r'^media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),