from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json

from users.models import User
from friends.models import FriendRequest

# Create your views here.

@login_required(login_url='users:login')
def show_friend_requests_view(request, *args, **kwargs):
    context = {}
    user = request.user
    user_id = kwargs.get("user_id")
    user_object = User.objects.get(pk=user_id)
    if user_object == user:
        friend_requests = FriendRequest.objects.filter(receiver= user_object, is_active = True)
        context['friend_requests'] = friend_requests
    else:
        return HttpResponse("You can't view another users friend requests.")
    return render(request, "friends/show_friend_requests.html", context)

@login_required(login_url='users:login')
def send_friend_request_view(request, *args, **kwargs):
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
    # return HttpResponse(json.dumps(payload), content_type="application/json")
    return JsonResponse(payload)


@login_required(login_url='users:login')
def accept_friend_request(request, request_id):
    user = request.user
    payload= {}
    if request.method == "GET":
        # friend_request_id = kwargs.get("friend_request_id")
        friend_request_id = request_id
        if friend_request_id :
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            # Confirm that is the correct request
            if friend_request.receiver == user:
                if friend_request:
                    #found the request. now accept it
                    friend_request.accept()
                    payload['response'] = "Friend request accepted."
                else:
                    payload['response'] = "something went wrong."
            else:
                payload['response'] = "That is not your request to accept."
        else:
            payload['response'] = "Unable to accept that friend request."
    else:
        payload['response'] = "You must be authenticated to accept a friend request."
    
    # return HttpResponse(json.dumps(payload), content_type="application/json")
    return JsonResponse(payload)
    