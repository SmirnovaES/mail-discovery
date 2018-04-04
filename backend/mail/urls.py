from django.conf.urls import url
from mail import views

urlpatterns = [
               url(r'^letters/$', views.letter_list),
               url(r'^letters/(?P<date_from>\S+),(?P<date_before>\S+)/$', views.letter_detail),
               ]

