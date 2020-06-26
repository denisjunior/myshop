from django.contrib import admin
from shop.models import *

admin.site.register(Categorie)
admin.site.register(Produit)
admin.site.register(Fournisseur)
admin.site.register(Vente)
admin.site.register(Entre)
admin.site.register(Client)
admin.site.register(Facture)
admin.site.register(TypeUser)
admin.site.register(Facture_Ligne)

# Register your models here.
