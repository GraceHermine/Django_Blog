from django import forms
from .models import Article  

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'couverture', 'tag_ids', 'resume']  
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre de l\'article'}),
            'resume': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Résumé'}),
            'contenu': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Contenu'}),
            'tag_ids': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'couverture': forms.FileInput(attrs={'class': 'form-control'}),
        }
