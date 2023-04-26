from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json

from users.models import User
from friends.models import FriendRequest, FriendsList

# Create your views here.
@login_required(login_url='users:login')
def friend_list_view(request, *args, **kwargs):
    context = {}
    user = request.user
    user_id = kwargs.get("user_id")
    if user_id:
        try:
            this_user = User.objects.get(pk=user_id)
            context["this_user"] = this_user
        except User.DoesNotExist:
            return HttpResponse("That user does not exist.")
        
        try:
            friend_list = FriendsList.objects.get(user= this_user)
        except FriendsList.DoesNotExist:
            return HttpResponse(f"Could not find a friends list for {this_user.username}")
        
        # Must be friends to view a friend list
        if user != this_user:
            if not user in friend_list.friends.all():
                messages.info(request,"You must be friend to view their friends list.")
                return redirect("userProfile:profile_view",this_user.id)
            
        friends = [] # [(User1, True), (User2, False),...]
        user_friend_list = FriendsList.objects.get(user = user)
        
        for friend in friend_list.friends.all():
            friends.append((friend, user_friend_list.is_mutual_friend(friend)))
        context['friends'] = friends
    else:
        return HttpResponse("You must be friend to view their friends list.")
    return render(request, "friends/friends_list.html", context )


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


@login_required(login_url='users:login')
def remove_friend(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST":
        user_id = request.POST["receiver_user_id"]
        if user_id:
            try:
                removee = User.objects.get(pk=user_id)
                friend_list = FriendsList.objects.get(user=user)
                friend_list.unfriend(removee)
                payload['response'] = "Successfully removed that friend."
            except Exception as e:
                payload['response'] = f"Something wnt wrong: {str(e)}."
        else:
            payload['response'] = "There was an error. Unable to remove that friend."
    else:
        payload['response'] = "You must be authenticated to remove a friend."
    return JsonResponse(payload)


@login_required(login_url='users:login')
def decline_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "GET":
        friend_request_id = kwargs.get("friend_request_id")
        if friend_request_id:
            friend_request = FriendRequest.objects.get(pk=friend_request_id)
            # Confirm that is the correct request
            if friend_request:
                if friend_request.receiver == user:
                    # Found the request. Now delcine it 
                    friend_request.decline()
                    payload['response'] = "Friend request decline."
                else:
                    payload['response'] = "Something went wrong."
            else:
                payload['response'] = "That's not yoour friend request to decline."
        else:
            payload['response'] = "Unable to decline that friend request"
    else:
        payload['response'] = "You must be authenticated to decline a friend request."
    
    return JsonResponse(payload)
   
    
@login_required(login_url='users:login')
def cancel_friend_request(request, *args, **kwargs):
    user = request.user
    payload = {}
    if request.method == "POST":
        user_id = request.POST["receiver_user_id"]
        if user_id:
            receiver = User.objects.get(pk=user_id)
            try:
                friend_requests = FriendRequest.objects.filter(sender=user, receiver=receiver, is_active=True)
            except Exception as e:
                payload['response'] = "Nothing to cancel. Friend request does not exist."
            # There should only ever be a single active friend request at any given time. 
            # cancel them all just in case.
            if len(friend_requests) > 1:
                for request in friend_requests:
                    request.cancel()
                payload["response"] ="Friend request cancelled."
            else:
                friend_requests.first().cancel()
                payload["response"] = "Friend request cancelled."
        else:
            payload["response"] = "unable to cancel that friend request."
    else:
        payload['response'] = "you must be authenticated to cancel a friend request."

    return JsonResponse(payload)
