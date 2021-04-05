from django.contrib import admin
from .models import news, Images, Category, TagsNValue

# Register your models here.
admin.site.register(news)
admin.site.register(Images)
admin.site.register(Category)
admin.site.register(TagsNValue)