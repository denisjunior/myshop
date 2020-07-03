from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Categorie(models.Model):
    libelleCate = models.CharField(max_length=100)
    etatC       = models.BooleanField(null=True)

    def __str__(self):
        return self.libelleCate
class TypeUser(models.Model):
    libelle     = models.CharField(max_length=100)
    userId      = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.libelle

class Fournisseur(models.Model):
    nomF         = models.CharField(max_length=100)
    prenomF      = models.CharField(max_length=100)
    adresseF     = models.CharField(max_length=50)
    telephone    = models.IntegerField(default=None)
    mail         = models.EmailField(max_length=150,default=True)
    def __str__(self):
        return self.nomF

class Produit(models.Model):
    libelleProd  = models.CharField(max_length=100)
    quantite     = models.IntegerField(default=None)
    prixAchat    = models.FloatField(default=None)
    prixVente    = models.FloatField(default=None)
    stock        = models.IntegerField(default=None)
    description  = models.CharField(max_length=150)
    cateProd     = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    fournisseur  = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)
    etatP        = models.BooleanField(null=True)

    def __str__(self):
        return self.libelleProd

class Entre(models.Model):
    qtE          = models.IntegerField(default=None)
    qtAvant      = models.IntegerField(default=None)
    dateE        = models.DateField(auto_now=True)
    prodE        = models.ForeignKey(Produit, on_delete=models.CASCADE)
    etatE        = models.BooleanField(null=True)

    def __int__(self):
        return self.qtE

class Client(models.Model):
    nomClient    = models.CharField(max_length=100)
    prenomClient = models.CharField(max_length=100)
    numeroClient = models.IntegerField(default=None)

    def __str__(self):
        return self.nomClient

class Vente(models.Model):
    dateVente  = models.DateField(auto_now=True)
    remise     = models.FloatField(default=None)
    totalPaye  = models.FloatField(default=None)
    totalFactur= models.FloatField(default=None)
    SomRemise  = models.FloatField(default=None)
    monnaiRemise= models.FloatField(default=None)

    def __float__(self):
        return self.totalFactur

class Facture(models.Model):
    dateFacture   = models.DateField(auto_now=True)
    venteId       = models.ForeignKey(Vente, on_delete=models.CASCADE)
    totalG        = models.FloatField(null=True)
    totalV        = models.FloatField(null=True)


    def __int__(self):
        return self.id

class Facture_Ligne(models.Model):
    datefac = models.DateField(auto_now=True)
    produitId   = models.ForeignKey(Produit, on_delete=models.CASCADE)
    qteAchete   = models.IntegerField(default=None)
    prix        = models.FloatField(default=None)
    gain        = models.FloatField(default=None)
    factureId   = models.ForeignKey(Facture, on_delete=models.CASCADE)

    def __int__(self):
        return self.qteAchete

class Statistique(models.Model):
    dateF       = models.DateField(auto_now=True)
    totalgain   = models.FloatField(default=None)
    totalvente  = models.FloatField(null=True)
    facturestat = models.ForeignKey(Facture, on_delete=models.CASCADE)






