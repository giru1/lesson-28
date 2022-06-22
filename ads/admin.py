from django.contrib import admin

# Register your models here.
from ads.models import Ads, Category
from users.models import Location, User

admin.site.register(Ads)
admin.site.register(Category)
admin.site.register(Location)
admin.site.register(User)

