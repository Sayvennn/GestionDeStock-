from django.conf import settings
from abc import abstractmethod
from django.core.exceptions import ValidationError
from django.db import models,transaction

from catalogue.models import Produit
from partenaires.models import Client,Fournisseur

STATUT_CHOICES = [
        ("BROUILLON", "Brouillon"),
        ("VALIDEE", "Validée"),
        ("ANNULEE", "Annulée"),
    ]

class OperationStock(models.Model): 

    TYPE_OPERATION_CHOICES = [
        ('ENTREE', 'Entrée'),
        ('SORTIE', 'Sortie'),
    ]

    employe = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="operations_stock"
    )

    date_operation = models.DateTimeField(auto_now_add=True)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default="BROUILLON"
    )

    type_operation = models.CharField(
        max_length=10,
        choices=TYPE_OPERATION_CHOICES
    )

    # Champs spécifiques aux entrées
    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="operations_entree"
    )

    # Champs spécifiques aux sorties
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="operations_sortie"
    )

    class Meta:
        app_label = 'stock'

    def getTypeOperation(self):
        return self.type_operation

    def valider(self):
        if self.mouvements.exists():
            return

        with transaction.atomic():
            if self.type_operation == 'ENTREE':
                for l in self.lignes.select_related("produit"):
                    l.produit.quantite_stock += l.quantite
                    l.produit.save()
                    l.createMvtStock()
            elif self.type_operation == 'SORTIE':
                for l in self.lignes.select_related("produit"):
                    if not l.estStockSuffisant():
                        raise ValidationError(
                            f"Stock insuffisant pour {l.produit.nom}"
                        )
                    l.produit.quantite_stock -= l.quantite
                    l.produit.save()
                    l.createMvtStock()

    def __str__(self):
        return f"Opération {self.type_operation} - {self.date_operation}"


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
    
    def createMvtStock(self):
        return MouvementStock.objects.create(
            operation=self.operation,
            ligne_operation=self,
            produit=self.produit,
            type_mouvement=self.operation.type_operation,
        )

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"
    
    def estStockSuffisant(self):
        return self.quantite<=self.produit.quantite_stock


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

    type_mouvement = models.CharField(
        max_length=20,
        choices=TYPE_MOUVEMENT
    )

    date_mouvement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produit.nom} - {self.type_mouvement} ({self.date_mouvement})"

    type_mouvement = models.CharField(
        max_length=20,
        choices=TYPE_MOUVEMENT
    )

    date_mouvement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.produit.nom} - {self.type_mouvement} ({self.date_mouvement})"

    type_mouvement = models.CharField(max_length=10, choices=TYPE_MOUVEMENT)
    # quantite = models.PositiveIntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom} ({self.ligne_operation.quantite})"