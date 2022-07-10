import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ads
from bulletin_board import settings
from users.models import User


def index(request):
    return JsonResponse({
        "status": "ok 200"
    })


@method_decorator(csrf_exempt, name='dispatch')
class AdsListView(ListView):
    model = Ads
    queryset = Ads.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('-price')

        paginator = Paginator(self.object_list, settings.TOTAL_0N_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        ads = []
        for ad in page_obj:
            ads.append({
                "id": ad.id,
                "name": ad.name,
                "price": ad.price,
                "description": ad.description,
                "author_id": ad.author_id,
                "is_published": ad.is_published,
                "image": ad.image.url if ad.image else None,
            })

        response = {
            'items': ads,
            'num_page': paginator.num_pages,
            'total': paginator.count
        }
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        ads = self.get_object()

        return JsonResponse({
            "id": ads.id,
            "name": ads.name,
            "author": ads.author_id,
            "price": ads.price,
            "description": ads.description,
            "is_published": ads.is_published,
            "image": ads.image.url if ads.image else None,
            "category": ads.category_id,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published', 'image', 'category']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        author = get_object_or_404(User, id=data["author_id"])
        category = get_object_or_404(Category, id=data["category_id"])

        ads = Ads.objects.create(
            name=data["name"],
            author=author,
            price=data["price"],
            description=data["description"],
            is_published=data["is_published"],
            image=data["image"],
            category=category,
        )

        return JsonResponse({
            "id": ads.id,
            "name": ads.name,
            "author_id": ads.author.id,
            "price": ads.price,
            "description": ads.description,
            "is_published": ads.is_published,
            "image": ads.image.url if ads.image else None,
            "category_id": ads.category.id,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'category']

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        self.object.name = data["name"]
        self.object.author = get_object_or_404(User, id=data["author_id"])
        self.object.price = data["price"]
        self.object.description = data["description"]
        self.object.is_published = data["is_published"]
        self.object.image = data["image"]
        self.object.category = get_object_or_404(Category, id=data["category_id"])

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url,
            "category": self.object.category.id,
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdsDeleteView(DeleteView):
    model = Ads
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsImageView(UpdateView):
    model = Ads
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(request.FILES)
        self.object.image = request.FILES.get('image', None)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.id,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url if self.object.image else None,
            "category": self.object.category.id,
        })


# ////////////////

@method_decorator(csrf_exempt, name='dispatch')
class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('name')

        response = []
        for ad in self.object_list:
            response.append({
                'id': ad.id,
                'name': ad.name,
            })
        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        category = Category.objects.create(
            name=data["name"],
        )

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        self.object.name = data["name"]

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
