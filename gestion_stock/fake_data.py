import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_stock.settings")
django.setup()

from faker import Faker

from accounts.models import Employe
from partenaires.models import Client, Fournisseur
from catalogue.models import Produit, Categorie
from stock.models import (
    OperationStock,
    LigneOperation,
    MouvementStock
)

fake = Faker("fr_FR")


# =========================
# EMPLOYES
# =========================

for i in range(5):
    Employe.objects.create_user(
        username=f"user{i}",
        password="1234",
        email=fake.email()
    )


# =========================
# CLIENTS
# =========================

clients = []

for _ in range(10):
    client = Client.objects.create(
        nom=fake.name(),
        email=fake.email(),
        telephone=fake.phone_number(),
        adresse=fake.address()
    )

    clients.append(client)


# =========================
# FOURNISSEURS
# =========================

fournisseurs = []

for _ in range(5):
    fournisseur = Fournisseur.objects.create(
        nom=fake.company(),
        email=fake.company_email(),
        telephone=fake.phone_number(),
        adresse=fake.address()
    )

    fournisseurs.append(fournisseur)


# =========================
# CATEGORIES
# =========================

categories = []

for nom in [
    "Informatique",
    "Téléphone",
    "Accessoires",
    "Bureau"
]:
    categorie = Categorie.objects.create(
        nom=nom,
        description=fake.text()
    )

    categories.append(categorie)


# =========================
# PRODUITS
# =========================

produits = []

for i in range(20):
    produit = Produit.objects.create(
        nom=fake.word().capitalize(),
        reference=f"REF-{i}",
        description=fake.text(),
        prix=random.randint(50, 5000),
        categorie=random.choice(categories),
        fournisseur=random.choice(fournisseurs)
    )

    produits.append(produit)


# =========================
# OPERATIONS
# =========================

employes = list(Employe.objects.all())

for _ in range(15):

    type_operation = random.choice(["ENTREE", "SORTIE"])

    operation = OperationStock.objects.create(
        type_operation=type_operation,
        employe=random.choice(employes),
        client=random.choice(clients) if type_operation == "SORTIE" else None,
        statut="VALIDEE"
    )

    nb_lignes = random.randint(1, 4)

    for _ in range(nb_lignes):

        produit = random.choice(produits)

        quantite = random.randint(1, 10)

        ligne = LigneOperation.objects.create(
            operation=operation,
            produit=produit,
            quantite=quantite,
            prix_total=produit.prix * quantite
        )

        MouvementStock.objects.create(
            operation=operation,
            ligne_operation=ligne,
            produit=produit,
            type_mouvement=type_operation,
            quantite=quantite
        )


print("Fake data generated successfully.")