from django.contrib import admin
from stock.models import Commande,LigneCommande,MouvementStock
# Register your models here.

admin.site.register([Commande,LigneCommande,MouvementStock])
