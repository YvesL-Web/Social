from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from users.models import User
# from .models import Chat
from .models import ChatMessage
from friends.models import FriendsList
# Create your views here.
  
@login_required(login_url='users:login')
def index(request):
    user = request.user
    context = {}
    friend_list = FriendsList.objects.get(user = user)
    friends = []
    for friend in friend_list.friends.all():
        friends.append(friend)
    context["friend_list"] = friends
    return render(request, 'chat/index.html', context)

@login_required(login_url='users:login')
def single_chat(request, *args, **kwargs):
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

        if user == this_user:
            messages.info(request,"You can't send a message to yourself..Make no sense!!.")
            return redirect("userProfile:profile_view",this_user.id) 
        # Must be friends to send a message
        if user != this_user:
            if not user in friend_list.friends.all():
                messages.info(request,"You must be friend to send a message.")
                return redirect("userProfile:profile_view",this_user.id)  
        
              
        chats = ChatMessage.objects.all()
        nbr_msg_between_user =  ChatMessage.objects.filter(sender=this_user, receiver=user)
        nbr_msg_between_user.update(is_read=True)
        context["nbr_msg"] = nbr_msg_between_user.count()
        context["chats"] = chats
    return render(request, 'chat/single_chat.html', context)

@login_required(login_url='users:login')
def send_message(request, *args, **kwargs):
    if request.method == "POST":
        # current login user
        user_id = kwargs.get("user_id") 
        this_user = User.objects.get(pk=user_id)
        sender = User.objects.get(username=request.user.username)
        receiver = this_user
        body = request.POST['body']
        if body:
            chat_message  = ChatMessage(sender=sender, receiver=receiver, body=body)
            chat_message.save()
            success = f'Message Sent'
            return JsonResponse(success, safe=False)
        else:
            messages.error(request, "The message can't be empty")
            return redirect("chat:single_chat", this_user.id)
        

def received_messages(request, *args, **kwargs):
    user = User.objects.get(username=request.user.username)
    user_id = kwargs.get("user_id") 
    this_user = User.objects.get(pk=user_id)
    chats = ChatMessage.objects.filter(sender=this_user, receiver=user)
    chats_list=[]
    for chat in chats:
        chats_list.append(chat.body)
    return JsonResponse(chats_list, safe=False)

def messages_notifications(request):
    user = User.objects.get(username=request.user.username)
    arr=[]
    
    try:
        friend_list = FriendsList.objects.get(user=user)
    except FriendsList.DoesNotExist:
        return HttpResponse(f"Could not find a friends list for {user.username}")
    
    for friend in friend_list.friends.all():
        chat_messages = ChatMessage.objects.filter(sender__id=friend.id, receiver=user, is_read=False)
        arr.append(chat_messages.count())
    return  JsonResponse(arr, safe=False)

