from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from catalogue.models import Produit
from partenaires.models import Client


class OperationStock(models.Model):
    TYPE_OPERATION = [
        ("ENTREE", "Entrée"),
        ("SORTIE", "Sortie"),
    ]

    STATUT_CHOICES = [
        ("BROUILLON", "Brouillon"),
        ("VALIDEE", "Validée"),
        ("ANNULEE", "Annulée"),
    ]

    type_operation = models.CharField(max_length=10, choices=TYPE_OPERATION)

    employe = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="operations_stock"
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="operations_stock"
    )

    date_operation = models.DateTimeField(auto_now_add=True)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="BROUILLON"
    )

    def clean(self):
        if self.type_operation == "SORTIE" and not self.client:
            raise ValidationError("Une sortie doit avoir un client.")

        if self.type_operation == "ENTREE" and self.client:
            raise ValidationError("Une entrée ne doit pas avoir de client.")

    def __str__(self):
        return f"{self.type_operation} #{self.id}"


class LigneOperation(models.Model):
    operation = models.ForeignKey(
        OperationStock,
        on_delete=models.CASCADE,
        related_name="lignes"
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
        related_name="lignes_operation"
    )

    quantite = models.PositiveIntegerField()
    # prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"


class MouvementStock(models.Model):
    TYPE_MOUVEMENT = [
        ("ENTREE", "Entrée"),
        ("SORTIE", "Sortie"),
    ]

    operation = models.ForeignKey(
        OperationStock,
        on_delete=models.PROTECT,
        related_name="mouvements"
    )

    ligne_operation = models.OneToOneField(
        LigneOperation,
        on_delete=models.PROTECT,
        related_name="mouvement"
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT,
        related_name="mouvements_stock"
    )

    type_mouvement = models.CharField(max_length=10, choices=TYPE_MOUVEMENT)
    quantite = models.PositiveIntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom} ({self.quantite})"