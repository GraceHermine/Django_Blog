
from BLOG.models import Article,Vission,Team,About,Commentaire
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils.text import slugify
from django.http import Http404
from BLOG.forms import CommentaireForm



def index(request):
    articles = Article.objects.filter(est_pulie=True) 
    paginator = Paginator(articles, 3)  
    page_number = request.GET.get('page')  
    page_objet = paginator.get_page(page_number) 
    datas = {
        'active_index' : 'active',
        # 'articles' : articles,
        'page_objet': page_objet, 
    }

    return render(request, 'index.html', datas)

def contact(request):
    datas = {
        'active_contact' : 'active',

    }
    return render (request, 'contact.html', datas)


def blog(request,):
    produits = Article.objects.filter(est_pulie=True)
    datas = {
        'active_blog' : 'active',
        'produits':produits,

    }
    return render (request, 'blog.html', datas)


def blog_single(request, slug):
    articles = Article.objects.filter(slug=slug)  # Utilise filter() pour récupérer un queryset
    form = CommentaireForm()
    if not articles.exists():
        raise Http404("Article not found")  # Si aucun article n'est trouvé 
    article = articles.first()  # Si plusieurs articles existent, on récupère le premier
    # Mettre à jour le slug si le titre a changé
    if article.titre != article.slug:
        article.slug = slugify(article.titre)
        article.save() 

    if request.method == "POST":
        contenu = request.POST["contenu"]
        
        commentaire = Commentaire()
        commentaire.auteur_id = request.user
        commentaire.article_id = article
        commentaire.contenu = contenu
        commentaire.save()

    datas = {
        'active_blog': 'active',
        'article': article,
        'comment_form': form
    }
    
    return render(request, 'blog-single.html', datas)


def about(request):
    datas = {
        'active_about': 'active',
        'about_content' : About.objects.first(),
        'visions' : Vission.objects.all(),
        'team_members' : Team.objects.all(),
        
    }
    return render (request, 'about.html', datas)
# Create your views her:e.
