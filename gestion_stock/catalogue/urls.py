from django.urls import path
from . import views

app_name = "catalogue"

urlpatterns = [
    path("", views.produit_list, name="produit_list"),
    path("produits/", views.produit_list, name="produit_list"),
    path("produits/nouveau/", views.produit_add, name="produit_add"),
    path("categories/", views.categorie_list, name="categorie_list"),
    path("categories/nouveau/", views.categorie_add, name="categorie_add"),
    path("categories/<int:pk>/modifier/", views.categorie_edit, name="categorie_edit"),
]
