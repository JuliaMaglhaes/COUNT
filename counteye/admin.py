from django.contrib import admin
from . import models

@admin.register(models.Count)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('product', 'id', 'status', 'slug', 'author')
    prepopulate_fields = {'slug': ('product',),}

admin.site.register(models.Category)

