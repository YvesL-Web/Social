# Function
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

# different Model

# class Chat(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
#     message = models.TextField()
#     date = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)

#     def sender_message(from_user, to_user, message):
#         sender_message = Chat(
#            user = from_user,
#            sender = from_user,
#            receiver= to_user,
#            message = message,
#            is_read = True   
#         )
#         sender_message.save()

#         receiver_message = Chat(
#            user = to_user,
#            sender = from_user,
#            receiver= from_user,
#            message = message,
#            is_read = True   
#         )
#         receiver_message.save()
    
#         return sender_message
     
#     def get_message(user):
#         users = []
#         messages = Chat.objects.filter(user = user).values('receiver').annotate(last=Max('date')).order_by('-last')
#         for message in messages:
#             users.append({
#                 'user':User.objects.get(pk=message['receiver']),
#                 'last': message['last'],
#                 'unread': Chat.objects.filter(user=user, receiver__pk=message['receiver'], is_read=False).count()
#             })
#         return users