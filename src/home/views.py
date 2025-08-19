from django.shortcuts import render
from movies.models import Movie
from django.db.models import Avg

def home(request):
    top_movies = (
        Movie.objects.annotate(avg_rating=Avg("rated_by__rating"))
        .order_by("-average_rating")[:5]
    )
    
    return render(request, "home.html", {"top_movies": top_movies})