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
