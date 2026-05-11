from django.contrib import admin
from .models import Client,Fournisseur

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "telephone")
    search_fields = ("nom", "email")


@admin.register(Fournisseur)
class FournisseurAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "telephone")
    search_fields = ("nom", "email")