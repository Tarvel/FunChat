from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("room/<str:pk>", views.room, name="room"),
    path("profile/<str:username>", views.userProfile, name="user-profile"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("complete_profile/", views.completeProfile, name="create-profile"),
    path("create_room/", views.createRoom, name="create-room"),
    path("update_room/<str:pk>", views.updateRoom, name="update-room"),
    path("delete_room/<str:pk>", views.deleteRoom, name="delete-room"),
    path("delete_message/<str:pk>", views.deleteMessage, name="delete-message"),
    path("update_profile/", views.updateUser, name="update-profile"),
    path("browse_topics", views.topicsPage, name="topics-page"),
    path("recent_activities", views.activityPage, name="activity"),
]
