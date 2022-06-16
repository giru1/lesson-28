from django.contrib import admin

# Register your models here.
from ads.models import Ads, Category, Location, User

admin.site.register(Ads)
admin.site.register(Category)
admin.site.register(Location)

