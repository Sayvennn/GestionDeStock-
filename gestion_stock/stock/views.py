from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from catalogue.models import Produit
from partenaires.models import Client, Fournisseur
from .models import LigneOperation, MouvementStock, OperationStock
from django.contrib.auth.decorators import login_required



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


def liste_entrees(request):
    entrees = OperationStock.objects.filter(
        type_operation="ENTREE"
    ).select_related("fournisseur", "employe").order_by("-date_operation")

    return render(request, "stock/entree_list.html", {
        "entrees": entrees,
    })

@login_required(login_url="accounts:login")
def creer_entree(request):
    if request.method == "POST":
        fournisseur_id = request.POST.get("fournisseur")
        produit_id = request.POST.get("produit")
        quantite = request.POST.get("quantite")

        operation = OperationStock.objects.create(
            employe=request.user,
            type_operation="ENTREE",
            fournisseur_id=fournisseur_id,
            statut="BROUILLON",
        )

        LigneOperation.objects.create(
            operation=operation,
            produit_id=produit_id,
            quantite=quantite,
        )

        return redirect("stock:entree_list")

    fournisseurs = Fournisseur.objects.all()
    produits = Produit.objects.all()

    return render(request, "stock/entree_form.html", {
        "fournisseurs": fournisseurs,
        "produits": produits,
    })

@login_required(login_url="accounts:login")
def valider_entree(request, pk):
    operation = get_object_or_404(OperationStock, pk=pk, type_operation="ENTREE")

    try:
        operation.valider()
        operation.statut = "VALIDEE"
        operation.save()
        messages.success(request, f"L'entrée #{pk} a été validée et le stock mis à jour.")
    except Exception as e:
        messages.error(request, f"Erreur lors de la validation : {str(e)}")

    return redirect("stock:entree_list")


def liste_sorties(request):
    sorties = OperationStock.objects.filter(
        type_operation="SORTIE"
    ).select_related("client", "employe").order_by("-date_operation")

    return render(request, "stock/sortie_list.html", {
        "sorties": sorties,
    })

@login_required(login_url="accounts:login")
def creer_sortie(request):
    if request.method == "POST":
        client_id = request.POST.get("client")
        produit_id = request.POST.get("produit")
        quantite = request.POST.get("quantite")

        operation = OperationStock.objects.create(
            employe=request.user,
            type_operation="SORTIE",
            client_id=client_id,
            statut="BROUILLON",
        )

        LigneOperation.objects.create(
            operation=operation,
            produit_id=produit_id,
            quantite=quantite,
        )

        return redirect("stock:sortie_list")

    clients = Client.objects.all()
    produits = Produit.objects.all()

    return render(request, "stock/sortie_form.html", {
        "clients": clients,
        "produits": produits,
    })

@login_required(login_url="accounts:login")
def valider_sortie(request, pk):
    operation = get_object_or_404(OperationStock, pk=pk, type_operation="SORTIE")

    try:
        operation.valider()
        operation.statut = "VALIDEE"
        operation.save()
        messages.success(request, f"La sortie #{pk} a été validée.")
    except Exception as e:
        messages.error(request, f"Échec : {str(e)}")

    return redirect("stock:sortie_list")


def detail_operation(request, pk):
    operation = get_object_or_404(OperationStock, pk=pk)
    lignes = operation.lignes.all().select_related("produit")

    return render(request, "stock/operation_detail.html", {
        "operation": operation,
        "lignes": lignes,
    })
