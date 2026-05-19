from django.db import models
from partenaires.models import Fournisseur

# Create your models here.
class Categorie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=100)
    reference = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    seuil_alerte=models.PositiveIntegerField(default=5)
    quantite_stock=models.PositiveBigIntegerField(default=0)

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,
        related_name="produits"
    )

    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT,
        related_name="produits"
    )

    def __str__(self):
        return f"{self.nom} ({self.reference})"

    def save(self, *args, **kwargs):
        if self.reference and Produit.objects.filter(reference=self.reference).exclude(pk=self.pk).exists():
            raise ValueError("La référence doit être unique.")
        super().save(*args, **kwargs)
