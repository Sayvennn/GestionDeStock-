from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Employe(AbstractUser):
    telephone = models.CharField(max_length=20, blank=True, null=True)
    adresse = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Employé"
        verbose_name_plural = "Employés"

    def __str__(self):
        return self.username