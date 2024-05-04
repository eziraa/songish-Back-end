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



@api_view(['POST'])
def create_playlist(request):
    # data = json.loads(request.body)
    customer = Customer.objects.get(id=request.data['customer_id'])
    playlist_data = {k: v for k, v in request.data.items()
                     if k != 'customer_id'}
    playlist = Playlist.objects.create(customer=customer, **playlist_data)
    serializer = PlaylistSerializer(playlist)
    return JsonResponse(serializer.data, status=201)


@api_view(["DELETE"])
def delete_playlist(request, playlist_id):
    try:

        playlist = Playlist.objects.get(id=playlist_id)
        playlist.delete()

        return JsonResponse({'message': 'Playlist deleted successfully'}, status=200)
    except Playlist.DoesNotExist:
        return JsonResponse({'error': 'Playlist not found'}, status=404)


@api_view(['GET'])
def getPlaylists(request, user_id):
    playlists = Playlist.objects.filter(customer_id=user_id)
    serializer = PlaylistSerializer(playlists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def get_song_in_playlist(request):

    playlist = get_object_or_404(Playlist, id=request.data["playlist_id"])
    song_list = playlist.song.all()

    paginator = Paginator(song_list, 10)  # Show 10 song items per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    song_list = list(page_obj.object_list.values())

    return JsonResponse({
        'song': song_list,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'number': page_obj.number,
        'num_pages': paginator.num_pages,
    })
