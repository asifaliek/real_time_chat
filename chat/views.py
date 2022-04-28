import json
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse

from .models import Room, Message
from .forms import ChatRoomForm
from personal_chat.forms import PersonalChatForm
from personal_chat.models import Thread,PersonalMessage

@login_required
def index(request):
    user = request.user
    rooms = Room.objects.all()
    active_rooms = []
    for room in rooms:
        members = room.users.all()
        if user in members:
            active_rooms.append(room)

    all_members = User.objects.filter(is_active=True)
    threads = Thread.objects.all()
    active_threads = []
    for thread in threads:
        members = thread.users.all()
        if user in members:
            active_threads.append(thread)


    context = {
        "active_rooms": active_rooms,
        "active_threads":active_threads,
        "all_members": all_members,
        "gform": ChatRoomForm(),
        "pform":PersonalChatForm()
    }
    return render(request, 'chat/index.html', context)


@login_required
def create_room(request):
    if request.method == "POST":
        form = ChatRoomForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.creator = request.user
            data.save()
            users = form.cleaned_data['users']
            for user in users:
                data.users.add(user)
                data.users.add(request.user)
            return redirect('/')
        else:
            return JsonResponse({"error": form.errors})
    else:
        form = ChatRoomForm()
        context = {'form':form}
        return render(request, 'chat/room_form.html', context)


@login_required
def room(request, room_code):
    user = request.user
    try:
        room = Room.objects.get(code=room_code, users=request.user)
    except:
        return HttpResponseForbidden()
    username = request.user.username
    members = room.users.all()

    chats = []
    chats = Message.objects.filter(room=room)

    all_members = User.objects.filter(is_active=True)

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

    return render(request, 'chat/chat.html', {
        'room_code': room.code,
        "username": username,
        "room": room,
        "members": members,
        "all_members": all_members,
        "active_rooms": active_rooms,
        "active_threads":active_threads,
        "chats":chats,
        "gform": ChatRoomForm(),
        "pform": PersonalChatForm()
    })

