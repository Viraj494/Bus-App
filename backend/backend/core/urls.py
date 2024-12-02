from django.urls import path

from . import views


app_name = 'core'


urlpatterns = [
    path('', views.admin_home, name="admin_home"),
    path('index', views.index, name='index'),
]