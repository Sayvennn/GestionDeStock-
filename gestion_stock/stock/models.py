from django.db import models
from products.models import Produit
from users.models import Employe

# Create your models here.
class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('validee', 'Validee'),
        ('annulee', 'Annulee'),
    ]

    date_commande = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)

    def __str__(self):
        return f"Commande {self.id} - {self.statut}"


class LigneCommande(models.Model):
    commande = models.ForeignKey(
        Commande,
        on_delete=models.CASCADE,
        related_name='lignes'
    )
    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='lignes_commande'
    )
    quantite = models.IntegerField()
    prix = models.IntegerField()

    def __str__(self):
        return f"Ligne {self.id} - Commande {self.commande.id}"


class MouvementStock(models.Model):
    TYPE_MOUVEMENT_CHOICES = [
        ('entree', 'Entree'),
        ('sortie', 'Sortie'),
    ]

    produit = models.ForeignKey(
        Produit,
        on_delete=models.CASCADE,
        related_name='mouvements'
    )
    employe = models.ForeignKey(
        Employe,
        on_delete=models.CASCADE,
        related_name='mouvements'
    )
    type_mouvement = models.CharField(max_length=20, choices=TYPE_MOUVEMENT_CHOICES)
    quantite = models.IntegerField()
    date_mouvement = models.DateField()

    def __str__(self):
        return f"{self.type_mouvement} - {self.produit.nom}"