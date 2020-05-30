from django.shortcuts import render, redirect, get_object_or_404
from shop.forms import *
from shop.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    produit = Produit.objects.all()
    return render(request, 'shop/accueil.html', locals())

# CRUD CATEGORIES
@login_required
def categorie(request):

    cate = Categorie.objects.all()
    categori = Categorie.objects.all()
    produit = Produit.objects.all()
    entre   = Entre.objects.all()
    if request.method == 'POST':
        catform = CategorieForm(request.POST)
        if catform.is_valid():
            catform.save()
            messages.add_message(request, messages.INFO, 'Catégorie bien enregistrer')
        else:
            return redirect(categorie)
    else:
        catform = CategorieForm

    return render(request, 'shop/produit.html', locals())

@login_required
def updateCategorie(request, id=None):
    modif = get_object_or_404(Categorie, id=id)
    cat = Categorie.objects.all()
    if request.method == 'GET':
        update = True
        return render(request, 'shop/produit.html', locals())
    else:
        catForm = CategorieForm(request.POST or None, instance=modif)
        if catForm.is_valid():
            modif = catForm.save(commit=False)
            modif.save()
        return redirect(categorie)

# CRUD PRODUITS
@login_required
def produits(request):

    cate = Categorie.objects.all()
    categori = Categorie.objects.all()
    produit = Produit.objects.all()
    entre = Entre.objects.all()

    if request.method == 'POST':
        libelle = request.POST.get('libelleProd')
        desc = request.POST.get('description')
        qte = request.POST.get('quantite')
        prixA = request.POST.get('prixAchat')
        prixV = request.POST.get('prixVente')
        stockMin = request.POST.get('stock')
        lacateg = request.POST.get('cateProd')

        createprod = Produit.objects.create(libelleProd  = libelle,
                                             description = desc,
                                             quantite    = qte,
                                             prixAchat   = prixA,
                                             prixVente   = prixV,
                                             stock       = stockMin,
                                             cateProd    = Categorie.objects.get(id=lacateg) )
    return render(request, 'shop/produit.html', locals())

@login_required
def entreStock(request):
    cate = Categorie.objects.all()
    categori = Categorie.objects.all()
    produit = Produit.objects.all()
    entre = Entre.objects.all()

    if request.method == 'POST':
        lib = request.POST.get('prodE')
        quantite  = request.POST.get('qtE')

        createEntre = Entre.objects.create(qtE= quantite,

                                           prodE= Produit.objects.get(id=lib),
                                           )
    return render(request, 'shop/produit.html', locals())