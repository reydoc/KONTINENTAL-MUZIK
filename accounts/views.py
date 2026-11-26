from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from .forms import ArtistRegistrationForm
from .models import ArtistProfile
from music.models import Release


User = get_user_model()


# ==========================================
# ARTIST REGISTRATION
# ==========================================

def register(request):

    if request.method == 'POST':

        form = ArtistRegistrationForm(request.POST)

        if form.is_valid():

            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )

            ArtistProfile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                artist_name=form.cleaned_data['artist_name']
            )

            login(request, user)

            messages.success(
                request,
                'Welcome to Wave-Distro! Your account has been created.'
            )

            return redirect('dashboard')

    else:
        form = ArtistRegistrationForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )


# ==========================================
# ARTIST AND ADMINISTRATOR DASHBOARD
# ==========================================

@login_required
def dashboard(request):

    # Administrators should use the administrator dashboard
    if request.user.is_staff:
        return redirect('admin_dashboard')

    # Check whether the logged-in user has an artist profile
    if not hasattr(request.user, 'artist_profile'):

        messages.error(
            request,
            'Your artist profile could not be found. Please contact support.'
        )

        return redirect('home')

    # Retrieve the artist profile
    profile = request.user.artist_profile

    return render(
        request,
        'accounts/dashboard.html',
        {'profile': profile}
    )


# ==========================================
# ADMINISTRATOR DASHBOARD
# ==========================================

@staff_member_required
def admin_dashboard(request):

    total_artists = ArtistProfile.objects.count()

    total_releases = Release.objects.count()

    pending_releases = Release.objects.filter(
        status='Pending Review'
    ).count()

    approved_releases = Release.objects.filter(
        status='Approved'
    ).count()

    rejected_releases = Release.objects.filter(
        status='Rejected'
    ).count()

    recent_releases = Release.objects.select_related(
        'artist'
    ).order_by('-created_at')[:5]

    context = {
        'total_artists': total_artists,
        'total_releases': total_releases,
        'pending_releases': pending_releases,
        'approved_releases': approved_releases,
        'rejected_releases': rejected_releases,
        'recent_releases': recent_releases,
    }

    return render(
        request,
        'accounts/admin_dashboard.html',
        context
    )


# ==========================================
# MANAGE REGISTERED ARTISTS
# ==========================================

@staff_member_required
def admin_artists(request):

    artists = ArtistProfile.objects.select_related(
        'user'
    ).order_by('-created_at')

    return render(
        request,
        'accounts/admin_artists.html',
        {'artists': artists}
    )


# ==========================================
# MANAGE ALL MUSIC RELEASES
# ==========================================

@staff_member_required
def admin_releases(request):

    releases = Release.objects.select_related(
        'artist',
        'artist__user'
    ).order_by('-created_at')

    return render(
        request,
        'accounts/admin_releases.html',
        {'releases': releases}
    )


# ==========================================
# REVIEW A MUSIC RELEASE
# ==========================================

@staff_member_required
def review_release(request, pk):

    release = get_object_or_404(
        Release,
        pk=pk
    )

    tracks = release.tracks.all()

    return render(
        request,
        'accounts/review_release.html',
        {
            'release': release,
            'tracks': tracks
        }
    )


# ==========================================
# APPROVE OR REJECT A MUSIC RELEASE
# ==========================================

@staff_member_required
def update_release_status(request, pk):

    if request.method != 'POST':
        return redirect('admin_releases')

    release = get_object_or_404(
        Release,
        pk=pk
    )

    action = request.POST.get('action')

    if release.status != 'Pending Review':

        messages.error(
            request,
            'Only releases awaiting review can be updated.'
        )

        return redirect(
            'review_release',
            pk=release.pk
        )

    if action == 'approve':

        release.status = 'Approved'

        messages.success(
            request,
            'The release has been approved successfully.'
        )

    elif action == 'reject':

        release.status = 'Rejected'

        messages.success(
            request,
            'The release has been rejected.'
        )

    else:

        messages.error(
            request,
            'Invalid review action.'
        )

        return redirect(
            'review_release',
            pk=release.pk
        )

    release.save(update_fields=['status'])

    return redirect(
        'review_release',
        pk=release.pk
    )
