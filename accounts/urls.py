from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # ARTIST ACCOUNT URLS
    path('register/', views.register, name='register'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    path('dashboard/', views.dashboard, name='dashboard'),

    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),

    # ADMINISTRATOR URLS
    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'admin-artists/',
        views.admin_artists,
        name='admin_artists'
    ),

    path(
        'admin-releases/',
        views.admin_releases,
        name='admin_releases'
    ),

    path(
        'admin-release/<int:pk>/',
        views.review_release,
        name='review_release'
    ),

    path(
        'admin-release/<int:pk>/update/',
        views.update_release_status,
        name='update_release_status'
    ),

]
