import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import Playlist, Song
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers.serializer import PlaylistSerializer, SongSerializer
from rest_framework import status
from rest_framework.response import Response


from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Playlist, Customer


@api_view(["DELETE"])
def delete_playlist(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        playlist.delete()
        return JsonResponse({'message': 'Playlist deleted successfully'}, status=200)
    except Playlist.DoesNotExist:
        return JsonResponse({'error': 'Playlist not found'}, status=404)


@api_view(['POST'])
def create_playlist(request):
    # data = json.loads(request.body)
    customer = Customer.objects.get(id=request.data['customer_id'])
    playlist_data = {k: v for k, v in request.data.items()
                     if k != 'customer_id'}
    playlist = Playlist.objects.create(customer=customer, **playlist_data)
    serializer = PlaylistSerializer(playlist)
    return JsonResponse(serializer.data, status=201)


@api_view(['GET'])
def getPlaylists(request, user_id):
    playlists = Playlist.objects.filter(customer_id=user_id)
    serializer = PlaylistSerializer(playlists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_song_in_playlist(request):

    playlist = get_object_or_404(Playlist, id=request.data["playlist_id"])
    song_list = playlist.song.all()

    # Create a Paginator object
    paginator = Paginator(song_list, 10)  # Show 10 song items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert the Page object to a list so it can be serialized to JSON
    song_list = list(page_obj.object_list.values())

    return JsonResponse({
        'song': song_list,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'number': page_obj.number,
        'num_pages': paginator.num_pages,
    })


@api_view(['POST'])
def add_song_to_playlist(request, playlist_id, song_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id)
        song = Song.objects.get(id=song_id)
        playlist.song.add(song)
        playlist.save()
        return Response({"message": "Song added to playlist successfully", "data": SongSerializer(song).data}, status=status.HTTP_200_OK)
    except Playlist.DoesNotExist:

        return Response({"error": "Playlist not found"}, status=status.HTTP_404_NOT_FOUND)
    except Song.DoesNotExist:
        return Response({"error": "Song not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
def remove_song_from_playlist(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    song = get_object_or_404(Song, id=song_id)
    playlist.song.remove(song)
    playlist.save()
    return JsonResponse(SongSerializer(song).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_song_in_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    serializer = SongSerializer(playlist.song, many=True)
    return JsonResponse(serializer.data, safe=False)


class DeletePlaylistView(View):
    def delete(self, request, playlist_id):
        try:
            playlist = Playlist.objects.get(id=playlist_id)
            playlist.delete()
            return JsonResponse({'message': 'Playlist deleted successfully'}, status=200)
        except Playlist.DoesNotExist:
            return JsonResponse({'error': 'Playlist not found'}, status=404)
