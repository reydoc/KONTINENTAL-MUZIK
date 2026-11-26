from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Release, Track
from .forms import ReleaseForm, TrackForm


@login_required
def release_list(request):

    releases = Release.objects.filter(
        artist=request.user.artist_profile
    ).order_by('-created_at')

    return render(
        request,
        'music/release_list.html',
        {'releases': releases}
    )


@login_required
def upload_release(request):

    if request.method == 'POST':

        form = ReleaseForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            release = form.save(commit=False)

            release.artist = request.user.artist_profile

            release.save()

            messages.success(
                request,
                'Your release has been uploaded successfully.'
            )

            return redirect(
                'release_detail',
                pk=release.pk
            )

    else:
        form = ReleaseForm()

    return render(
        request,
        'music/upload_release.html',
        {'form': form}
    )


@login_required
def release_detail(request, pk):

    release = get_object_or_404(
        Release,
        pk=pk,
        artist=request.user.artist_profile
    )

    tracks = release.tracks.all()

    return render(
        request,
        'music/release_detail.html',
        {
            'release': release,
            'tracks': tracks
        }
    )


@login_required
def add_track(request, pk):

    release = get_object_or_404(
        Release,
        pk=pk,
        artist=request.user.artist_profile
    )

    if release.status != 'Draft':
        messages.error(
            request,
            'Tracks cannot be changed after submission.'
        )
        return redirect(
            'release_detail',
            pk=release.pk
        )

    if request.method == 'POST':

        form = TrackForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            track = form.save(commit=False)
            track.release = release
            track.save()

            messages.success(
                request,
                'Track added successfully.'
            )

            return redirect(
                'release_detail',
                pk=release.pk
            )

    else:
        form = TrackForm()

    return render(
        request,
        'music/add_track.html',
        {
            'form': form,
            'release': release
        }
    )


@login_required
def submit_release(request, pk):

    if request.method != 'POST':
        return redirect('release_list')

    release = get_object_or_404(
        Release,
        pk=pk,
        artist=request.user.artist_profile
    )

    if release.status != 'Draft':
        messages.error(
            request,
            'This release has already been submitted.'
        )
        return redirect(
            'release_detail',
            pk=release.pk
        )

    if not release.tracks.exists():
        messages.error(
            request,
            'Please add at least one track before submitting.'
        )

        return redirect(
            'release_detail',
            pk=release.pk
        )

    if release.release_type == 'Single' and release.tracks.count() != 1:
        messages.error(
            request,
            'A single must contain exactly one track.'
        )

        return redirect(
            'release_detail',
            pk=release.pk
        )

    release.status = 'Pending Review'
    release.save(update_fields=['status'])

    messages.success(
        request,
        'Your music has been submitted for review.'
    )

    return redirect(
        'release_detail',
        pk=release.pk
    )
