from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.wall),
    path('logout', views.logout),
    path('make_post', views.make_post),
    path('delete_post/<post>', views.delete_post),
    path('make_comment/<post>', views.make_comment)

]
