from django.db import models
from django.conf import settings


class ArtistProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='artist_profile'
    )

    full_name = models.CharField(max_length=150)

    artist_name = models.CharField(max_length=150)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.artist_name
