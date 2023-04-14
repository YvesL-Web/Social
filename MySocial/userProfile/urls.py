from django.urls import path
from . import views

app_name="userProfile"

urlpatterns = [
    path('', views.edit_profile, name='profile'),
    path('<user_id>', views.profile_view, name='profile_view'),
    path('search/', views.profile_search_view, name="search")
]
