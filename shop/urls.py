from django.urls import path
from . import views

urlpatterns = [
    #url pour l'administrateur
    path('accueil/', views.index, name='index'),
    path('categorie/', views.categorie, name='addCategorie'),
    path('produit/', views.produits, name='addProduit'),
    path('update/categorie/<int:id>/', views.modifCateg, name='modification'),
    path('update/produit/<int:id>/', views.update_produits, name='update_produit'),
    path('update/provision/<int:id>/', views.update_entres, name='update_entre'),
    path('entre/', views.entreStock, name='addEntre'),
    path('addVente/', views.vente, name='saveVente'),
    path('Fournisseur/', views.fournisseurs, name='addfournisseur'),
    path('facture/detail/<int:id>/', views.detailFact, name='facturedetail'),
    path('fournisseur/liste/', views.fournisseur_list, name='listFournisseur'),
    path('stock/inventaire/', views.inventaire, name='stock'),
    path('delete/categorie/<int:id>/', views.delete_categorie, name='deletecate'),
    path('delete/produit/<int:id>/', views.delete_produit, name='deleteprod'),
    path('delete/approvision/<int:id>/', views.delete_entre, name='deletentre'),
    path('add_user/', views.add_user, name='adduser'),

    ## listes des factures
    path('factures/', views.facture, name='facliste'),

    #url pour la caissière
    path('accueil_caissiere/', views.index1, name='index1'),
    path('saveVente/', views.vente1, name='saveVente1'),
    path('Detailfacture/detail/<int:id>/', views.detailFact1, name='detailfacture1'),
    ## listes des factures
    path('facture/', views.facture1, name='facliste1'),

    #url pour le magasinier
    path('accueil_magasinier/', views.index2, name='index2'),
    path('update_2/categorie/<int:id>/', views.modifCateg2, name='modifi'),
    path('stock/produit/', views.produit2, name='produit2'),
    path('addStock/', views.entreStock2, name='addEntre2'),
    path('fournisseur_liste/', views.fournisseur_list2, name='liste_fournisseur'),
    path('update_2/produit/<int:id>/', views.update_produit2, name='update_produit2'),
    path('update_2/provision/<int:id>/', views.update_entre2, name='update_entre2'),

    path('addFournisseur/', views.fournisseurs2, name='fournisseur'),
    # path('categorie/update/<int:id>/', views.updateCategorie, name='updateCategorie'),

    path('stat/', views.stats, name='states'),
]
