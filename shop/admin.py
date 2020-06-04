from django.contrib import admin
from shop.models import *

admin.site.register(Categorie)
admin.site.register(Produit)
admin.site.register(Fournisseur)
admin.site.register(Vente)
admin.site.register(Entre)
admin.site.register(Sorti)
admin.site.register(Client)

# Register your models here.
