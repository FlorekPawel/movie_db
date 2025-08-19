from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime as dt
from django.db.models import Avg


class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True)
    release_year = models.IntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(dt.now().year)]
    )

    GENRE_CHOICES = [
        ("ACTION", "Action"),
        ("COMEDY", "Comedy"),
        ("DRAMA", "Drama"),
        ("FANTASY", "Fantasy"),
        ("HORROR", "Horror"),
        ("SCI_FI", "Science Fiction"),
        ("ROMANCE", "Romance"),
        ("THRILLER", "Thriller"),
        ("DOCUMENTARY", "Documentary"),
        ("ANIMATION", "Animation"),
        ("OTHER", "Other"),
    ]

    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    duration = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    director = models.CharField(max_length=100, null=True, default="Unknown")
    average_rating = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        managed = True

    def update_average_rating(self):
        average = self.rated_by.aggregate(Avg("rating"))["rating__avg"]
        self.average_rating = round(average, 2) if average else 0
        self.save()

    def __str__(self) -> str:
        return self.title
