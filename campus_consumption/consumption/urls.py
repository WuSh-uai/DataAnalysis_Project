from django.urls import path
from . import views

app_name = 'consumption'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('index/', views.index_view, name='index'),
    path('list/', views.list_view, name='list'),
]