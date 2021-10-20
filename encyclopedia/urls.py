from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("<str:title>", views.title, name="title")
]
