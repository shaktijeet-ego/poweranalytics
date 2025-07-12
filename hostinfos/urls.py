from django.urls import path
from . import views
from .views import region_lists, home_view

urlpatterns = [
    #path('hosts/', views.host_list, name='host_list'),
    path('regions/', region_lists, name='region_list'),
    path('', home_view, name='home'),
    path('hosts/', views.host_list_view, name='host_list'),
    path('hosts/edit/<int:host_id>/', views.host_edit_view, name='host_edit'),
    path('hosts/delete/<int:host_id>/', views.host_delete_view, name='host_delete'),
    path('hosts/ajax_search/', views.ajax_host_list, name='ajax_host_list'),
    path('hosts/deleted/', views.deleted_hosts_view, name='deleted_hosts'),
    path('hosts/recover/<int:host_id>/', views.recover_host_view, name='recover_host'),
]



    #urlpatterns += [
    #path('edit-host/', host_edit_view, name='edit_host'),
#]