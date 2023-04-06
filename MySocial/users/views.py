from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from userProfile.models import UserProfile
from .models import User
from .forms import UserRegisterForm



# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect("posts:index") 
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            # Check Username
            if User.objects.filter(username=form.cleaned_data.get('username')).exists():
                messages.error(request,'That Username is taken!')
                return redirect('users:register')
            # Check Email
            elif not User.objects.filter(email=form.cleaned_data.get('email')).exists():
                #check password
                if form.cleaned_data['password1'] != form.cleaned_data['password2']:
                    messages.error(request, 'Password do not match!')
                    return redirect('users:register')
                
                messages.success(request,'Account Successfully created')
                new_user = form.save()
                
                # create a profile object for the new user
                username = form.cleaned_data.get('username')
                user_model = User.objects.get(username=username)
                new_profile = UserProfile.objects.create(user=user_model )
                new_profile.save()
                return redirect('users:login') 
            else:
                messages.error(request, 'That email is being used!')
                return redirect('users:register')
                               
    else:
       form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request,'users/register.html',context)

        


def login_view(request):

    if request.user.is_authenticated:
        return redirect("posts:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)      
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in!")
                return redirect("posts:index")
            else:
                messages.warning(request, "email or password is incorrect")
                return redirect("users:login")
        except:
            messages.warning(request, f'User does not exist !.')
        

    return render(request, "users/login.html")


@login_required(login_url='users:login')
def logout_view(request):
    logout(request)
    messages.success(request, "You are now logged out!")
    return redirect('users:login')

