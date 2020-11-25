from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("create/submit", views.submit_creation, name="submit_creation"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("edit/submit/<str:title>", views.submit_edit, name="submit_edit"),
    path("random", views.random_page, name="random")
]
