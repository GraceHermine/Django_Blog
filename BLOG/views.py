
from BLOG.models import Article,Vission,Team,About,Commentaire
from django.core.paginator import Paginator
from django.utils.text import slugify
from BLOG.forms import CommentaireForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm



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



# Debut de la partie blog detail
def blog_single(request, slug):
    article = get_object_or_404(Article, slug=slug)
    commentaires = article.article_commentaire_ids.all().order_by('-created_at')  
    form = CommentaireForm()

    if request.method == "POST":
        form = CommentaireForm(request.POST)
        if form.is_valid():
            commentaire = form.save(commit=False)
            commentaire.auteur_id = request.user
            commentaire.article_id = article
            commentaire.save()
            return redirect('blog_single', slug=slug)  

    datas = {
        'active_blog': 'active',
        'article': article,
        'comment_form': form,
        'commentaires': commentaires
    }

    return render(request, 'blog-single.html', datas)

@login_required
def update_comment(request, comment_id):
    commentaire = get_object_or_404(Commentaire, id=comment_id)

    if request.user != commentaire.auteur_id:
        return redirect('blog-single', slug=commentaire.article_id.slug)

    if request.method == "POST":
        form = CommentaireForm(request.POST, instance=commentaire)
        if form.is_valid():
            form.save()
            return redirect('blog-single', slug=commentaire.article_id.slug)

    return render(request, 'update_comment.html', {'form': form, 'commentaire': commentaire})

@login_required
def delete_comment(request, comment_id):
    # Vérifie si le commentaire existe
    try:
        commentaire = Commentaire.objects.get(id=comment_id)
    except Commentaire.DoesNotExist:
        return redirect('blog')  # Redirige si le commentaire n'existe pas

    # Vérifie si l'utilisateur est authentifié et est l'auteur du commentaire
    if not request.user.is_authenticated:
        return redirect('login')  # Rediriger vers la page de connexion si non authentifié

    # Vérifie si l'utilisateur est bien l'auteur du commentaire
    if request.user == commentaire.auteur_id:
        commentaire.delete()

    return redirect('blog-single', slug=commentaire.article_id.slug)

# fin de la partie blog detail
def about(request):
    datas = {
        'active_about': 'active',
        'about_content' : About.objects.first(),
        'visions' : Vission.objects.all(),
        'team_members' : Team.objects.all(),
        
    }
    return render (request, 'about.html', datas)
# Create your views her:e.




# Debut de la partie formulaire des articles

@login_required
def submit_article(request):
    if request.method == "POST":
        form = ArticleForm()
        if form.is_valid():
            form = ArticleForm(request.POST, request.FILES)
            article = form.save(commit=False)
            article.est_pulie = True  
            article.save()
            form.save_m2m() 
            return redirect("blog")  
    else:
        form = ArticleForm()

    return render(request, 'soumettre_article.html', {'form': form})


@login_required
def update_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user == article.auteur:
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                form.save()
                return redirect('blog-single', slug=article.slug)
        else:
            form = ArticleForm(instance=article)

        return render(request, 'blog/update_article.html', {'form': form})
    else:
        return redirect('blog') 
    

@login_required
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.user == article.auteur:
        article.delete()
        return redirect('blog')  
    else:
        return redirect('blog')  
