from django.conf.urls import url,include
from django.contrib import admin
from . import views
#admin.autodiscover()

urlpatterns = [
    url(r'^$',views.Index),
    url(r'^Index/$',views.Index),
    url(r'^index/$',views.Index),

    url(r'^Login/$',views.Login),
    url(r'^login/$',views.Login),

    url(r'^Signup/$',views.Signup),
    url(r'^signup/$',views.Signup),

    url(r'^UserInfo/$',views.UserInfo),
    url(r'^userInfo/$',views.UserInfo),

    url(r'^AdminDataInfo/$',views.AdminDataInfo),
    url(r'^adminDataInfo/$',views.AdminDataInfo),

    url(r'^BuyableData/$',views.BuyableData),
    url(r'^buyableData/$',views.BuyableData),

    url(r'^Upload/$',views.Upload),
    url(r'^upload/$',views.Upload),

    url(r'^MyData/$',views.MyData),
    url(r'^myData/$',views.MyData),

    url(r'^Order/$',views.Order),
    url(r'^order/$',views.Order),

    url(r'^Recharge/$',views.Recharge),
    url(r'^recharge/$',views.Recharge),

    url(r'^Notify/$',views.Notify),
    url(r'^notify/$',views.Notify),

    url(r'^ChainInfo/$',views.ChainInfo),
    url(r'^chainInfo/$',views.ChainInfo),

    url(r'^AdminChainInfo/$',views.AdminChainInfo),
    url(r'^adminChainInfo/$',views.AdminChainInfo),
]
