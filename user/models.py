from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.core.validators import MinValueValidator, MaxValueValidator
from movies.models import Movie

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, related_name="bookmarked_by"
    )

    class Meta:
        unique_together = ("user", "movie")

    def __str__(self) -> str:
        return f"Bookmark for {self.movie.title} by {self.user.username}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rates")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="rated_by")
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        unique_together = ("user", "movie")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.movie.update_average_rating()

    def __str__(self) -> str:
        return f"Rating for {self.movie.title} by {self.user.username}"
