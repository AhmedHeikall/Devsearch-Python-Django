from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login-page"),
    path("logout/", views.logout_page, name="logout-page"),
    path("register/", views.register_page, name="register-page"),

    path("developers/", views.profiles, name="profiles-page"),
    path("developers/<str:pk>/", views.profile, name="profile-page"),

    path("account/", views.user_account, name="user-account-page"),
    path("edit-account", views.edit_account, name="edit-account-page"),

    path("create-skill/", views.create_skill, name="create-skill-page"),
    path("update-skill/<str:pk>", views.update_skill, name="update-skill-page"),
    path("delete-skill/<str:pk>", views.delete_skill, name="delete-skill-page"),

    path("inbox/", views.inbox, name="inbox-page"),
    path("inbox/message/<str:pk>/", views.view_message, name="view-message-page"),
    path("create-message/<str:pk>/", views.create_message, name="create-message-page"),


]