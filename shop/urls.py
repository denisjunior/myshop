from django.urls import path
from . import views

urlpatterns = [
    path('accueil/', views.index, name='index'),
    path('categorie/', views.categorie, name='addCategorie'),
    path('produit/', views.produits, name='addProduit'),
    path('entre/', views.entreStock, name='addEntre'),
    path('update/', views.updateCategorie, name='updateCategorie'),

]
