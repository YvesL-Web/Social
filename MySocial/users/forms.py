from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
 
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-3 shadow',"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control my-3 shadow',"placeholder":"Confirm Password"}))
    class Meta:
        model = User
        fields = ['username','email']

        widgets= {
            'username' : forms.TextInput(attrs={'class':'form-control my-3 shadow','placeholder':'Username'}),
            'email' :forms.EmailInput(attrs={'class':'form-control my-3 shadow','placeholder':'Email'}),
        }

