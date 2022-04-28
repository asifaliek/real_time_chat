from django.urls import path
from . import views

app_name = "pearsonal_chat"

urlpatterns = [
    path('create-personal-chat/', views.create_personal_chat,name='create_personal_chat'),
    path('<str:username>/', views.lobby, name='lobby')
]