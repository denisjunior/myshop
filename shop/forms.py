from django import forms
from shop.models import *

class FournisseurForm(forms.ModelForm):
    class Meta:
        model=Fournisseur
        fields='__all__'

class CategorieForm(forms.ModelForm):
    class Meta:
        model   = Categorie
        fields  = '__all__'

class ProduitForm(forms.ModelForm):
    class Meta:
        model   = Produit
        fields  = (
            'libelleProd',
            'quantite',
            'prixAchat',
            'prixVente',
            'stock',
            'description',
            'cateProd',
            'fournisseur',
            'etatP'
        )
class EntreForm(forms.ModelForm):
    class Meta:
        model   = Entre
        fields  = 'qtE',