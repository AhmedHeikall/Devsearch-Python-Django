from django.urls import path
from . import views

urlpatterns = [
    path("projects/", views.projects, name="projects-page"),
    path("projects/<str:pk>/" , views.project, name="single-project-page"),

    path("create-project/", views.create_project, name="create-project-page"),
    path("ubdate-project/<str:pk>/", views.ubdate_project, name="ubdate-project-page"),
    path("delete-project/<str:pk>/", views.delete_project, name="delete-project-page"),
]