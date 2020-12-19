from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>", views.entry, name ="entry"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new"),
    path("save",views.save_entry,name="save"),
    path("random",views.random_entry,name="random"),
    path("edit/<str:title>", views.editPage, name="editPage")

]
