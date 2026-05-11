from django.urls import path
from . import views

app_name = "partenaires"

urlpatterns = [
    path("", views.liste_partenaires, name="partenaire_list"),
    path("clients/", views.liste_clients, name="client_list"),
    path("fournisseurs/", views.liste_fournisseurs, name="fournisseur_list"),

    path("clients/<int:pk>/modifier/", views.modifier_client, name="client_edit"),
    path("clients/<int:pk>/supprimer/", views.supprimer_client, name="client_delete"),
    path("fournisseurs/<int:pk>/modifier/", views.modifier_fournisseur, name="fournisseur_edit"),
    path("fournisseurs/<int:pk>/supprimer/", views.supprimer_fournisseur, name="fournisseur_delete"),
]
