from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render

from catalogue.models import Categorie, Produit
from partenaires.models import Client, Fournisseur
from stock.models import OperationStock, OperationStockEntree, OperationStockSortie


@login_required(login_url="accounts:login")
def parametres(request):
    context = {
        "total_produits": Produit.objects.count(),
        "total_categories": Categorie.objects.count(),
        "total_clients": Client.objects.count(),
        "total_fournisseurs": Fournisseur.objects.count(),
        "operations_brouillon": OperationStock.objects.filter(statut="BROUILLON").count(),
        "entrees_brouillon": OperationStockEntree.objects.filter(statut="BROUILLON").count(),
        "sorties_brouillon": OperationStockSortie.objects.filter(statut="BROUILLON").count(),
        "produits_alerte": Produit.objects.filter(quantite_stock__lte=F("seuil_alerte")).count(),
    }

    return render(request, "core/parametres.html", context)
