from django.urls import path
from . import views

app_name = "friends"

urlpatterns = [
    path('friend_request/', views.send_friend_request_view, name="send-friend-request"),
    path('show_friend_request/<user_id>', views.show_friend_requests_view, name="show-friend-requests"),
    path('accept_friend_request/<request_id>/', views.accept_friend_request, name="accept-friend-request"),
    # path('test/<friend_request_id>/', views.accept_friend_request, name="accept-friend-request"),
]
