# Generated by Django 3.0.6 on 2020-06-18 16:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelleCate', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomClient', models.CharField(max_length=100)),
                ('prenomClient', models.CharField(max_length=100)),
                ('numeroClient', models.IntegerField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Fournisseur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomF', models.CharField(max_length=100)),
                ('prenomF', models.CharField(max_length=100)),
                ('adresseF', models.CharField(max_length=50)),
                ('telephone', models.IntegerField(default=None)),
                ('mail', models.EmailField(default=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateVente', models.DateField(null=True)),
                ('remise', models.FloatField(default=None)),
                ('totalPaye', models.FloatField(default=None)),
                ('totalFactur', models.FloatField(default=None)),
                ('SomRemise', models.FloatField(default=None)),
                ('monnaiRemise', models.FloatField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='TypeUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=100)),
                ('userId', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelleProd', models.CharField(max_length=100)),
                ('quantite', models.IntegerField(default=None)),
                ('prixAchat', models.FloatField(default=None)),
                ('prixVente', models.FloatField(default=None)),
                ('stock', models.IntegerField(default=None)),
                ('description', models.CharField(max_length=150)),
                ('cateProd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Categorie')),
            ],
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qteAchete', models.IntegerField(default=None)),
                ('produitId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Produit')),
                ('venteId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Vente')),
            ],
        ),
        migrations.CreateModel(
            name='Entre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qtE', models.IntegerField(default=None)),
                ('dateE', models.DateField(auto_now=True)),
                ('prodE', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Produit')),
            ],
        ),
    ]
