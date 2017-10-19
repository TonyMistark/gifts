from django.contrib import admin
from friends import models as frd_models

# Register your models here.


@admin.register(frd_models.User)
class UserAdmin(admin.ModelAdmin):

    list_display = ("id", "slug", "username", )
    list_per_page = 20
    search_fields = ("username", "slug")


@admin.register(frd_models.Interests)
class InterestsAdmin(admin.ModelAdmin):

    list_display = ("id", "user", )
    list_per_page = 20

