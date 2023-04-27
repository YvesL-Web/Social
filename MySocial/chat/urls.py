from django.urls import path
from . import views

app_name= "chat"

urlpatterns = [
    path('', views.index, name="index"),
    path("<user_id>", views.single_chat, name="single_chat"),
    path("send_message/<user_id>", views.send_message, name="send_message"), 
    path("received_message/<user_id>", views.received_messages, name="received_message"), 
    path("messages_notifications/", views.messages_notifications, name="messages_notifications"), 
    
    # other
    # path("send_message/", views.send_message, name="send_message"), 
    # path('',views.index, name ="index"),
    # path('<username>',views.single_chat, name ="single_chat"),
]
