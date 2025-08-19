from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'duration', 'director', 'release_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie Title'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duration in minutes'}),
            'director': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Director Name'}),
            'release_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Release Year'}),
        }