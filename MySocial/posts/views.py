from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from chat.models import Chat

from comment.models import Comment
from comment.forms import CommentForm
from users.models import User
from .models import Post
from userProfile.models import UserProfile
# User = get_user_model()


# Create your views here.
@login_required(login_url='users:login')
def post(request):
    # user_object = User.objects.get(username=request.user.username)
    posts= Post.objects.all()
    comment = Comment.objects.select_related('post').all()
    # messages
    user = request.user
    chat_user = Chat.get_message(user=user)
    active_message = None
    messages = None

    if chat_user:
        message = chat_user[0]
        active_message = message['user'].username
        messages = Chat.objects.filter(user=user, receiver=message['user'])
        messages.update(is_read=True)

        for message in chat_user:
            if message['user'].username == active_message:
                message['unread'] = 0
    # print(chat_user)
    context = {
        # post
        'posts':posts.order_by('-created_at'),
        'comments': comment.order_by('-created_at'),
        # message
        'chat_user': chat_user, 
        'active_message' : active_message,
        'user_messages' : messages,  
    }
    return render(request,'posts/index.html',context)

@login_required(login_url='users:login')
def upload(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user.username)
        image = request.FILES['image']
        caption=request.POST['caption']
      
        new_post = Post.objects.create(user=user, image=image,caption=caption)
        new_post.save()
        return redirect("posts:index")

@login_required(login_url='users:login')
def single_post(request, id):
    post = get_object_or_404(Post, id=id)
    user_object = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user_object)
    comment = Comment.objects.filter(post=post).order_by('-created_at')
    len_comment = len(Comment.objects.filter(post=post))
    # add_comment
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user_object
            comment.save()
            # return HttpResponseRedirect(reverse('posts:single_post', args=[id]))
            return redirect('posts:single_post', id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'user_profile': user_profile,
        'comments': comment,
        'len_comment': len_comment,
        'form':form,
    }
    return render(request, 'posts/post_detail.html', context)

# delete_post
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.user != post.user :
        messages.info(request,"it's not your post.cmon")
        return redirect('posts:index')
    else:
        post.delete()
        return redirect('posts:index')

#delete_comment
@login_required(login_url='users:login')
def delete_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    post = get_object_or_404(Post, id=comment.post.id)
    
    if request.user != comment.user :
        messages.info(request,"it's not your comment")
        return redirect('posts:single_post',post.id)
    else:
        comment.delete()
        return redirect('posts:single_post',post.id)


# edit_comment
@login_required(login_url='users:login')
def edit_comment(request, id):
    comment = get_object_or_404(Comment, id=id)
    post = get_object_or_404(Post, id = comment.post.id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.post = post
            comment.user = request.user
            comment.body = form.cleaned_data['body']
            comment.save()
            return redirect("posts:single_post",post.id)
    else:
        form = CommentForm()
        return redirect("posts:index")
    return redirect("posts:single_post",post.id)

# like function
@login_required(login_url='users:login')
def like_post(request):
    if request.POST.get('action') == "post":
        result = ''
        id = request.POST.get('postid')
        # user = User.objects.get(username=request.user.username) 
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.like_count -=1
            result = post.like_count
            post.save()
        else:
            post.likes.add(request.user)
            post.like_count +=1
            result= post.like_count
            post.save()

        return JsonResponse({'result':result})


# @login_required(login_url='users:login')
# def like_post(request, post_id):
#     user = User.objects.get(username=request.user.username)
#     # post_id = request.GET.get('post_id')
#     post=Post.objects.get(id=post_id)
#     current_likes = post.likes
#     liked = Likes.objects.filter(user=user.username, post=post).count()
#     if not liked:
#         liked  = Likes.objects.create(user=user, post=post)
#         current_likes +=1
#     else:
#         liked  = Likes.objects.filter(user=user, post=post).delete()
#         current_likes -=1
#     post.likes = current_likes
#     post.save()
#     return HttpResponseRedirect(reverse('index'))




