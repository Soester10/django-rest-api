from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics, filters
from rest_framework.exceptions import AuthenticationFailed

from django_filters.rest_framework import DjangoFilterBackend

from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings

from .validations import custom_validation, validate_username, validate_password
from .serializers import UserRegisterSerializer, UserLoginSerializer, DataSerializer
from .models import DataModel, Custom_User
from .utils import generate_access_token

import jwt


# register user
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
    # authentication_classes = (SessionAuthentication,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_username(data)
        assert validate_password(data)

        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validate(data)
            # generate jwt for signing in users
            user_access_token = generate_access_token(user)
            response = Response()
            # store jwt in cookie
            response.set_cookie(key="access_token", value=user_access_token)
            response.data = {"access_token": user_access_token}
            # clear caches to fetch new user's data
            cache.delete("api_user_data")
            cache.clear()
            return response

            ##session ID
            # user = serializer.validate(data)
            # login(request, user)
            # cache.delete("api_user_data")
            # cache.clear()
            # return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    permission_classes = (permissions.AllowAny,)
    # authentication_classes = (SessionAuthentication,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        user_token = request.COOKIES.get("access_token", None)
        if user_token:
            response = Response()
            # delete jwt cookie
            response.delete_cookie("access_token")
            response.data = {"message": "Logged out successfully."}
            # clear caches to clear logged out user's data
            cache.delete("api_user_data")
            cache.clear()
            return response

        response = Response()
        response.data = {"message": "User is already logged out."}
        return response

        ##session ID
        # logout(request)
        # cache.delete("api_user_data")
        # cache.clear()
        # return Response(status=status.HTTP_200_OK)


class CustomPagination(PageNumberPagination):
    page_size = 3  # currently set at 3 data per page
    page_size_query_param = "page_size"
    max_page_size = 1000


##With session ID
# class Data(generics.ListCreateAPIView):
#     cache.delete("api_user_data")
#     cache.clear()
#     permission_classes = (permissions.IsAuthenticated,)
#     authentication_classes = (SessionAuthentication,)

#     serializer_class = DataSerializer
#     pagination_class = CustomPagination
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.OrderingFilter,
#         filters.SearchFilter,
#     ]
#     filterset_fields = ["category", "SKU", "stock_status", "available_stock"]
#     ordering_fields = ["SKU", "name"]
#     search_fields = ["SKU", "name"]

#     def get_queryset(self):
#         cache_key_user = "api_user_data"
#         cached_data = cache.get(cache_key_user)
#         if not cached_data:
#             user_data = DataModel.objects.filter(user=self.request.user)
#             cache.set(cache_key_user, user_data, timeout=60 * 5)
#         else:
#             user_data = cached_data

#         return user_data

#     def perform_create(self, serializer):
#         cache.delete("api_user_data")
#         cache.clear()
#         serializer.save(user=self.request.user)
#         cache_key_user = "api_user_data"
#         user_data = DataModel.objects.filter(user=self.request.user)
#         cache.set(cache_key_user, user_data, timeout=60 * 5)

#     def post(self, request, *args, **kwargs):
#         cache.delete("api_user_data")
#         cache.clear()
#         return self.create(request, *args, **kwargs)


##With JWT
class Data(generics.ListCreateAPIView):
    # clear cache on first atempt
    cache.delete("api_user_data")
    cache.clear()
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    serializer_class = DataSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = ["category", "SKU", "stock_status", "available_stock", "name"]
    ordering_fields = ["SKU", "name"]
    search_fields = ["SKU", "name"]

    def get_queryset(self):
        # check for jwt in cookies
        user_token = self.request.COOKIES.get("access_token")
        if not user_token:
            raise AuthenticationFailed("Unauthenticated user!")

        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        user = Custom_User.objects.filter(id=payload["id"]).first()

        # if cached use that, otherwise fetch from db and save it in cache
        cache_key_user = "api_user_data"
        cached_data = cache.get(cache_key_user)
        if not cached_data:
            user_data = DataModel.objects.filter(user=user)
            cache.set(cache_key_user, user_data, timeout=60 * 5)
        else:
            user_data = cached_data

        return user_data

    def perform_create(self, serializer):
        # check for jwt in cookies
        user_token = self.request.COOKIES.get("access_token")
        if not user_token:
            raise AuthenticationFailed("Unauthenticated user!")

        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=["HS256"])
        user = Custom_User.objects.filter(id=payload["id"]).first()
        serializer.save(user=user)

        # clear cache when new data is added to fetch from db on next GET
        cache.delete("api_user_data")
        cache.clear()

        # fetch from db and add to cache
        cache_key_user = "api_user_data"
        user_data = DataModel.objects.filter(user=user)
        cache.set(cache_key_user, user_data, timeout=60 * 5)

    def post(self, request, *args, **kwargs):
        # clear cache when new data is added to fetch from db on next GET
        cache.delete("api_user_data")
        cache.clear()
        return self.create(request, *args, **kwargs)
