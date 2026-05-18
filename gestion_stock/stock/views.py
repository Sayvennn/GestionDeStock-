from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from catalogue.models import Produit
from partenaires.models import Client, Fournisseur
from .models import (
    LigneOperation,
    MouvementStock,
    OperationStock,
    OperationStockEntree,
    OperationStockSortie,
    STATUT_CHOICES,
)


@login_required(login_url="accounts:login")
def liste_operations(request):
    recherche = request.GET.get("q", "").strip()
    type_filtre = request.GET.get("type", "all")
    statut_filtre = request.GET.get("statut", "all")

    types_valides = {"all", "entree", "sortie"}
    statuts_valides = {statut for statut, _ in STATUT_CHOICES}

    if type_filtre not in types_valides:
        type_filtre = "all"

    if statut_filtre != "all" and statut_filtre not in statuts_valides:
        statut_filtre = "all"

    entrees_qs = OperationStockEntree.objects.select_related("fournisseur", "employe")
    sorties_qs = OperationStockSortie.objects.select_related("client", "employe")

    if statut_filtre != "all":
        entrees_qs = entrees_qs.filter(statut=statut_filtre)
        sorties_qs = sorties_qs.filter(statut=statut_filtre)

    if recherche:
        filtre_entrees = (
            Q(fournisseur__nom__icontains=recherche)
            | Q(employe__username__icontains=recherche)
            | Q(lignes__produit__nom__icontains=recherche)
            | Q(lignes__produit__reference__icontains=recherche)
        )
        filtre_sorties = (
            Q(client__nom__icontains=recherche)
            | Q(employe__username__icontains=recherche)
            | Q(lignes__produit__nom__icontains=recherche)
            | Q(lignes__produit__reference__icontains=recherche)
        )

        if recherche.isdigit():
            filtre_entrees |= Q(pk=int(recherche))
            filtre_sorties |= Q(pk=int(recherche))

        entrees_qs = entrees_qs.filter(filtre_entrees).distinct()
        sorties_qs = sorties_qs.filter(filtre_sorties).distinct()

    entrees = list(entrees_qs) if type_filtre in {"all", "entree"} else []
    sorties = list(sorties_qs) if type_filtre in {"all", "sortie"} else []

    operations = []

    for operation in entrees:
        operations.append({
            "objet": operation,
            "type": "ENTREE",
            "partenaire": operation.fournisseur,
        })

    for operation in sorties:
        operations.append({
            "objet": operation,
            "type": "SORTIE",
            "partenaire": operation.client,
        })

    operations.sort(key=lambda item: item["objet"].date_operation, reverse=True)

    return render(request, "stock/operation_list.html", {
        "operations": operations,
        "recherche": recherche,
        "type_filtre": type_filtre,
        "statut_filtre": statut_filtre,
        "statuts": STATUT_CHOICES,
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
        client_id = request.POST.get("client")
        produit_id = request.POST.get("produit")
        quantite_saisie = request.POST.get("quantite")

        try:
            produit = Produit.objects.get(pk=produit_id)
            quantite_demandee = int(quantite_saisie)
        except (Produit.DoesNotExist, TypeError, ValueError):
            return render(request, "stock/sortie_form.html", {
                "clients": Client.objects.all(),
                "produits": Produit.objects.all(),
                "error": "Veuillez selectionner un produit et saisir une quantite valide.",
                "selected_client": client_id,
                "selected_produit": produit_id,
                "quantite": quantite_saisie or "",
            })

        if quantite_demandee > produit.quantite_stock:
            return render(request, "stock/sortie_form.html", {
                "clients": Client.objects.all(),
                "produits": Produit.objects.all(),
                "error": (
                    f"Stock insuffisant pour {produit.nom}. "
                    f"Stock disponible: {produit.quantite_stock}, quantite demandee: {quantite_demandee}."
                ),
                "selected_client": client_id,
                "selected_produit": produit_id,
                "quantite": quantite_demandee,
            })

        operation = OperationStockSortie.objects.create(
            employe=request.user,
            client_id=client_id,
            statut="BROUILLON",
        )

        LigneOperation.objects.create(
            operation=operation,
            produit=produit,
            quantite=quantite_demandee,
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
        for ligne in operation.lignes.select_related("produit"):
            if ligne.quantite > ligne.produit.quantite_stock:
                messages.error(
                    request,
                    (
                        f"Stock insuffisant pour {ligne.produit.nom}. "
                        f"Stock disponible: {ligne.produit.quantite_stock}, quantite demandee: {ligne.quantite}."
                    )
                )
                return redirect("stock:operation_list")

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
