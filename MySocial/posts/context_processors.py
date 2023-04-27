from users.models import User
from friends.models import FriendRequest, FriendsList
from chat.models import ChatMessage

def extras(request):
    if (request.user.username):
        context={}
        total_msg=[]

        user = request.user
        user_object = User.objects.get(username=request.user.username)
        
        # check friendrequest
        if user_object == user:
            friend_requests = FriendRequest.objects.filter(receiver= user_object, is_active = True)
        # check number of messages
        friend_list = FriendsList.objects.get(user=user_object)
        for friend in friend_list.friends.all():
            chat_messages = ChatMessage.objects.filter(sender__id=friend.id, receiver=user, is_read=False)
            total_msg.append(chat_messages.count())

        context = {
            'friend_requests': friend_requests,
            'total_msg': sum(total_msg)
        }
        
        return context
    return{}

