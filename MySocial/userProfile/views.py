from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from users.models import User
from friends.models import FriendsList, FriendRequest
from friends.utils import get_friend_request_or_false
from friends.friend_request_status import FriendRequestStatus
# Create your views here.

@login_required(login_url='users:login')
def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":

        if request.FILES.get('image') == None:
            image= user_profile.profile_img
            name= request.POST['name']
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_img= image
            user_profile.name = name
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
            messages.success(request,"Profile updated.")
            return redirect('userProfile:profile_view',user_profile.id)
        
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            name= request.POST['name']
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_img= image
            user_profile.name = name
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
            messages.success(request,"Profile updated.")
            return redirect('userProfile:profile_view',user_profile.id)
        
    context = {
       'user_info': user_profile 
    }

    return render (request,'userProfile/profile.html',context)

@login_required(login_url='users:login')
def profile_view(request,*args, **kwargs):
    
    context = {}
    user_id = kwargs.get("user_id")
    try:
        user = User.objects.get(pk=user_id)
       
    except UserProfile.DoesNotExist:
        return HttpResponse("That user doesn't exist.")
    if user:
        context['id'] = user.id
        context['username'] = user.username
        context['email'] = user.email
        context['profile_img'] = user.userprofile.profile_img.url
        
        try:
            friend_list = FriendsList.objects.get(user = user )
        except FriendsList.DoesNotExist:
            friend_list = FriendsList(user = user)
            friend_list.save()
        friends = friend_list.friends.all()
        context['friends'] = friends
            

        # Define state template
        is_self = True
        is_friend = False
        request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        friend_requests = None
        auth_user = request.user
        if auth_user.id != user.id :
            is_self = False
            if friends.filter(pk = auth_user.id):
                is_friend = True
            else :
                is_friend = False

                #Case1: request has been sent from them to you
                if get_friend_request_or_false(sender=user, receiver=auth_user) != False:
                    request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
                    context['pending_friend_request_id'] = get_friend_request_or_false(sender=user, receiver=auth_user).id
                #Case2: request has been sent by you to them
                elif get_friend_request_or_false(sender=auth_user, receiver=user) != False:
                    request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
                else:
                #Case3: No request has been sent
                    request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
        elif not auth_user.is_authenticated:
            is_self = False
        else:
            try:
                friend_requests = FriendRequest.objects.filter(receiver=auth_user, is_active=True)
            except:
                pass

        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['request_sent'] = request_sent
        context['friend_requests'] = friend_requests
        return render(request, "userProfile/userprofile.html", context)
    

def profile_search_view(request, *args, **kwargs):
    context={}
    if request.method == "GET":
        search_query = request.GET["q"]
        if len(search_query) > 0:
            search_results = User.objects.filter(username__icontains=search_query)
            user = request.user
            profiles = [] # [(profile1, True),(profile2, False)]
            for profile in search_results:
                profiles.append((profile, False))   
            context['profiles'] = profiles
            
            
    return render (request, "userProfile/search_result.html", context)