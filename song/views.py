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