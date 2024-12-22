from django.urls import path
# import views from core
from . import views


app_name = 'core'

# add core file paths
urlpatterns = [
    path('', views.admin_home, name="admin_home"),
    path('index', views.index, name='index'),
]