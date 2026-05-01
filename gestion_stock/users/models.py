from django.db import models

# Create your models here.
class Employe(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=128)

    def __str__(self):
        return self.nom