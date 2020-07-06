from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from shop.forms import *
from shop.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.db.models import F
from datetime import date
from django.contrib.auth.models import User, Group

from django.core.serializers import serialize
# Create your views here.

@login_required
def index(request):
    produit = Produit.objects.all()
    if request.is_ajax() and request.method == 'GET':
        pk = request.GET.get("id", None)
        if  Produit.objects.filter(id = pk).exists():
            produit = Produit.objects.get(pk=pk)
            return JsonResponse({"price":produit.prixVente,"quantite":produit.quantite}, status=200)
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
    fournisseurs = Fournisseur.objects.all()
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

@login_required
def update_produits(request, id):
    categories = Categorie.objects.all()
    fournisseurs= Fournisseur.objects.all()
    produit     = Produit.objects.get(id=id)
    if request.method == "POST":
        produit_form = ProduitForm(request.POST, instance=produit)

        if produit_form.is_valid():
            produit_form.save()
            messages.success(request, 'Modification effectuer avec succès')
            return redirect(produits)
        else:
            return HttpResponse(produit_form.errors.as_json())
    return render(request, 'shop/modifProd.html', locals())

@login_required
def update_entres(request, id):
    entre = Entre.objects.get(id=id)
    if request.method == "POST":
        entre_form = EntreForm(request.POST, instance=entre)

        if entre_form.is_valid():
            entre_form.save()
            messages.success(request, 'Modification effectuer avec succès')
            return redirect(entreStock)
        else:
            return HttpResponse(entre_form.errors.as_json())
    return render(request, 'shop/modifEntre.html', locals())
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

# CRUD PRODUITS
@login_required
def produits(request):
    cate         = Categorie.objects.all()
    categori     = Categorie.objects.all()
    produit      = Produit.objects.all()
    entre        = Entre.objects.all()
    fournisseurs = Fournisseur.objects.all()

    if request.method == 'POST':
        libelle = request.POST.get('libelleProd')
        desc = request.POST.get('description')
        qte = request.POST.get('quantite')
        prixA = request.POST.get('prixAchat')
        prixV = request.POST.get('prixVente')
        stockMin = request.POST.get('stock')
        lacateg = request.POST.get('cateProd')
        four    = request.POST.get('fournisseur')

        createprod = Produit.objects.create(libelleProd  = libelle,
                                            description = desc,
                                            quantite    = qte,
                                            prixAchat   = prixA,
                                            prixVente   = prixV,
                                            stock       = stockMin,
                                            cateProd    = Categorie.objects.get(id=lacateg),
                                            fournisseur = Fournisseur.objects.get(id=four)
                                            )
    return render(request, 'shop/produit.html', locals())


@login_required
def entreStock(request):
    cate = Categorie.objects.all()
    categori = Categorie.objects.all()
    produit = Produit.objects.all()
    entre = Entre.objects.all()
    fournisseurs = Fournisseur.objects.all()

    if request.method == 'POST':
        lib = request.POST.get('prodE')
        quantity  = request.POST.get('qtE')
        val = Produit.objects.get(id=lib)
        qt  = val.quantite

        createEntre = Entre.objects.create(qtE= quantity,
                                           prodE= Produit.objects.get(id=lib),
                                           qtAvant= qt,
                                           )

        new = Produit.objects.get(id=lib)
        new.quantite = F('quantite') + int(quantity)
        new.save()


    return render(request, 'shop/produit.html', locals())
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
        return redirect(fournisseurs)
    else:
        formAlerte = FournisseurForm
    return render(request, 'shop/fournisseur.html', locals())


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
        print(data['produit'])

        new = Vente.objects.create(
            SomRemise   =client,
            remise      =reduction,
            totalPaye   =totalaPaye,
            totalFactur =total,
            monnaiRemise=remi
        )
        #print(new)
        facture = Facture.objects.create(
            venteId=new
        )
        facture.save()
        ventetotal = facture.venteId.totalFactur
        statgain =0

        for val in data['produit']:
            libelle     = val.get('libelleprod')
            qte         = val.get('quantite')
            pu          = val.get('prix')
            pk          = val.get('id')
            print(libelle, qte, pu, pk)
            pro         = Produit.objects.get(id=pk)
            pro.quantite = F('quantite') - int(qte)
            pro.save()

            prixprod  = (int(qte)*pu)
            prixunitaire= pro.prixAchat

            totalgain = (prixprod  - int(qte)*prixunitaire)
            facligne    = Facture_Ligne.objects.create(
                qteAchete = qte,
                produitId = pro,
                prix      = prixprod,
                gain      = totalgain,
                factureId = Facture.objects.get(id=facture)
            )
            facligne.save()

            statgain +=totalgain

        stat = Statistique.objects.create(
            totalgain   = statgain,
            totalvente  = ventetotal,
            facturestat = Facture.objects.get(id=facture)
        )
        stat.save()

        fact = Facture.objects.get(id=facture)
        dateEmi = fact.dateFacture
        numero = fact.id
        total = fact.venteId.totalFactur
        remi = fact.venteId.remise
        editeFact = Facture_Ligne.objects.filter(factureId_id=facture)

        print(data)
    return render(request, 'shop/facture.html', locals())

@login_required
def detailFact(request, id):
    modif = get_object_or_404(Facture, id=id)
    listfacture = Facture_Ligne.objects.filter(factureId_id=id)

    return render(request, 'shop/detailFacture.html', locals())
@login_required
def fournisseur_list(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'shop/listeFournisseur.html', locals())

@login_required
def facture(request):
    lafacture   = Facture.objects.all()
    return render(request, 'shop/listeFacture.html', locals())
@login_required
def inventaire(request):
    entre = Entre.objects.all()
    return render(request, 'shop/inventaire.html', locals())
@login_required
def delete_categorie(request, id):
    element = Categorie.objects.get(id=id)
    element.etatC = True
    element.save()
    return redirect(categorie)
@login_required
def delete_produit(request, id):
    element = Produit.objects.get(id=id)
    element.etatP = True
    element.save()
    return redirect(produits)
@login_required
def delete_entre(request, id):
    element = Entre.objects.get(id=id)
    element.etatE = True
    element.save()
    return redirect(entreStock)

@login_required
def add_user(request):
    groupe = Group.objects.all()
    users   = User.objects.all()

    if request.method == 'POST':
        formUser = UserForm(request.POST)
        if formUser.is_valid():
            formUser.save()
            messages.add_message(request, messages.INFO, 'utilisateur enregistré avec succès')
        else:
            return redirect(add_user)
    else:
        formUser = UserForm
    return render(request, 'shop/utilisateurs.html', locals())
#################les views qui permettent de traité la page du magasinier#############################
@login_required
def index2(request):
    cate = Categorie.objects.all()
    categori = Categorie.objects.all()
    produit = Produit.objects.all()
    entre = Entre.objects.all()
    fournisseurs = Fournisseur.objects.all()
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
def update_produit2(request, id):
    categories = Categorie.objects.all()
    fournisseurs= Fournisseur.objects.all()
    produit     = Produit.objects.get(id=id)
    if request.method == "POST":
        produit_form = ProduitForm(request.POST, instance=produit)

        if produit_form.is_valid():
            produit_form.save()
            messages.success(request, 'Modification effectuer avec succès')
            return redirect(produit2)
        else:
            return HttpResponse(produit_form.errors.as_json())
    return render(request, 'shop/modifProd2.html', locals())

@login_required
def update_entre2(request, id):
    entre = Entre.objects.get(id=id)
    if request.method == "POST":
        entre_form = EntreForm(request.POST, instance=entre)

        if entre_form.is_valid():
            entre_form.save()
            messages.success(request, 'Modification effectuer avec succès')
            return redirect(entreStock2)
        else:
            return HttpResponse(entre_form.errors.as_json())
    return render(request, 'shop/modifEntre2.html', locals())

@login_required
def produit2(request):

    cate = Categorie.objects.all()
    categori = Categorie.objects.all()
    produit = Produit.objects.all()
    entre = Entre.objects.all()
    fournisseurs = Fournisseur.objects.all()

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
    fournisseurs = Fournisseur.objects.all()

    if request.method == 'POST':
        lib = request.POST.get('prodE')
        quantite  = request.POST.get('qtE')

        createEntre = Entre.objects.create(qtE= quantite,

                                           prodE= Produit.objects.get(id=lib),
                                           )
    return render(request, 'shop/produit2.html', locals())

@login_required
def fournisseurs2(request):
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
        return redirect(fournisseurs2)
    else:
        formAlerte = FournisseurForm
    return render(request, 'shop/fournisseur2.html', locals())

@login_required
def fournisseur_list2(request):
    fournisseurs = Fournisseur.objects.all()
    return render(request, 'shop/listeFournisseur2.html', locals())

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
        guichet = data['caisse']

        client = data.get('caisse')[0].get('client')
        reduction = data.get('caisse')[0].get('remise')
        remi = data.get('caisse')[0].get('remi')
        total = data.get('caisse')[0].get('total')
        totalaPaye = data.get('caisse')[0].get('totalPaye')
        print(client, reduction, remi, total, totalaPaye)
        print(data['produit'])

        new = Vente.objects.create(
            SomRemise=client,
            remise=reduction,
            totalPaye=totalaPaye,
            totalFactur=total,
            monnaiRemise=remi
        )
        # print(new)
        facture = Facture.objects.create(
            venteId=new
        )
        facture.save()
        ventetotal = facture.venteId.totalFactur
        statgain = 0

        for val in data['produit']:
            libelle = val.get('libelleprod')
            qte = val.get('quantite')
            pu = val.get('prix')
            pk = val.get('id')
            print(libelle, qte, pu, pk)
            pro = Produit.objects.get(id=pk)
            pro.quantite = F('quantite') - int(qte)
            pro.save()

            prixprod = (int(qte) * pu)
            prixunitaire = pro.prixAchat

            totalgain = (prixprod - int(qte) * prixunitaire)
            facligne = Facture_Ligne.objects.create(
                qteAchete=qte,
                produitId=pro,
                prix=prixprod,
                gain=totalgain,
                factureId=Facture.objects.get(id=facture)
            )
            facligne.save()

            statgain += totalgain

        stat = Statistique.objects.create(
            totalgain=statgain,
            totalvente=ventetotal,
            facturestat=Facture.objects.get(id=facture)
        )
        stat.save()

        fact = Facture.objects.get(id=facture)
        dateEmi = fact.dateFacture
        numero = fact.id
        total = fact.venteId.totalFactur
        remi = fact.venteId.remise
        editeFact = Facture_Ligne.objects.filter(factureId_id=facture)

        print(data)
    return render(request, 'shop/facture1.html', locals())

@login_required
def detailFact1(request, id):
    modif = get_object_or_404(Facture, id=id)
    listfacture = Facture_Ligne.objects.filter(factureId_id=id)

    return render(request, 'shop/detailFacture1.html', locals())

#### liste des factures ##########
@login_required
def facture1(request):
    lafacture   = Facture.objects.all()
    return render(request, 'shop/listeFacture1.html', locals())
#########################################################################

@login_required
def stats(request):
    totalg=0
    totalv=0

    statistiques = Statistique.objects.filter(dateF=date.today())
    for facts in statistiques:
        totalg += facts.totalgain
        totalv  += facts.totalvente
        facts.save()

    return render(request, 'shop/statistique.html', locals())



