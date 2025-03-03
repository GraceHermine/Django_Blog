from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django import forms
from django_ckeditor_5.fields import CKEditor5Field



User = get_user_model()
# Create your models here.
class Categorie(models.Model):

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    nom = models.CharField(verbose_name="Nom", max_length=255)
    description = models.TextField()

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    nom = models.CharField(verbose_name="Nom", max_length=255)
    
    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Article(models.Model):

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    titre = models.CharField(max_length=256)
    couverture = models.ImageField(upload_to="articles")
    resume = models.TextField()
    contenu = CKEditor5Field('Text', config_name='extends')
   
    slug = models.SlugField(unique=True, blank=True, null=True)

    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    auteur_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="auteur_article_ids")
    categorie_id = models.ForeignKey('BLOG.Categorie', on_delete=models.SET_NULL, null=True, related_name="auteur_article_ids", verbose_name="Catégories")
    tag_ids = models.ManyToManyField('BLOG.Tag', related_name="tag_article_ids", verbose_name="Tags")
    est_pulie = models.BooleanField(default=True)
    date_de_publication = models.DateField(auto_now=True)
    

    #La méthode save est une méthode intégrée dans les modèles
    
#  Django qui est appelée lorsque vous enregistrez un objet
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)



    def __str__(self):
        return self.titre


class Commentaire(models.Model):
    class Meta:
        verbose_name = "commentaire"
        verbose_name_plural = "commentaires"

    auteur_id = models.ForeignKey(User, on_delete= models.SET_NULL, null=True, related_name="auteur_commentaire_ids")
    article_id = models.ForeignKey('BLOG.Article', on_delete= models.CASCADE, related_name="article_commentaire_ids")
    contenu = CKEditor5Field('Text', config_name='extends')

     # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.auteur_id.username


class About(models.Model):

    titre = models.CharField(max_length=255)
    sous_titre = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to="about", blank=True, null=True)

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre
    

class Vission(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    image = models.ImageField(upload_to="vision", blank=True, null=True)
    titre_mission = models.CharField(max_length=255, default="")
    contenu_mission = models.TextField()
    photo = models.ImageField(upload_to="mission", blank=True, null=True)

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre
    

class Team(models.Model):
    nom = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="team")


    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
    
