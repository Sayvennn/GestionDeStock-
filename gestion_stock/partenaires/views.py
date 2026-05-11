from django.shortcuts import render, redirect
from .models import Client, Fournisseur
from django.shortcuts import get_object_or_404


def liste_partenaires(request):
    if request.method == "POST":
        type_partenaire = request.POST.get("type_partenaire")

        data = {
            "nom": request.POST.get("nom"),
            "email": request.POST.get("email"),
            "telephone": request.POST.get("telephone"),
            "adresse": request.POST.get("adresse"),
        }

        if type_partenaire == "fournisseur":
            Fournisseur.objects.create(**data)
        else:
            Client.objects.create(**data)

        return redirect("partenaires:partenaire_list")

    clients = list(Client.objects.all())
    fournisseurs = list(Fournisseur.objects.all())

    for client in clients:
        client.type = "Client"

    for fournisseur in fournisseurs:
        fournisseur.type = "Fournisseur"

    partenaires = clients + fournisseurs

    return render(request, "partenaires/partenaire_list.html", {
        "partenaires": partenaires,
        "titre": "Liste des Partenaires",
    })


def liste_clients(request):
    partenaires = list(Client.objects.all())

    for p in partenaires:
        p.type = "Client"

    return render(request, "partenaires/partenaire_list.html", {
        "partenaires": partenaires,
        "titre": "Liste des Clients",
    })


def liste_fournisseurs(request):
    partenaires = list(Fournisseur.objects.all())

    for p in partenaires:
        p.type = "Fournisseur"

    return render(request, "partenaires/partenaire_list.html", {
        "partenaires": partenaires,
        "titre": "Liste des Fournisseurs",
    })



def modifier_client(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.nom = request.POST.get("nom")
        client.email = request.POST.get("email")
        client.telephone = request.POST.get("telephone")
        client.adresse = request.POST.get("adresse")
        client.save()
        return redirect("partenaires:partenaire_list")

    return render(request, "partenaires/partenaire_form.html", {
        "partenaire": client,
        "type_partenaire": "client",
        "titre": "Modifier Client",
    })


def supprimer_client(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.delete()
        return redirect("partenaires:partenaire_list")

    return render(request, "partenaires/partenaire_confirm_delete.html", {
        "partenaire": client,
        "type_partenaire": "client",
    })


def modifier_fournisseur(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)

    if request.method == "POST":
        fournisseur.nom = request.POST.get("nom")
        fournisseur.email = request.POST.get("email")
        fournisseur.telephone = request.POST.get("telephone")
        fournisseur.adresse = request.POST.get("adresse")
        fournisseur.save()
        return redirect("partenaires:partenaire_list")

    return render(request, "partenaires/partenaire_form.html", {
        "partenaire": fournisseur,
        "type_partenaire": "fournisseur",
        "titre": "Modifier Fournisseur",
    })


def supprimer_fournisseur(request, pk):
    fournisseur = get_object_or_404(Fournisseur, pk=pk)

    if request.method == "POST":
        fournisseur.delete()
        return redirect("partenaires:partenaire_list")

    return render(request, "partenaires/partenaire_confirm_delete.html", {
        "partenaire": fournisseur,
        "type_partenaire": "fournisseur",
    })
