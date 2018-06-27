from django.conf.urls import url
from polls import views

urlpatterns = [
    url(r'^groups/$', views.groups),
    url(r'^groups/(?P<pk>[0-9]+)/$', views.group_detail),
    url(r'^users/$', views.users),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
]