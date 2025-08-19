from django.test import TestCase
from django.urls import reverse, resolve
from movies.models import Movie
from user.models import Rating
from django.contrib.auth.models import User
from .views import home

class HomeViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="testpass123")
        self.user2 = User.objects.create_user(username="user2", password="testpass123")

        self.movie1 = Movie.objects.create(title="Movie 1", genre="Action", duration=120, director="Director 1", release_year=2020)
        self.movie2 = Movie.objects.create(title="Movie 2", genre="Drama", duration=90, director="Director 2", release_year=2021)
        self.movie3 = Movie.objects.create(title="Movie 3", genre="Comedy", duration=110, director="Director 3", release_year=2019)
        self.movie4 = Movie.objects.create(title="Movie 4", genre="Action", duration=140, director="Director 4", release_year=2022)
        self.movie5 = Movie.objects.create(title="Movie 5", genre="Horror", duration=95, director="Director 5", release_year=2018)
        self.movie6 = Movie.objects.create(title="Movie 6", genre="Sci-Fi", duration=100, director="Director 6", release_year=2022)

        Rating.objects.create(user=self.user1, movie=self.movie1, rating=5)
        Rating.objects.create(user=self.user2, movie=self.movie1, rating=4)
        Rating.objects.create(user=self.user1, movie=self.movie2, rating=3)
        Rating.objects.create(user=self.user2, movie=self.movie2, rating=2)
        Rating.objects.create(user=self.user1, movie=self.movie3, rating=4.5)
        Rating.objects.create(user=self.user2, movie=self.movie3, rating=5)
        Rating.objects.create(user=self.user1, movie=self.movie4, rating=1)
        Rating.objects.create(user=self.user2, movie=self.movie4, rating=1.5)
        Rating.objects.create(user=self.user1, movie=self.movie5, rating=3)
        Rating.objects.create(user=self.user2, movie=self.movie5, rating=4)
        Rating.objects.create(user=self.user1, movie=self.movie6, rating=2)
        Rating.objects.create(user=self.user2, movie=self.movie6, rating=3.5)

    def test_home_view(self):
        '''Test the top movies panel'''
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

        top_movies = response.context["top_movies"]
        self.assertEqual(len(top_movies), 5)

        top_movie_titles = [movie.title for movie in top_movies]
        self.assertEqual(top_movie_titles[0], "Movie 3")
        self.assertIn("Movie 1", top_movie_titles)
        self.assertNotIn("Movie 4", top_movie_titles)
        
class URLTests(TestCase):

    def test_home_url_resolves_to_home_view(self):
        url = reverse('home')
        self.assertEqual(url, '/')

        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func, home)