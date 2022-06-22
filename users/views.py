from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from ads.models import Category
from bulletin_board import settings
from users.models import User, Location
import json


class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        search_text = request.GET.get('search_text', None)
        if search_text:
            self.object_list = self.object_list.filter(text=search_text)

        paginator = Paginator(self.object_list, settings.TOTAL_0N_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append({
                'id': ad.id,
                'name': ad.name,
                'author': ad.author,
                'price': ad.price,
                'description': ad.description,
                'address': ad.address,
            })

        response = {
            'items': ads,
            'num_page': paginator.num_pages,
            'total': paginator.count
        }
        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        ads = self.get_object()

        return JsonResponse({
            "id": ads.id,
            "name": ads.name,
            "author": ads.author,
            "price": ads.price,
            "description": ads.description,
            "address": ads.address,
            "is_published": ads.is_published,
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ['name', 'author_id', 'price', 'description', 'address', 'is_published', 'image', 'category_id']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        author_id = get_object_or_404(User, data["author_id"])
        category_id = get_object_or_404(Category, data["category_id"])

        ads = User.objects.create(
            name=data["name"],
            author_id=author_id,
            price=data["price"],
            description=data["description"],
            address=data["address"],
            is_published=data["is_published"],
            image=data["image"],
            category_id=category_id,
        )

        return JsonResponse({
            "id": ads.id,
            "name": ads.name,
            "author_id": ads.author_id,
            "price": ads.price,
            "description": ads.description,
            "address": ads.address,
            "is_published": ads.is_published,
            "image": ads.image,
            "category_id": ads.category_id,
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ['name', 'author_id', 'price', 'description', 'address', 'is_published', 'image', 'category_id']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        self.objects.name = data["name"]
        self.object.author_id = get_object_or_404(User, data["author_id"])
        self.objects.price = data["price"]
        self.objects.description = data["description"]
        self.objects.address = data["address"]
        self.objects.is_published = data["is_published"]
        self.objects.image = data["image"]
        self.object.category_id = get_object_or_404(Category, data["category_id"])

        self.object.save()

        return JsonResponse({
            "id": self.objects.id,
            "name": self.objects.name,
            "author_id": self.objects.author_id,
            "price": self.objects.price,
            "description": self.objects.description,
            "address": self.objects.address,
            "is_published": self.objects.is_published,
            "image": self.objects.image,
            "category_id": self.objects.category_id,
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
