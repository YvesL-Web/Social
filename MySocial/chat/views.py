from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from users.models import User
# from .models import Chat
from .models import ChatMessage
from friends.models import FriendsList
# Create your views here.

# @login_required(login_url='users:login')
# def inbox(request):
#     user = request.user
#     chats = Chat.get_message(user=user)
#     active_message = None
#     messages = None
#     if chats:
#         message = chats[0]
#         active_message = message['user'].username
#         messages = Chat.objects.filter(user=user, receiver=message['user'])
#         messages.update(is_read=True)

#         for message in chats:
#             if message['user'].username == active_message:
#                 message['unread'] = 0
#         context ={
#             'messages' : messages,
#             'active_message' : active_message,
#             'chats': chats, 
#         }
#         return render (request, 'posts/index.html', context)

# @login_required(login_url='users:login') 
# def index(request):
#     context={}
#     user = request.user
#     messages = Chat.get_message(user=user)
#     active_chat = None
#     chats = None
    
#     if messages:
#         message = messages[0]
#         active_chat = message['user'].username
#         chats = Chat.objects.filter(user = user, receiver=message['user'])
#         chats.update(is_read=True)
#         for message in messages:
#             if message['user'].username == active_chat:
#                 message['unread'] = 0
#         context = {
#         'messages': messages,
#         'chats' : chats,
#         'active_chat': active_chat
#         }
    
#     return render(request, 'chat/index.html', context)

# @login_required(login_url='users:login')
# def single_chat(request, username):
#     user = request.user
#     messages = Chat.get_message(user=user)
#     active_chats = username
    
#     chats = Chat.objects.filter(user=user, receiver__username=username)
#     chats.update(is_read=True)
#     for message in messages:
#         if message['user'].username == username:
#             message['unread'] = 0 
#     context = {
#        'messages': messages,
#        'chats' : chats,
#        'active_chats': active_chats
#     }
#     return render(request, 'chat/single_chat.html', context)

# @login_required(login_url='users:login')
# def send_message(request):
#     if request.method == "POST":
#         from_user = request.user
#         to_user_username = request.POST['to_user']
#         message = request.POST['message']
#         to_user = User.objects.get(username = to_user_username)
#         Chat.sender_message(from_user, to_user, message)
#         success = 'Message Sent'
#         return HttpResponse(success)
    
@login_required(login_url='users:login')
def index2(request):
    user = request.user
    context = {}
    friend_list = FriendsList.objects.get(user = user)
    friends = []
    for friend in friend_list.friends.all():
        friends.append(friend)
    context["friend_list"] = friends
    return render(request, 'chat/index.html', context)

@login_required(login_url='users:login')
def single_chat2(request, *args, **kwargs):
    context = {}
    user = request.user
    user_id = kwargs.get("user_id")  
    
    if user_id:
        try:
            this_user = User.objects.get(pk=user_id)
            context["this_user"] = this_user
            
            
        except:
            return HttpResponse("That user does not exist.")
        
        try:
            friend_list = FriendsList.objects.get(user= this_user)
        except FriendsList.DoesNotExist:
            return HttpResponse(f"Could not find a friends list for {this_user.username}")

        # Must be friends to send a message
        if user != this_user:
            if not user in friend_list.friends.all():
                messages.info(request,"You must be friend to send a message.")
                return redirect("userProfile:profile_view",this_user.id)
            
        if request.method == "POST":
            # current login user
            sender = User.objects.get(username=request.user.username)
            receiver = this_user
            body = request.POST['body']
            chat_message  = ChatMessage(sender=sender, receiver=receiver, body=body)
            chat_message.save()
            
            return redirect("chat:single_chat", this_user.id)
        
            
        chats = ChatMessage.objects.all()
        context["chats"] = chats
        print(context)
    return render(request, 'chat/single_chat.html', context)


def send_message(request):
    return JsonResponse("it is working", safe=False)