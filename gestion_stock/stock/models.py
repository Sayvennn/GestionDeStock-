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
    class Meta:
        abstract=False

    @abstractmethod
    def getTypeOperation(self):
        pass

class OperationStockEntree(OperationStock): 

    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="Entree_stock"
    )

    def getTypeOperation(self):
        return "ENTREE"
    
    def valider(self):
        if self.mouvements.exists():
            return

        with transaction.atomic():
            for l in self.lignes.select_related("produit"):
                l.produit.quantite_stock += l.quantite
                l.produit.save()
                l.createMvtStock()
                self.statut="VALIDEE"
                self.save()
    
    def annuler(self):
        if self.statut=="BROUILLON":
            self.statut="ANNULEE"
            self.save() 
            return
        if not self.mouvements.exists():
            return
        print("Annulation de l'entrée, retrait du stock des produits...")
        with transaction.atomic():
            print("0000000000000")
            for m in self.mouvements.select_related("produit","ligne_operation"):
                if m.produit.quantite_stock < m.ligne_operation.quantite:
                    self.statut="ANNULEE"
                    self.save() 
                    raise ValidationError(
                        f"Stock insuffisant pour {m.produit.nom} pour qte {m.ligne_operation.quantite} à annuler"
                    )
                m.produit.quantite_stock -= m.ligne_operation.quantite
                print("1111111111111")
                m.produit.save()
                m.delete()

class OperationStockSortie(OperationStock):

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="sortie_stock"
    )

    def getTypeOperation(self):
        return "SORTIE"
    
    def valider(self):
        if self.mouvements.exists():
            return

        with transaction.atomic():
            for l in self.lignes.select_related("produit"):
                if not l.estStockSuffisant():
                    self.statut="BROUILLON"
                    self.save() 
                    raise ValidationError(f"Stock insuffisant pour {l.produit.nom}")

                l.produit.quantite_stock -= l.quantite
                l.produit.save()
                l.createMvtStock()
                self.statut="VALIDEE"
                self.save()
                print("mvt added")
    
    def annuler(self):
        if not self.mouvements.exists():
            return
        print("Annulation de la sortie, retour en stock des produits...")
        with transaction.atomic():
            for m in self.mouvements.select_related("produit","ligne_operation"):
                m.produit.quantite_stock+=m.ligne_operation.quantite
                m.produit.save()
                m.delete()
                


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
            type_mouvement="SORTIE" if hasattr(self.operation, 'operationstocksortie') else "ENTREE",
        )
    def createMvtStockRetour(self):
        return MouvementStock.objects.create(
            operation=self.operation,
            ligne_operation=self,
            produit=self.produit,
            type_mouvement=f"RETOUR {self.operation.getTypeOperation()}",
        )

    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"
    
    def estStockSuffisant(self):
        return self.quantite<=self.produit.quantite_stock


class MouvementStock(models.Model):
    TYPE_MOUVEMENT = [
        ("ENTREE", "Entrée"),
        ("SORTIE", "Sortie"),
        ("RETOUR ENTREE", "Retour fournisseur"),
        ("RETOUR SORTIE", "Retour client"),
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

    type_mouvement = models.CharField(max_length=15, choices=TYPE_MOUVEMENT)
    # quantite = models.PositiveIntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom} ({self.ligne_operation.quantite})"
    

    
