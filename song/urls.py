from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .playlist_views import *
router = DefaultRouter()
router.register(r'songs', SongViewSet)

urlpatterns = [
    path('songs/songs/', views.GetSongsView.as_view()),
    path('songs/get-songs/', views.GetPlayListSongsView.as_view()),
    path('songs/add', views.AddSongView.as_view()),
    path('single-song/', views.song_detail),
    path('songs/<int:song_id>', views.delete_song, name='delete_song'),
    path('songs/delete/', views.DeleteSongView.as_view()),
    path('user/register', views.SignUpView.as_view()),
    path('user/login', views.LogIndView.as_view()),
    path('songs/', views.song_create),
    path('get-songs/', views.song_list),
    path('playlist/playlists/', create_playlist, name='create_playlist'),
    path('playlist/<int:user_id>/my_playlists/',
         getPlaylists, name='get_my_playlists'),
    path('playlist/<int:playlist_id>/songs/',
         get_song_in_playlist, name='get_songs'),
    path('playlist/<int:playlist_id>/add_song/<int:song_id>',
         add_song_to_playlist, name='add_song'),
    path('playlist/<int:playlist_id>/remove_song/<int:song_id>',
         remove_song_from_playlist, name='remove_song'),
    path('playlist/<int:playlist_id>', delete_playlist, name='delete_playlist'),





]
