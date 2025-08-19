from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie
from .filters import MovieFilter
from user.models import Bookmark, Rating
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg
from django.core.paginator import Paginator
from .forms import MovieForm

def movie_list(request):
    movies = Movie.objects.all()
    myFilter = MovieFilter(request.GET, queryset=movies)
    movies = myFilter.qs

    user = request.user
    bookmarks = Bookmark.objects.filter(user=user).values_list("movie_id", flat=True)

    paginator = Paginator(movies, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "movies.html",
        {
            "movies": movies,
            "filter": myFilter,
            "bookmarks": bookmarks,
            "page_obj": page_obj,
        },
    )


def movie_info(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    bookmarks = Bookmark.objects.filter(movie=movie)
    ratings = Rating.objects.filter(movie=movie)
    avg_rating = ratings.aggregate(Avg("rating"))["rating__avg"]
    if avg_rating is not None:
        avg_rating = round(avg_rating, 2)
    else:
        avg_rating = 0

    user_rating = Rating.objects.filter(user=request.user, movie=movie).first()
    star_range = range(5)
    return render(
        request,
        "movie_info.html",
        {
            "movie": movie,
            "bookmarks": bookmarks,
            "ratings": ratings,
            "avg_rating": avg_rating,
            "star_range": star_range,
            "user_rating": user_rating,
        },
    )

def is_movie_editor(user):
    return user.groups.filter(name="MovieEditor").exists()

@user_passes_test(is_movie_editor)
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies')
        
    else:
        form = MovieForm()
        return render(request, "add_movie.html", {"movie_form":form})

@login_required
def toggle_bookmark(request):
    if request.method == "POST":
        movie_id = request.POST.get("movie_id")
        action = request.POST.get("action")

        try:
            movie = Movie.objects.get(id=movie_id)
            bookmark, created = Bookmark.objects.get_or_create(
                user=request.user, movie=movie
            )

            if action == "add":
                if created:
                    return JsonResponse(
                        {"status": "added", "message": "Bookmark added."}
                    )
                else:
                    return JsonResponse(
                        {"status": "exists", "message": "Already bookmarked."}
                    )
            elif action == "remove":
                bookmark.delete()
                return JsonResponse(
                    {"status": "removed", "message": "Bookmark removed."}
                )
        except Movie.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Movie not found."})

    return JsonResponse({"status": "invalid", "message": "Invalid request."})


@login_required
def submit_movie_rating(request):
    movie_id = request.POST.get("movie_id")
    rating_value = request.POST.get("rating")

    movie = Movie.objects.get(id=movie_id)

    Rating.objects.update_or_create(
        user=request.user, movie=movie, defaults={"rating": rating_value}
    )
    print(movie_id)
    print(rating_value)

    return JsonResponse({"success": True})
