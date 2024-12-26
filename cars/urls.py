from django.urls import path

from . import views

urlpatterns = [
    path("", views.homepage, name=""),
    path("register/", views.register, name="register"),
    path("login/", views.login1, name="login"),
    path("loginpage", views.loginpage, name="loginpage"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("user_logout", views.user_logout, name="user_logout"),
    # parking_spaces
    path('parking_spaces/', views.parking_space_list, name='parking_space_list'),
    path('parking_spaces/<int:id>/', views.parking_space_detail, name='parking_space_detail'),
    path('parking_spaces/create/', views.parking_space_create, name='parking_space_create'),
    path('parking_spaces/<int:id>/update/', views.parking_space_update, name='parking_space_update'),
    path('parking_spaces/<int:id>/delete/', views.parking_space_delete, name='parking_space_delete'),
    path('provider/rental-history/', views.provider_rental_history, name='provider_rental_history'),
    path('provider/total-earning/', views.provider_total_earning, name='provider_total_earning'),
    path('provider/view_customer/<int:customer_id>/', views.view_customer_info, name='view_customer_info'),
]
