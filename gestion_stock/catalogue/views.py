from django.shortcuts import get_object_or_404, redirect, render

from partenaires.models import Fournisseur
from .models import Categorie, Produit


def dashboard(request):
    context = {
        "total_produits": Produit.objects.count(),
        "total_categories": Categorie.objects.count(),
        "alertes_stock": 0,
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
