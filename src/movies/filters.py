from django_filters import CharFilter, FilterSet, ChoiceFilter, NumberFilter
from django.forms.widgets import TextInput, NumberInput, Select
from .models import Movie


class MovieFilter(FilterSet):
    title = CharFilter(
        field_name="title",
        lookup_expr="icontains",
        widget=TextInput(attrs={"class": "form-control", "placeholder": "Title"}),
    )

    genre = ChoiceFilter(
        choices=Movie.GENRE_CHOICES,
        field_name="genre",
        widget=Select(
            attrs={"class": "form-control", "placeholder": "Genre"}
        ),
    )

    director = CharFilter(
        field_name="director",
        lookup_expr="icontains",
        widget=TextInput(attrs={"class": "form-control", "placeholder": "Director"}),
    )

    year = NumberFilter(
        field_name="release_year",
        widget=NumberInput(
            attrs={"class": "form-control", "placeholder": "Year: 1900-now"}
        ),
    )

    rating = NumberFilter(
        field_name="average_rating",
        lookup_expr="gte",
        widget=NumberInput(
            attrs={"class": "form-control", "placeholder": "Min. rating: 0.0-5.0"}
        ),
    )

    class Meta:
        model = Movie
        fields = []
