from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.db.models import Count
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView

from ads.models import Category
from bulletin_board import settings
from users.models import User, Location
import json

from users.serializers import UserDetailSerializer, UserListSerializer, UserCreateSerializer


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

    def post(self, request, *args, **kwargs):
        user = UserCreateSerializer(data=json.loads(request.body))

        if user.is_valid():
            user.save()
        else:
            return JsonResponse(user.errors)

        return JsonResponse(user.data)


class UserUpdateView(UpdateView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
