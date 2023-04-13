from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
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
            return redirect('userProfile:profile')
        
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
        userprofile = UserProfile.objects.get(pk=user_id)
    except UserProfile.DoesNotExist:
        return HttpResponse("That user doesn't exist.")
    if userprofile:
        context['id'] = userprofile.id
        context['username'] = userprofile.user.username
        context['email'] = userprofile.user.email
        context['profile_img'] = userprofile.profile_img.url
        
        # Define state template
        is_self = True
        is_friend = False
        auth_user = request.user
        if auth_user.id != userprofile.id :
            is_self = False
        elif not auth_user.is_authenticated:
            is_self = False
        context['is_self'] = is_self
        context['is_friend'] = is_friend

        return render(request, "userProfile/userprofile.html", context)