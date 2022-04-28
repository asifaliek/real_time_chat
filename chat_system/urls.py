
from django.contrib import admin
from django.urls import path,include
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns = [
 
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register,name="registrer_user"),

    path('', include('chat.urls',namespace="chat")),
    path('personal_chat/', include('personal_chat.urls',namespace="personal_chat")),
]
