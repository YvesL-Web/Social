from django.db import models
from users.models import User 
from django.db.models import Max
# Create your models here.

class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def send_message(from_user, to_user, message):
        sender_message = Chat(
           user = from_user,
           sender = from_user,
           receiver= to_user,
           message = message,
           is_read = True   
        )
        sender_message.save()

        receiver_message = Chat(
           user = from_user,
           sender = from_user,
           receiver= to_user,
           message = message,
           is_read = True   
        )
        receiver_message.save()
    
        return sender_message
     
    def get_message(user):
        users = []
        messages = Chat.objects.filter(user = user).values('receiver').annotate(last=Max('date')).order_by('-last')
        for message in messages:
            users.append({
                'user':User.objects.get(pk=message['receiver']),
                'last': message['last'],
                'unread': Chat.objects.filter(user=user, receiver__pk=message['receiver'], is_read=False)
            })
        return users