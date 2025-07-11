from django.urls import path
from . import views
from .views import region_lists

urlpatterns = [
    #path('hosts/', views.host_list, name='host_list'),
    path('regions/', region_lists, name='region_list'),
]