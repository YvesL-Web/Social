from django.shortcuts import render, redirect, get_object_or_404
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
            return redirect('userProfile:profile')
        
    context = {
       'user_info': user_profile 
    }

    return render (request,'userProfile/profile.html',context)

def profile(request, id):
    pass