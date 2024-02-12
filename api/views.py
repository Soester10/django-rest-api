from django.shortcuts import render
from django.core.cache import cache

# Create your views here.

from rest_framework import permissions, status
from .validations import custom_validation, validate_username, validate_password


from django.contrib.auth import get_user_model, login, logout
from rest_framework.authentication import SessionAuthentication

from rest_framework.views import APIView

from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserLoginSerializer, DataSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from .models import DataModel
from rest_framework import generics, filters


class UserRegister(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        clean_data = custom_validation(request.data)
        serializer = UserRegisterSerializer(data=clean_data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            user.set_password(clean_data["password"])
            user.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_username(data)
        assert validate_password(data)

        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validate(data)
            login(request, user)
            cache.delete('api_user_data')
            cache.clear()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    def post(self, request):
        logout(request)
        cache.delete('api_user_data')
        cache.clear()
        return Response(status=status.HTTP_200_OK)

class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 1000




class Data(generics.ListCreateAPIView):
    cache.delete('api_user_data')
    cache.clear()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    
    serializer_class = DataSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'SKU', 'stock_status', 'available_stock']
    ordering_fields = ['SKU', 'name']
    search_fields = ['SKU', 'name']

    def get_queryset(self):
        cache_key_user = 'api_user_data'
        cached_data = cache.get(cache_key_user)
        if not cached_data:
            user_data = DataModel.objects.filter(user=self.request.user)
            cache.set(cache_key_user, user_data, timeout=60 * 5)
        else:
            user_data = cached_data

        
        return DataModel.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        cache.delete('api_user_data')
        cache.clear()
        serializer.save(user=self.request.user)
        cache_key_user = 'api_user_data'
        user_data = DataModel.objects.filter(user=self.request.user)
        cache.set(cache_key_user, user_data, timeout=60 * 5)

    def post(self, request, *args, **kwargs):
        cache.delete('api_user_data')
        cache.clear()
        return self.create(request, *args, **kwargs)
        
    


