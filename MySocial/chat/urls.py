from django.urls import path
from . import views

app_name= "chat"

urlpatterns = [
    path('', views.index, name="index"),
    path("<username>", views.single_chat, name="single_chat"),
    path("send_message/", views.send_message, name="send_message"),
    # test
    path('',views.index2, name ="index2"),
    path('<str:pk>',views.index2, name ="single_chat2"),
]
