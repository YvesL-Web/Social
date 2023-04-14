from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json

from users.models import User
from friends.models import FriendRequest

# Create your views here.

@login_required(login_url='users:login')
def send_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST":
        user_id = request.POST.get("receiver_user_id")
        if user_id:       
            receiver = User.objects.get(pk=user_id)
            try:
                # Get any friend requests(active and not-active)
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver)
                # find if any of them are active
                try:
                    for request in friend_requests:
                        if request.is_active:
                            raise Exception("You have already sent them a friend request.")
                    # if none are active, then create a new friend request
                    friend_request = FriendRequest(sender=user, receiver=receiver)
                    friend_request.save()
                    # payload['result'] = "success"
                    payload['response'] = "Friend request sent."
                except Exception as e:
                    # payload['result'] = 'error'
                    payload['response'] = str(e)
            #if the FriendRequest object doesn't exist.
            except FriendRequest.DoesNotExist:
                # There are no friend requests create one
                friend_request = FriendRequest(sender=user, receiver=receiver)
                friend_request.save()
                payload['response'] = "Friend request sent."

            if payload['response'] == None:
                payload['response'] = "Something went wrong."
        else:
            payload['response'] = "Unable to send a friend request"
    else:
        payload['response'] = " You must be authenticated to send a friend request.!"
    return HttpResponse(json.dumps(payload), content_type="application/json")