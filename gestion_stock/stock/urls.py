from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    # --- TABLEAU DE BORD & HISTORIQUE ---
    # Liste globale de tous les mouvements (le journal de bord)
    path('mouvements/', views.liste_mouvements, name='mouvement_list'),
    
    # --- ENTRÉES (FOURNISSEURS) ---
    path('entrees/', views.liste_entrees, name='entree_list'),
    path('entrees/nouvelle/', views.creer_entree, name='entree_add'),
    path('entrees/<int:pk>/valider/', views.valider_entree, name='entree_validate'),
    
    # --- SORTIES (CLIENTS) ---
    path('sorties/', views.liste_sorties, name='sortie_list'),
    path('sorties/nouvelle/', views.creer_sortie, name='sortie_add'),
    path('sorties/<int:pk>/valider/', views.valider_sortie, name='sortie_validate'),

    # --- DÉTAILS ---
    # Voir les lignes d'une opération spécifique
    path('operation/<int:pk>/', views.detail_operation, name='operation_detail'),
]