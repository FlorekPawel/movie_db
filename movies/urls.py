from django.urls import path
from . import views

urlpatterns = [
    path("", views.movie_list, name="movies"),
    path("toggle-bookmark/", views.toggle_bookmark, name="toggle_bookmark"),
    path("movie/<int:pk>/", views.movie_info, name="movie_info"),
    path("submit_movie_rating", views.submit_movie_rating, name="submit_movie_rating"),
    path("add_movie", views.add_movie, name="add_movie")
]
