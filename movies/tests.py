from django.test import TestCase
from .models import Movie
from django.core.exceptions import ValidationError
from datetime import datetime as dt
from django.contrib.auth import get_user_model
from user.models import Rating, Bookmark
from django.urls import reverse
from django.contrib.auth.models import Group
from .forms import MovieForm
from .filters import MovieFilter



User = get_user_model()


class MovieModelTest(TestCase):

    def setUp(self):
        self.movie = Movie.objects.create(
            title="Inception",
            release_year=2010,
            genre="SCI_FI",
            duration=148,
            director="Christopher Nolan",
        )

    def test_movie_creation(self):
        """Test if a movie can be successfully created"""
        movie = Movie.objects.get(title="Inception")
        self.assertEqual(movie.title, "Inception")
        self.assertEqual(movie.release_year, 2010)
        self.assertEqual(movie.genre, "SCI_FI")
        self.assertEqual(movie.duration, 148)
        self.assertEqual(movie.director, "Christopher Nolan")

    def test_release_year_validation(self):
        """Test that release year must be between 1800 and current year"""
        movie = Movie(
            title="Future Movie", release_year=3000, genre="SCI_FI"
        )

        movie2 = Movie(title="Too Old Movie", release_year=1800, genre="SCI_FI")

        with self.assertRaises(ValidationError):
            movie.full_clean()
            movie2.full_clean()

    def test_genre_validation(self):
        """Test that invalid genre choices raise a ValidationError"""
        movie = Movie(
            title="Invalid Genre Movie", release_year=2000, genre="UNKNOWN_GENRE"
        )
        with self.assertRaises(ValidationError):
            movie.full_clean()

    def test_update_average_rating(self):
        """Test that the average rating is updated correctly"""
        user1 = User.objects.create_user(username="user1", password="test123")
        user2 = User.objects.create_user(username="user2", password="test123")
        Rating.objects.create(movie=self.movie, user=user1, rating=4)
        Rating.objects.create(movie=self.movie, user=user2, rating=5)

        self.movie.update_average_rating()
        self.assertEqual(self.movie.average_rating, 4.5)

    def test_default_average_rating(self):
        """Test that a new movie has a default average rating of 0"""
        new_movie = Movie.objects.create(
            title="No Ratings Yet", release_year=2022, genre="COMEDY", duration=90
        )
        self.assertEqual(new_movie.average_rating, 0)


class MovieViewsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.movie = Movie.objects.create(
            title="Inception",
            release_year=2010,
            genre="SCI_FI",
            duration=148,
            director="Christopher Nolan",
        )
        self.client.login(username="testuser", password="testpass")

    def test_movie_list_view(self):
        """Test that the movie list view works correctly."""
        response = self.client.get(reverse("movies"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movies.html")
        self.assertIn(self.movie, response.context["movies"])

    def test_movie_info_view(self):
        """Test that the movie info view returns correct movie details."""
        response = self.client.get(reverse("movie_info", args=[self.movie.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "movie_info.html")
        self.assertEqual(response.context["movie"].title, "Inception")
        self.assertEqual(response.context["avg_rating"], 0)

    def test_add_movie_view_permissions(self):
        """Test that only users in 'MovieEditor' group can access the add movie view."""
        editor_group = Group.objects.create(name="MovieEditor")
        self.user.groups.add(editor_group)

        response = self.client.get(reverse("add_movie"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add_movie.html")

        # Test with a POST request
        response = self.client.post(
            reverse("add_movie"),
            {
                "title": "Interstellar",
                "release_year": 2014,
                "genre": "SCI_FI",
                "duration": 169,
                "director": "Christopher Nolan",
            },
        )
        self.assertRedirects(response, reverse("movies"))
        self.assertTrue(Movie.objects.filter(title="Interstellar").exists())

    def test_toggle_bookmark_add(self):
        """Test adding a bookmark."""
        response = self.client.post(
            reverse("toggle_bookmark"),
            {
                "movie_id": self.movie.id,
                "action": "add",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "added")
        self.assertTrue(
            Bookmark.objects.filter(user=self.user, movie=self.movie).exists()
        )

    def test_toggle_bookmark_remove(self):
        """Test removing a bookmark."""
        Bookmark.objects.create(user=self.user, movie=self.movie)
        response = self.client.post(
            reverse("toggle_bookmark"),
            {
                "movie_id": self.movie.id,
                "action": "remove",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "removed")
        self.assertFalse(
            Bookmark.objects.filter(user=self.user, movie=self.movie).exists()
        )

    def test_submit_movie_rating(self):
        """Test that a user can submit a rating for a movie."""
        response = self.client.post(
            reverse("submit_movie_rating"),
            {
                "movie_id": self.movie.id,
                "rating": 4,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)
        self.assertTrue(
            Rating.objects.filter(user=self.user, movie=self.movie, rating=4).exists()
        )

    def test_submit_movie_rating_update(self):
        """Test that a user can update their rating."""
        Rating.objects.create(user=self.user, movie=self.movie, rating=3)
        response = self.client.post(
            reverse("submit_movie_rating"),
            {
                "movie_id": self.movie.id,
                "rating": 5,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)
        self.assertTrue(
            Rating.objects.filter(user=self.user, movie=self.movie, rating=5).exists()
        )

class MovieFormTest(TestCase):

    def test_valid_form(self):
        """Test that the form is valid with correct data."""
        form_data = {
            'title': 'Inception',
            'genre': 'SCI_FI',
            'duration': 148,
            'director': 'Christopher Nolan',
            'release_year': 2010,
        }
        form = MovieForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['title'], 'Inception')
        self.assertEqual(form.cleaned_data['genre'], 'SCI_FI')
        self.assertEqual(form.cleaned_data['duration'], 148)
        self.assertEqual(form.cleaned_data['director'], 'Christopher Nolan')
        self.assertEqual(form.cleaned_data['release_year'], 2010)

    def test_invalid_form_missing_title(self):
        """Test that the form is invalid without a title."""
        form_data = {
            'genre': 'SCI_FI',
            'duration': 148,
            'director': 'Christopher Nolan',
            'release_year': 2010,
        }
        form = MovieForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

    def test_invalid_form_invalid_release_year(self):
        """Test that the form is invalid with a release year in the future."""
        future_year = 3000
        form_data = {
            'title': 'Inception',
            'genre': 'SCI_FI',
            'duration': 148,
            'director': 'Christopher Nolan',
            'release_year': future_year,
        }
        form = MovieForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('release_year', form.errors)

    def test_invalid_form_negative_duration(self):
        """Test that the form is invalid with a negative duration."""
        form_data = {
            'title': 'Inception',
            'genre': 'SCI_FI',
            'duration': -148,
            'director': 'Christopher Nolan',
            'release_year': 2010,
        }
        form = MovieForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('duration', form.errors)

    def test_form_renders_correctly(self):
        """Test that the form renders correctly with attributes."""
        form = MovieForm()
        self.assertIn('class="form-control"', str(form['title']))
        self.assertIn('placeholder="Movie Title"', str(form['title']))
        self.assertIn('class="form-control"', str(form['genre']))
        self.assertIn('class="form-control"', str(form['duration']))
        self.assertIn('class="form-control"', str(form['director']))
        self.assertIn('class="form-control"', str(form['release_year']))
        
class MovieFilterTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Create sample data for testing."""
        cls.movie1 = Movie.objects.create(
            title="Inception",
            genre="SCI_FI",
            duration=148,
            director="Christopher Nolan",
            release_year=2010,
            average_rating=4.8,
        )
        cls.movie2 = Movie.objects.create(
            title="The Dark Knight",
            genre="ACTION",
            duration=152,
            director="Christopher Nolan",
            release_year=2008,
            average_rating=4.7,
        )
        cls.movie3 = Movie.objects.create(
            title="Interstellar",
            genre="SCI_FI",
            duration=169,
            director="Christopher Nolan",
            release_year=2014,
            average_rating=4.6,
        )

    def test_filter_by_title(self):
        """Test filtering by title."""
        filterset = MovieFilter({"title": "Inception"}, queryset=Movie.objects.all())
        self.assertEqual(len(filterset.qs), 1)
        self.assertEqual(filterset.qs.first(), self.movie1)

    def test_filter_by_genre(self):
        """Test filtering by genre."""
        filterset = MovieFilter({"genre": "ACTION"}, queryset=Movie.objects.all())
        self.assertEqual(len(filterset.qs), 1)
        self.assertEqual(filterset.qs.first(), self.movie2)

    def test_filter_by_director(self):
        """Test filtering by director."""
        filterset = MovieFilter({"director": "Christopher Nolan"}, queryset=Movie.objects.all())
        self.assertEqual(len(filterset.qs), 3)

    def test_filter_by_release_year(self):
        """Test filtering by release year."""
        filterset = MovieFilter({"year": 2010}, queryset=Movie.objects.all())
        self.assertEqual(len(filterset.qs), 1)
        self.assertEqual(filterset.qs.first(), self.movie1)

    def test_filter_by_average_rating(self):
        """Test filtering by average rating."""
        filterset = MovieFilter({"rating": 4.7}, queryset=Movie.objects.all())
        self.assertEqual(len(filterset.qs), 2)