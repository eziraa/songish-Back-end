import json
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Song
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.hashers import check_password, make_password
from django.http import JsonResponse
from django.views import View
from .models import Customer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from rest_framework import viewsets
from rest_framework import status


from song.models import *
from song.serializers.serializer import *

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Song


@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            fullName = data.get('fullName')
            password = data.get('password')
            email = data.get('email')
            gender = data.get('gender')
            if Customer.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists."}, status=400)
            customer = Customer(fullName=fullName, password=make_password(
                password), email=email, gender=gender)
            result = customer.save()
            print(CustomerSerializer(customer).data)
            return JsonResponse(CustomerSerializer(result).data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class LogIndView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            customer = Customer.objects.get(email=email)
            if check_password(password, customer.password):
                # favorite_songs_i = [
                #     song.id for song in customer.favorite_songs]
                # my__songs_i = [
                #     song.id for song in customer.favorite_songs]
                serializer = CustomerSerializer(customer)
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse({"error": "Password is incorrect."}, status=400)
        except ObjectDoesNotExist:
            print("object does not exist")
            return JsonResponse({"error": "User does not exist not found."}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AddSongView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            customer_id = data.get('user_id')
            song_data = {k: v for k, v in data.items() if k != 'user_id'}
            customer = Customer.objects.get(id=customer_id)
            song = Song.objects.create(customer=customer, **song_data)
            serializer = SongSerializer(song)
            return JsonResponse(serializer.data, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Song not found."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)


class GetSongsView(View):
    def get(self, request, *args, **kwargs):
        try:
            songs = Song.objects.all()
            serializer = SongSerializer(songs, many=True)
            return JsonResponse(serializer.data, safe=False)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Songs not found."}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def song_detail(request):
    try:
        request.data['duration'] = int(float(request.data['duration']))
        song = Song.objects.get(pk=request.data['id'])
    except Song.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = SongSerializer(song)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SongSerializer(song, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        song.delete()
        return Response(status=204)


@api_view(['POST'])
def add_song_to_favorite(request, user_id, song_id):
    try:
        print(user_id, song_id)
        customer = Customer.objects.get(id=user_id)
        song = Song.objects.get(id=song_id)
        customer.favorite_songs.add(song)
        customer.save()
        return JsonResponse(SongSerializer(song).data, status=status.HTTP_200_OK)
    except Customer.DoesNotExist:

        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
    except Song.DoesNotExist:
        return Response({"error": "Song not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_your_favorite_songs(request, user_id):
    user = get_object_or_404(Customer, id=user_id)
    serializer = SongSerializer(user.favorite_songs, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['DELETE'])
def remove_song_from_favorite(request, user_id, song_id):
    customer = get_object_or_404(Customer, id=user_id)
    song = get_object_or_404(Song, id=song_id)
    customer.favorite_songs.remove(song)
    customer.save()
    return JsonResponse(SongSerializer(song).data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_my_songs(request, user_id):
    user = get_object_or_404(Customer, id=user_id)
    songs = user.songs
    serializer = SongSerializer(songs, many=True)
    return JsonResponse(serializer.data, safe=False)
