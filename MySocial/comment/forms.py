from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control border-0 rounded-pill bg-gray', 'placeholder':'Write a comment...'}))
    class Meta:
        model = Comment
        fields = ['body']