from django import forms
from BLOG.models import Article, Commentaire


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["titre", "couverture", "resume", "contenu", "categorie_id", "tag_ids"]



class CommentaireForm(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ["contenu"]