from django.conf.urls import url,include
from django.contrib import admin
from . import views
#admin.autodiscover()

urlpatterns = [
    url(r'^index/$',views.getIndex),
    url(r'^login/$',views.login),
    url(r'^signUp/$',views.signUp),
    url(r'^userInfo/$',views.userInfo),
    url(r'^adminInfo/$',views.adminInfo),
    url(r'^uploadData/$',views.uploadData),
]
