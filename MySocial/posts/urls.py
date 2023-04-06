from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name='posts'

urlpatterns = [
    path('',views.post, name='index' ),
    path('upload/',views.upload, name='upload' ),
    path('single-post/<uuid:id>',views.single_post, name='single_post' ),
    path('like/',csrf_exempt(views.like_post), name='like' ),
    path('delete_post/<uuid:id>',views.delete_post, name='delete_post' ),
    path('delete_comment/<str:id>',views.delete_comment, name='delete_comment' ),
    path('edit_comment/<str:id>',views.edit_comment, name='edit_comment' ),
 
    
]
