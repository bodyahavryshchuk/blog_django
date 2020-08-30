from django.urls import path
from . import views


urlpatterns = [
    path('list/<str:username>/', views.message_list_by_user, name='message_list_by_user'),
    path('', views.message_list, name='message_list'),
    path('registration/', views.user_registration, name='registration'),
]
