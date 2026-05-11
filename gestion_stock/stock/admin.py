from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from .models import OperationStockEntree, OperationStockSortie, LigneOperation, MouvementStock

# 1. Gestion des lignes en ligne (Inline)
class LigneOperationInline(admin.TabularInline):
    model = LigneOperation
    extra = 1
    fields = ('produit', 'quantite')

# 2. Admin pour les ENTRÉES (Fournisseurs)

@admin.register(OperationStockEntree)
class OperationStockEntreeAdmin(admin.ModelAdmin):
    list_display = ("id", "fournisseur", "employe", "statut", "date_operation")
    list_filter = ("statut", "date_operation")
    search_fields = ("fournisseur__nom", "employe__username")
    inlines = [LigneOperationInline]
    fields = ("employe", "fournisseur", "statut")

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        operation = form.instance

        if operation.statut == "VALIDEE":
            try:
                operation.valider()
            except ValidationError as e:
                messages.error(request, e.message)
        elif operation.statut=="ANNULEE":
            try:
                operation.annuler()
            except ValidationError as e:
                messages.error(request, e.message)



# 3. Admin pour les SORTIES (Clients)
@admin.register(OperationStockSortie)
class OperationStockSortieAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "employe", "statut", "date_operation")
    list_filter = ("statut", "date_operation")
    search_fields = ("client__nom", "employe__username")
    inlines = [LigneOperationInline]
    fields = ("employe", "client", "statut")

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        operation = form.instance

        if operation.statut == "VALIDEE":
            try:
                operation.valider()
            except ValidationError as e:
                messages.error(request, e.message)
        elif operation.statut=="ANNULEE":
            try:
                operation.annuler()
            except ValidationError as e:
                messages.error(request, e.message)



# 4. Historique des mouvements (Lecture seule recommandée)
@admin.register(MouvementStock)
class MouvementStockAdmin(admin.ModelAdmin):
    list_display = (
        "produit",
        "type_mouvement",
        "get_quantite",
        "date_mouvement",
        "operation",
    )
    list_filter = ("type_mouvement", "date_mouvement")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_quantite(self, obj):
        return obj.ligne_operation.quantite

    get_quantite.short_description = "Quantité"