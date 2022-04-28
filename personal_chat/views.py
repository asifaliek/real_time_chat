import json
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse
from .models import PersonalMessage,Thread
from .forms import PersonalChatForm
from chat.forms import ChatRoomForm
from chat.models import Room
# Create your views here.


@login_required
def create_personal_chat(request):
    if request.method == "POST":
        form = PersonalChatForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            users = form.cleaned_data['users'].all()
            name = [i.username for i in users if i.username != request.user.username]
            data.name=name[0]
            data.save()
            form.save_m2m()
            return redirect('/')
        else:
            return JsonResponse({"error": form.errors})


@login_required
def lobby(request, username):
    user = request.user
    try:
        lobby = Thread.objects.get(name=username)
    except:
        return HttpResponseForbidden()
    my_username = request.user.username

    chats = []
    chats = PersonalMessage.objects.filter(thread=lobby)

    all_rooms = Room.objects.all()
    active_rooms = []
    for i in all_rooms:
        members_list = i.users.all()
        if request.user in members_list:
            active_rooms.append(i)

    threads = Thread.objects.all()
    active_threads = []
    for thread in threads:
        members = thread.users.all()
        if user in members:
            active_threads.append(thread)

    current_site = get_current_site(request).domain
    if request.is_secure():
        protocol = "https://"
    else:
        protocol = "http://"

    return render(request, 'chat/personalchat.html', {
        "username": username,
        "my_username": my_username,
        "lobby": lobby,
        "active_rooms": active_rooms,
        "chats":chats,
        "active_threads":active_threads,
        "gform": ChatRoomForm(),
        "pform": PersonalChatForm()
    })

