from django.conf.urls import url,include
from django.contrib import admin
from . import views
#admin.autodiscover()

urlpatterns = [
    url(r'^Index/$',views.Index),
    url(r'^Login/$',views.Login),
    url(r'^Signup/$',views.Signup),
    url(r'^UserInfo/$',views.UserInfo),
    url(r'^AdminDataInfo/$',views.AdminDataInfo),
    url(r'^BuyableData/$',views.BuyableData),
    url(r'^Upload/$',views.Upload),
    url(r'^UploadData/$',views.UploadData),
    url(r'^Order/$',views.Order),
    url(r'^Recharge/$',views.Recharge),
]
