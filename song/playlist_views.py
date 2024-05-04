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
