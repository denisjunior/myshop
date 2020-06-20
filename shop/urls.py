from django.urls import path
from . import views

urlpatterns = [
    path('accueil/', views.index, name='index'),
    path('categorie/', views.categorie, name='addCategorie'),
    path('produit/', views.produits, name='addProduit'),
    path('modifica/<int:id>/', views.modifCateg, name='modification'),
    path('entre/', views.entreStock, name='addEntre'),
    path('addVente/', views.vente, name='saveVente'),

    #url pour la caissière
    path('accueil_caissiere/', views.index1, name='index1'),
    path('saveVente/', views.vente1, name='saveVente1'),

    #url pour le magasinier
    path('accueil_magasinier/', views.index2, name='index2'),
    path('modifica/<int:id>/', views.modifCateg2, name='modifi'),
    path('stock/produit/', views.produit2, name='produit2'),
    path('addStock/', views.entreStock2, name='addEntre2'),

    path('addFournisseur/', views.fournisseurs, name='fournisseur'),
    # path('categorie/update/<int:id>/', views.updateCategorie, name='updateCategorie'),
]
