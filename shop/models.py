from django.db import models

# Create your models here.

class Categorie(models.Model):
    libelleCate = models.CharField(max_length=100)

    def __str__(self):
        return self.libelleCate

class Produit(models.Model):
    libelleProd  = models.CharField(max_length=100)
    quantite     = models.IntegerField(default=None)
    prixAchat    = models.IntegerField(default=None)
    prixVente    = models.IntegerField(default=None)
    stock        = models.IntegerField(default=None)
    description  = models.CharField(max_length=150)
    cateProd     = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.libelleProd
class Fournisseur(models.Model):
    nomF         = models.CharField(max_length=100)
    prenomF      = models.CharField(max_length=100)
    adresseF     = models.CharField(max_length=50)
    telephone    = models.IntegerField(default=None)
    mail         = models.EmailField(max_length=150,default=True)
    def __str__(self):
        return self.nomF

class Entre(models.Model):
    qtE          = models.IntegerField(default=None)
    dateE        = models.DateField(auto_now=True)
    prodE        = models.ForeignKey(Produit, on_delete=models.CASCADE)

    def __str__(self):
        return self.dateE

class Sorti(models.Model):
    qtS = models.IntegerField(default=None)
    prixS = models.IntegerField(default=None)
    dateS = models.DateField(null=True)
    prodS = models.ForeignKey(Produit, on_delete=models.CASCADE)
    fourS = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)

    def __str__(self):
        return self.dateS

class Client(models.Model):
    nomClient    = models.CharField(max_length=100)
    prenomClient = models.CharField(max_length=100)
    numeroClient = models.IntegerField(default=None)

    def __str__(self):
        return self.nomClient

class Vente(models.Model):
    dateVente  = models.DateField(null=True)
    prod       = models.ForeignKey(Produit, on_delete=models.CASCADE)
    clt        = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.dateVente


