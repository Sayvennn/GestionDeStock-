from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from partenaires.models import Client, Fournisseur
from .models import Categorie, Produit

from django.db.models import F, Sum
from django.db.models.functions import TruncDate
from stock.models import MouvementStock, OperationStock, OperationStockEntree, OperationStockSortie
@login_required(login_url="accounts:login")
def dashboard(request):
    entrees = (
        MouvementStock.objects
        .filter(type_mouvement="ENTREE")
        .annotate(jour=TruncDate("date_mouvement"))
        .values("jour")
        .annotate(total=Sum("ligne_operation__quantite"))
        .order_by("jour")
    )
    sorties = (
        MouvementStock.objects
        .filter(type_mouvement="SORTIE")
        .annotate(jour=TruncDate("date_mouvement"))
        .values("jour")
        .annotate(total=Sum("ligne_operation__quantite"))
        .order_by("jour")
    )
    entrees_dict = {
        item["jour"]: item["total"] or 0
        for item in entrees
        if item["jour"]
    }
    sorties_dict = {
        item["jour"]: item["total"] or 0
        for item in sorties
        if item["jour"]
    }
    jours = sorted(set(entrees_dict.keys()) | set(sorties_dict.keys()))
    chart_points = [
        {
            "date": jour.strftime("%d/%m/%Y"),
            "entree": entrees_dict.get(jour, 0),
            "sortie": sorties_dict.get(jour, 0),
        }
        for jour in jours
    ]

    categories_stock = (
        Produit.objects
        .values("categorie__nom")
        .annotate(total=Sum("quantite_stock"))
        .order_by("categorie__nom")
    )

    category_points = [
        {
            "nom": item["categorie__nom"] or "Sans categorie",
            "total": item["total"] or 0,
        }
        for item in categories_stock
    ]

    entrees_recentes = list(
        OperationStockEntree.objects
        .select_related("fournisseur", "employe")
        .order_by("-date_operation")[:6]
    )
    sorties_recentes = list(
        OperationStockSortie.objects
        .select_related("client", "employe")
        .order_by("-date_operation")[:6]
    )

    operations_recentes = []

    for operation in entrees_recentes:
        operations_recentes.append({
            "objet": operation,
            "type": "ENTREE",
            "partenaire": operation.fournisseur,
        })

    for operation in sorties_recentes:
        operations_recentes.append({
            "objet": operation,
            "type": "SORTIE",
            "partenaire": operation.client,
        })

    operations_recentes.sort(key=lambda item: item["objet"].date_operation, reverse=True)
    operations_recentes = operations_recentes[:6]

    produits_alerte = Produit.objects.filter(
        quantite_stock__lte=F("seuil_alerte")
    ).select_related("categorie", "fournisseur")

    context = {
        "total_produits": Produit.objects.count(),
        "total_categories": Categorie.objects.count(),
        "total_clients": Client.objects.count(),
        "total_fournisseurs": Fournisseur.objects.count(),
        "total_stock": Produit.objects.aggregate(total=Sum("quantite_stock"))["total"] or 0,
        "total_entrees": MouvementStock.objects.filter(type_mouvement="ENTREE").aggregate(
            total=Sum("ligne_operation__quantite")
        )["total"] or 0,
        "total_sorties": MouvementStock.objects.filter(type_mouvement="SORTIE").aggregate(
            total=Sum("ligne_operation__quantite")
        )["total"] or 0,
        "operations_brouillon": OperationStock.objects.filter(statut="BROUILLON").count(),
        "operations_validees": OperationStock.objects.filter(statut="VALIDEE").count(),
        "alertes_stock": produits_alerte.count(),
        "chart_points": chart_points,
        "category_points": category_points,
        "produits_rupture": produits_alerte,
        "operations_recentes": operations_recentes,
        "mouvements_recents": MouvementStock.objects.select_related(
            "produit",
            "ligne_operation",
            "operation",
            "operation__employe",
        ).order_by("-date_mouvement")[:6],
        "top_produits": Produit.objects.annotate(
            volume_mouvement=Sum("mouvements_stock__ligne_operation__quantite")
        ).filter(
            volume_mouvement__isnull=False
        ).select_related("categorie").order_by("-volume_mouvement")[:5],
    }
    return render(request, "core/dashboard.html", context)
def produit_list(request):
    produits = Produit.objects.select_related("categorie", "fournisseur").all()
    return render(request, "catalogue/produit_list.html", {
        "produits": produits,
    })
def produit_add(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        reference = request.POST.get("reference")
        description = request.POST.get("description")
        prix = request.POST.get("prix")
        categorie_id = request.POST.get("categorie")
        fournisseur_id = request.POST.get("fournisseur")
        if not nom or not reference or not prix or not categorie_id or not fournisseur_id:
            categories = Categorie.objects.all()
            fournisseurs = Fournisseur.objects.all()
            return render(request, "catalogue/produit_form.html", {
                "categories": categories,
                "fournisseurs": fournisseurs,
                "error": "Veuillez remplir tous les champs obligatoires.",
            })
        Produit.objects.create(
            nom=nom,
            reference=reference,
            description=description,
            prix=prix,
            categorie_id=categorie_id,
            fournisseur_id=fournisseur_id,
        )
        return redirect("catalogue:produit_list")
    categories = Categorie.objects.all()
    fournisseurs = Fournisseur.objects.all()
    return render(request, "catalogue/produit_form.html", {
        "categories": categories,
        "fournisseurs": fournisseurs,
    })
def categorie_list(request):
    categories = Categorie.objects.all()
    return render(request, "catalogue/categorie_list.html", {
        "categories": categories,
    })
def categorie_add(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        description = request.POST.get("description", "")
        if not nom:
            return render(request, "catalogue/categorie_form.html", {
                "error": "Le nom de la catégorie est obligatoire.",
            })
        Categorie.objects.create(
            nom=nom,
            description=description,
        )
        return redirect("catalogue:categorie_list")
    return render(request, "catalogue/categorie_form.html")
def categorie_edit(request, pk):
    categorie = get_object_or_404(Categorie, pk=pk)
    if request.method == "POST":
        nom = request.POST.get("nom")
        description = request.POST.get("description", "")
        if not nom:
            return render(request, "catalogue/categorie_form.html", {
                "categorie": categorie,
                "error": "Le nom de la catégorie est obligatoire.",
            })
        categorie.nom = nom
        categorie.description = description
        categorie.save()
        return redirect("catalogue:categorie_list")
    return render(request, "catalogue/categorie_form.html", {
        "categorie": categorie,
    })
