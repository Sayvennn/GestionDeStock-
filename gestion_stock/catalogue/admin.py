from django.contrib import admin
from .models import Produit,Categorie

# Register your models here.
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ("nom",)
    search_fields = ("nom",)


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "reference",
        "categorie",
        "fournisseur",
        "prix",
    )

    list_filter = ("categorie", "fournisseur")

    search_fields = (
        "nom",
        "reference",
    )