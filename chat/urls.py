from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path('', views.index, name="index"),
    path('create-room/', views.create_room,name='create_room'),
    path('<str:room_code>/', views.room, name='room')
]