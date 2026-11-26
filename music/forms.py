from django import forms
from .models import Release, Track


class ReleaseForm(forms.ModelForm):

    class Meta:
        model = Release

        fields = [
            'title',
            'release_type',
            'genre',
            'release_date',
            'artwork',
        ]

        widgets = {
            'release_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }


class TrackForm(forms.ModelForm):

    class Meta:
        model = Track

        fields = [
            'track_title',
            'featured_artists',
            'producer',
            'track_number',
            'audio_file',
        ]
