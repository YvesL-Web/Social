from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Chat
# Create your views here.

@login_required(login_url='users:login')
def inbox(request):
    user = request.user
    chats = Chat.get_message(user=user)
    active_message = None
    messages = None
    print(user)
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