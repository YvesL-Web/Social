from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from users.models import User
from .models import Chat
# Create your views here.

@login_required(login_url='users:login')
def inbox(request):
    user = request.user
    chats = Chat.get_message(user=user)
    active_message = None
    messages = None
    if chats:
        message = chats[0]
        active_message = message['user'].username
        messages = Chat.objects.filter(user=user, receiver=message['user'])
        messages.update(is_read=True)

        for message in chats:
            if message['user'].username == active_message:
                message['unread'] = 0
        context ={
            'messages' : messages,
            'active_message' : active_message,
            'chats': chats, 
        }
        return render (request, 'posts/index.html', context)

@login_required(login_url='users:login') 
def index(request):
    user = request.user
    messages = Chat.get_message(user=user)
    active_chat = None
    chats = None
    
    if messages:
        message = messages[0]
        active_chat = message['user'].username
        chats = Chat.objects.filter(user = user, receiver=message['user'])
        chats.update(is_read=True)
        for message in messages:
            if message['user'].username == active_chat:
                message['unread'] = 0
        context = {
        'messages': messages,
        'chats' : chats,
        'active_chat': active_chat
        }
    
    return render(request, 'chat/index.html', context)

@login_required(login_url='users:login')
def single_chat(request, username):
    user = request.user
    messages = Chat.get_message(user=user)
    active_chats = username
    
    chats = Chat.objects.filter(user=user, receiver__username=username)
    chats.update(is_read=True)
    for message in messages:
        if message['user'].username == username:
            message['unread'] = 0 
    context = {
       'messages': messages,
       'chats' : chats,
       'active_chats': active_chats
    }
    return render(request, 'chat/single_chat.html', context)

@login_required(login_url='users:login')
def send_message(request):
    if request.method == "POST":
        from_user = request.user
        to_user_username = request.POST['to_user']
        message = request.POST['message']
        to_user = User.objects.get(username = to_user_username)
        Chat.sender_message(from_user, to_user, message)
        success = 'Message Sent'
        return HttpResponse(success)
    

def index2 (request):
    context = {}
    return render(request, 'chat/index2.html', context)

def detail(request, pk):
    context={}
    return render(request,"chat/single_chat2.html",context)