from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('management/drivers/', views.admin_drivers, name='admin_drivers'),
    path('management/users/', views.admin_users, name='admin_users'),
    path('management/deliveries/', views.admin_deliveries, name='admin_deliveries'),
    path('management/warehouses/', views.admin_warehouses, name='admin_warehouses'),
    path('management/feedback/', views.admin_feedback, name='admin_feedback'),
    path('management/settings/', views.admin_settings, name='admin_settings'),
    path('my-shipments/', views.client_shipments, name='client_shipments'),
    path('my-tasks/', views.driver_tasks, name='driver_tasks'),
    path('dispatcher/deliveries/', views.dispatcher_deliveries, name='dispatcher_deliveries'),
    path('dispatcher/warehouses/', views.dispatcher_warehouses, name='dispatcher_warehouses'),
    path('management/users/add/', views.add_user, name='add_user'),
    path('management/users/edit/<int:pk>/', views.edit_user, name='edit_user'),
    path('management/users/delete/<int:pk>/', views.delete_user, name='delete_user'),
]
