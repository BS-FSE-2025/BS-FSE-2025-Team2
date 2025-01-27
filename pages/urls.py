from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('main/', views.main, name='main'),
    path('logout/', views.user_logout, name='user_logout'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('popular_fields/', views.popular_fields, name='popular_fields'),
    path('about_us/', views.About_us, name='about_us'),
    path('upcoming_events/', views.upcoming_events, name='upcoming_events'),
 ]
