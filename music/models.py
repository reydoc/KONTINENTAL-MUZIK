from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


def validate_audio_size(file):
    if file.size > 100 * 1024 * 1024:
        raise ValidationError(
            "Audio file cannot exceed 100MB."
        )


def validate_artwork_size(file):
    if file.size > 5 * 1024 * 1024:
        raise ValidationError(
            "Artwork cannot exceed 5MB."
        )


class Release(models.Model):

    RELEASE_TYPES = [
        ('Single', 'Single'),
        ('EP', 'EP'),
        ('Album', 'Album'),
    ]

    STATUS_CHOICES = [
        ('Draft', 'Draft'),
        ('Pending Review', 'Pending Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    artist = models.ForeignKey(
        'accounts.ArtistProfile',
        on_delete=models.CASCADE,
        related_name='releases'
    )

    title = models.CharField(max_length=200)

    release_type = models.CharField(
        max_length=20,
        choices=RELEASE_TYPES
    )

    genre = models.CharField(max_length=100)

    release_date = models.DateField()

    artwork = models.FileField(
        upload_to='artwork/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png']
            ),
            validate_artwork_size
        ]
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Draft'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Track(models.Model):

    release = models.ForeignKey(
        Release,
        on_delete=models.CASCADE,
        related_name='tracks'
    )

    track_title = models.CharField(max_length=200)

    featured_artists = models.CharField(
        max_length=250,
        blank=True
    )

    producer = models.CharField(
        max_length=150,
        blank=True
    )

    track_number = models.PositiveIntegerField()

    audio_file = models.FileField(
        upload_to='music/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['mp3', 'wav']
            ),
            validate_audio_size
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['track_number']
        constraints = [
            models.UniqueConstraint(
                fields=['release', 'track_number'],
                name='unique_track_number_per_release'
            )
        ]

    def __str__(self):
        return self.track_title
