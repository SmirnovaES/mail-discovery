from django.conf.urls import url
from mail import views

urlpatterns = [url(r'^letters/$', views.letters_process)]