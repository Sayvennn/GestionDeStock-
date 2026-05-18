from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from catalogue.models import Produit
from partenaires.models import Client, Fournisseur
from .models import (
    LigneOperation,
    MouvementStock,
    OperationStock,
    OperationStockEntree,
    OperationStockSortie,
)


@login_required(login_url="accounts:login")
def liste_operations(request):
    entrees = list(OperationStockEntree.objects.filter(employe=request.user).select_related("fournisseur", "employe"))
    sorties = list(OperationStockSortie.objects.filter(employe=request.user).select_related("client", "employe"))

    operations = []

    for operation in entrees:
        operations.append({
            "objet": operation,
            "type": "ENTREE",
            "partenaire": operation.fournisseur,
            "produit": operation.lignes,
        })

    for operation in sorties:
        operations.append({
            "objet": operation,
            "type": "SORTIE",
            "partenaire": operation.client,
            "produit": operation.lignes.select_related("produit").all(),
        })

    operations.sort(key=lambda item: item["objet"].date_operation, reverse=True)

    return render(request, "stock/operation_list.html", {
        "operations": operations,
    })


@login_required(login_url="accounts:login")
def liste_mouvements(request):
    mouvements = MouvementStock.objects.select_related(
        "produit",
        "ligne_operation",
        "operation",
        "operation__employe",
    ).order_by("-date_mouvement")

    return render(request, "stock/mouvement_list.html", {
        "mouvements": mouvements,
    })


@login_required(login_url="accounts:login")
def creer_entree(request):
    if request.method == "POST":
        operation = OperationStockEntree.objects.create(
            employe=request.user,
            fournisseur_id=request.POST.get("fournisseur"),
            statut="BROUILLON",
        )

        LigneOperation.objects.create(
            operation=operation,
            produit_id=request.POST.get("produit"),
            quantite=request.POST.get("quantite"),
        )

        messages.success(request, "Entrée créée en brouillon. Elle doit être validée pour impacter le stock.")
        return redirect("stock:operation_list")

    return render(request, "stock/entree_form.html", {
        "fournisseurs": Fournisseur.objects.all(),
        "produits": Produit.objects.all(),
    })


@login_required(login_url="accounts:login")
def creer_sortie(request):
    if request.method == "POST":
        operation = OperationStockSortie.objects.create(
            employe=request.user,
            client_id=request.POST.get("client"),
            statut="BROUILLON",
        )

        LigneOperation.objects.create(
            operation=operation,
            produit_id=request.POST.get("produit"),
            quantite=request.POST.get("quantite"),
        )

        messages.success(request, "Sortie créée en brouillon. Elle doit être validée pour impacter le stock.")
        return redirect("stock:operation_list")

    return render(request, "stock/sortie_form.html", {
        "clients": Client.objects.all(),
        "produits": Produit.objects.all(),
    })


@login_required(login_url="accounts:login")
def valider_entree(request, pk):
    operation = get_object_or_404(OperationStockEntree, pk=pk)

    try:
        operation.valider()
        messages.success(request, f"Entrée #{pk} validée. Mouvement de stock créé.")
    except Exception as e:
        messages.error(request, str(e))

    return redirect("stock:operation_list")


@login_required(login_url="accounts:login")
def valider_sortie(request, pk):
    operation = get_object_or_404(OperationStockSortie, pk=pk)

    try:
        operation.valider()
        messages.success(request, f"Sortie #{pk} validée. Mouvement de stock créé.")
    except Exception as e:
        messages.error(request, str(e))

    return redirect("stock:operation_list")


@login_required(login_url="accounts:login")
def annuler_entree(request, pk):
    operation = get_object_or_404(OperationStockEntree, pk=pk)

    try:
        operation.annuler()
        messages.success(request, f"Entrée #{pk} annulée.")
    except Exception as e:
        messages.error(request, str(e))

    return redirect("stock:operation_list")


@login_required(login_url="accounts:login")
def annuler_sortie(request, pk):
    operation = get_object_or_404(OperationStockSortie, pk=pk)

    try:
        operation.annuler()
        messages.success(request, f"Sortie #{pk} annulée.")
    except Exception as e:
        messages.error(request, str(e))

    return redirect("stock:operation_list")


@login_required(login_url="accounts:login")
def detail_operation(request, pk):
    operation = get_object_or_404(OperationStock, pk=pk)
    lignes = operation.lignes.select_related("produit")

    type_operation = "ENTREE" if hasattr(operation, "operationstockentree") else "SORTIE"

    return render(request, "stock/operation_detail.html", {
        "operation": operation,
        "lignes": lignes,
        "type_operation": type_operation,
    })
