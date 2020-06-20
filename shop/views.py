from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from shop.forms import *
from shop.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

from django.core.serializers import serialize
# Create your views here.

@login_required
def index(request):
    produit = Produit.objects.all()
    if request.is_ajax() and request.method == 'GET':
        pk = request.GET.get("id", None)
        if  Produit.objects.filter(id = pk).exists():
            produit = Produit.objects.get(pk=pk)
            return JsonResponse({"prix":produit.prixVente}, status=200)
        else:
            # if nick_name not found, then user can create a new friend.
            return JsonResponse({"valid": True}, status=200)

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

# @login_required
# def updateCategorie(request, id=None):
#
#     modif= get_object_or_404(Categorie, id=id)
#     catForm = CategorieForm(request.POST or None, instance=modif)
#     if catForm.is_valid():
#         modif = catForm.save(commit=False)
#         modif.save()
#         catForm = CategorieForm
#         return redirect(categorie)
#     return render(request, 'shop/produit.html', locals())

@login_required
def modifCateg(request, id):
    if request.method == "POST":
        modif = Categorie.objects.get(id=id)
        categorie_new = Categorie.objects.filter(libelleCate=modif)[0]
        categorie_new.libelleCate=request.POST.get('libellecateg')

        categorie_new.save()
        messages.add_message(request, messages.INFO, 'Votre catégorie a été modifiée avec succès')
        return redirect('addProduit')
    else:
        modif = get_object_or_404(Categorie, pk=id)
        return render(request,'shop/modification.html' , locals())


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
def vente(request):
    if request.method == 'POST':
        fac = request.POST.get('formulaire')
        data = json.loads(fac)
        guichet= data['caisse']

        client     =data.get('caisse')[0].get('client')
        reduction  = data.get('caisse')[0].get('remise')
        remi       = data.get('caisse')[0].get('remi')
        total      = data.get('caisse')[0].get('total')
        totalaPaye = data.get('caisse')[0].get('totalPaye')
        print(client,reduction,remi,total,totalaPaye)

        new = Vente.objects.create(
            SomRemise   =client,
            remise      =reduction,
            totalPaye   =totalaPaye,
            totalFactur =total,
            monnaiRemise=remi
        )
        #print(new)
        facture = Facture()

        for val in data['produit']:
            libelle=val.get('libelleprod')
            qte=val.get('quantite')
            pu=val.get('prix')
            pk=val.get('id')
            print(libelle,qte,pu,pk)

            pro = Produit.objects.get(id=pk)

            facture.qteAchete = qte
            facture.produitId = pro
            facture.venteId   = new
        facture.save()

        print(data)
    return render(request, 'shop/facture.html', locals())

#################les views qui permettent de traité la page du magasinier#############################
@login_required
def index2(request):
    cate = Categorie.objects.all()
    categori = Categorie.objects.all()
    produit = Produit.objects.all()
    entre = Entre.objects.all()
    if request.method == 'POST':
        catform = CategorieForm(request.POST)
        if catform.is_valid():
            catform.save()
            messages.add_message(request, messages.INFO, 'Catégorie bien enregistrer')
        else:
            return redirect(categorie)
    else:
        catform = CategorieForm

    return render(request, 'shop/produit2.html', locals())

@login_required
def modifCateg2(request, id):
    if request.method == "POST":
        modif = Categorie.objects.get(id=id)
        categorie_new = Categorie.objects.filter(libelleCate=modif)[0]
        categorie_new.libelleCate=request.POST.get('libellecateg')

        categorie_new.save()
        messages.add_message(request, messages.INFO, 'Votre catégorie a été modifiée avec succès')
        return redirect('index2')
    else:
        modif = get_object_or_404(Categorie, pk=id)
        return render(request,'shop/modification2.html' , locals())


@login_required
def produit2(request):

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
    return render(request, 'shop/produit2.html', locals())


@login_required
def entreStock2(request):
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
    return render(request, 'shop/produit2.html', locals())

@login_required
def fournisseurs(request):
    if request.method == 'POST':
        name = request.POST.get('Nfour')
        prenom = request.POST.get('Pfour')
        adr = request.POST.get('adrfour')
        phone = request.POST.get('tel')
        email = request.POST.get('mail')

        enregFournisseur = Fournisseur(
            nomF=name,
            prenomF=prenom,
            adresseF=adr,
            telephone=phone,
            mail=email,
        )

        enregFournisseur.save()
        messages.add_message(request, messages.INFO, 'Le fournisseur a été enregistrée avec succès')
        return redirect('addFournisseur')
    else:
        formAlerte = FournisseurForm
    return render(request, 'shop/fournisseur.html', locals())

############## les views qui permettent de traiter les pages de la caissiere#####################

@login_required
def index1(request):
    produit = Produit.objects.all()
    if request.is_ajax() and request.method == 'GET':
        pk = request.GET.get("id", None)
        if  Produit.objects.filter(id = pk).exists():
            produit = Produit.objects.get(pk=pk)
            return JsonResponse({"prix":produit.prixVente}, status=200)
        else:
            # if nick_name not found, then user can create a new friend.
            return JsonResponse({"valid": True}, status=200)

    return render(request, 'shop/accueil1.html', locals())

@login_required
def vente1(request):
    if request.method == 'POST':
        fac = request.POST.get('formulaire')
        data = json.loads(fac)
        guichet= data['caisse']

        client     =data.get('caisse')[0].get('client')
        reduction  = data.get('caisse')[0].get('remise')
        remi       = data.get('caisse')[0].get('remi')
        total      = data.get('caisse')[0].get('total')
        totalaPaye = data.get('caisse')[0].get('totalPaye')
        print(client,reduction,remi,total,totalaPaye)

        new = Vente.objects.create(
            SomRemise   =client,
            remise      =reduction,
            totalPaye   =totalaPaye,
            totalFactur =total,
            monnaiRemise=remi
        )
        #print(new)
        facture = Facture()

        for val in data['produit']:
            libelle=val.get('libelleprod')
            qte=val.get('quantite')
            pu=val.get('prix')
            pk=val.get('id')
            print(libelle,qte,pu,pk)

            pro = Produit.objects.get(id=pk)

            facture.qteAchete = qte
            facture.produitId = pro
            facture.venteId   = new
        facture.save()

        print(data)
    return render(request, 'shop/facture1.html', locals())



