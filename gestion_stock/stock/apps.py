from django.apps import AppConfig

class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stock'
    
    # Si tu as besoin d'importer des signaux plus tard, 
    # fais-le ici dans une méthode ready() :
    # def ready(self):
    #     import stock.signals