from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import (
    LigneOperation,
    MouvementStock,
    OperationStockEntree,
    OperationStockSortie,
)


class LigneOperationInline(admin.TabularInline):
    model = LigneOperation
    extra = 1
    fields = ("produit", "quantite")


@admin.register(OperationStockEntree)
class OperationStockEntreeAdmin(admin.ModelAdmin):
    list_display = ("id", "fournisseur", "employe", "statut", "date_operation")
    list_filter = ("statut", "date_operation")
    search_fields = ("fournisseur__nom", "employe__username")
    inlines = [LigneOperationInline]
    fields = ("employe", "fournisseur", "statut")
    readonly_fields = ("statut",)
    actions = ("valider_operations", "annuler_operations")

    @admin.action(description="Valider les entrées sélectionnées")
    def valider_operations(self, request, queryset):
        for operation in queryset:
            try:
                operation.valider()
                messages.success(request, f"Entrée #{operation.pk} validée.")
            except ValidationError as e:
                messages.error(request, f"Entrée #{operation.pk} : {e.message}")
            except Exception as e:
                messages.error(request, f"Entrée #{operation.pk} : {str(e)}")

    @admin.action(description="Annuler les entrées sélectionnées")
    def annuler_operations(self, request, queryset):
        for operation in queryset:
            try:
                operation.annuler()
                messages.success(request, f"Entrée #{operation.pk} annulée.")
            except ValidationError as e:
                messages.error(request, f"Entrée #{operation.pk} : {e.message}")
            except Exception as e:
                messages.error(request, f"Entrée #{operation.pk} : {str(e)}")


@admin.register(OperationStockSortie)
class OperationStockSortieAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "employe", "statut", "date_operation")
    list_filter = ("statut", "date_operation")
    search_fields = ("client__nom", "employe__username")
    inlines = [LigneOperationInline]
    fields = ("employe", "client", "statut")
    readonly_fields = ("statut",)
    actions = ("valider_operations", "annuler_operations")

    @admin.action(description="Valider les sorties sélectionnées")
    def valider_operations(self, request, queryset):
        for operation in queryset:
            try:
                operation.valider()
                messages.success(request, f"Sortie #{operation.pk} validée.")
            except ValidationError as e:
                messages.error(request, f"Sortie #{operation.pk} : {e.message}")
            except Exception as e:
                messages.error(request, f"Sortie #{operation.pk} : {str(e)}")

    @admin.action(description="Annuler les sorties sélectionnées")
    def annuler_operations(self, request, queryset):
        for operation in queryset:
            try:
                operation.annuler()
                messages.success(request, f"Sortie #{operation.pk} annulée.")
            except ValidationError as e:
                messages.error(request, f"Sortie #{operation.pk} : {e.message}")
            except Exception as e:
                messages.error(request, f"Sortie #{operation.pk} : {str(e)}")


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
    search_fields = ("produit__nom", "produit__reference")
    readonly_fields = (
        "operation",
        "ligne_operation",
        "produit",
        "type_mouvement",
        "date_mouvement",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_quantite(self, obj):
        return obj.ligne_operation.quantite

    get_quantite.short_description = "Quantité"
