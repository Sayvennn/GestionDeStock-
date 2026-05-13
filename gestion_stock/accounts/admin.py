from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Employe


@admin.register(Employe)
class EmployeAdmin(UserAdmin):
    list_display = ("username", "email", "telephone", "is_staff", "is_superuser")
    search_fields = ("username", "email", "telephone")

    fieldsets = UserAdmin.fieldsets + (
        ("Informations employé", {
            "fields": ("telephone", "adresse"),
        }),
    )
