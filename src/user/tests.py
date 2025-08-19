from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Bookmark, Rating
from movies.models import Movie


class AuthViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass")

    def test_login_user_success(self):
        """Test logging in with correct credentials."""
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpass"}
        )
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_login_user_wrong_credentials(self):
        """Test logging in with wrong credentials."""
        response = self.client.post(
            reverse("login"), {"username": "wrong", "password": "wrongpass"}
        )
        self.assertRedirects(response, reverse("login"))

    def test_logout_user(self):
        """Test logging out a user."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("home"))

    def test_register_user(self):
        """Test user registration."""
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "newpass123",
                "password2": "newpass123",
            },
        )
        self.assertRedirects(response, reverse("home"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_profile_view(self):
        """Test the profile view."""
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profile.html")

    def test_password_reset(self):
        """Test password reset functionality."""
        response = self.client.post(
            reverse("password_reset"), {"email": "testuser@example.com"}
        )
        self.assertRedirects(response, reverse("home"))


class BookmarkRatingTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="password123")

        cls.movie = Movie.objects.create(
            title="Test Movie",
            genre="Action",
            duration=120,
            director="Test Director",
            release_year=2023,
        )

    def test_create_bookmark(self):
        """Test creating a bookmark"""
        bookmark = Bookmark.objects.create(user=self.user, movie=self.movie)
        self.assertEqual(bookmark.user, self.user)
        self.assertEqual(bookmark.movie, self.movie)

        self.assertEqual(
            str(bookmark), f"Bookmark for {self.movie.title} by {self.user.username}"
        )

    def test_create_duplicate_bookmark(self):
        """Test duplicate bookmark"""
        Bookmark.objects.create(user=self.user, movie=self.movie)
        with self.assertRaises(Exception):
            Bookmark.objects.create(user=self.user, movie=self.movie)

    def test_create_rating(self):
        """Test creating a rating"""
        rating = Rating.objects.create(user=self.user, movie=self.movie, rating=4.5)
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.movie, self.movie)
        self.assertEqual(rating.rating, 4.5)

        self.assertEqual(
            str(rating), f"Rating for {self.movie.title} by {self.user.username}"
        )

    def test_create_duplicate_rating(self):
        """Test duplicate rating"""
        Rating.objects.create(user=self.user, movie=self.movie, rating=4.5)
        with self.assertRaises(Exception):
            Rating.objects.create(user=self.user, movie=self.movie, rating=3.0)
            