
from django.urls import path
from . import views

urlpatterns = [

    path(
        'releases/',
        views.release_list,
        name='release_list'
    ),

    path(
        'upload/',
        views.upload_release,
        name='upload_release'
    ),

    path(
        'release/<int:pk>/',
        views.release_detail,
        name='release_detail'
    ),

    path(
        'release/<int:pk>/add-track/',
        views.add_track,
        name='add_track'
    ),

    path(
        'release/<int:pk>/submit/',
        views.submit_release,
        name='submit_release'
    ),

]
