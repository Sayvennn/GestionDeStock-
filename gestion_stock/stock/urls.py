from django.urls import path
from . import views

app_name = "stock"

urlpatterns = [
    path("operations/", views.liste_operations, name="operation_list"),
    path("mouvements/", views.liste_mouvements, name="mouvement_list"),

    path("entrees/nouvelle/", views.creer_entree, name="entree_add"),
    path("entrees/<int:pk>/valider/", views.valider_entree, name="entree_validate"),
    path("entrees/<int:pk>/annuler/", views.annuler_entree, name="entree_cancel"),

    path("sorties/nouvelle/", views.creer_sortie, name="sortie_add"),
    path("sorties/<int:pk>/valider/", views.valider_sortie, name="sortie_validate"),
    path("sorties/<int:pk>/annuler/", views.annuler_sortie, name="sortie_cancel"),

    path("operation/<int:pk>/", views.detail_operation, name="operation_detail"),
]
