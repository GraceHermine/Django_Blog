
from BLOG.models import Article,Vission,Team,About,Commentaire,Tag,Categorie
from django.core.paginator import Paginator
from django.utils.text import slugify
from BLOG.forms import CommentaireForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required




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
            return redirect('blog-single', slug=slug)  

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

    # Vérifier si l'utilisateur est l'auteur du commentaire
    if request.user != commentaire.auteur_id:
        return redirect('blog-single', slug=commentaire.article_id.slug)

    if request.method == "POST":
        form = CommentaireForm(request.POST, instance=commentaire)
        if form.is_valid():
            form.save()
            return redirect('blog-single', slug=commentaire.article_id.slug)
    else:
        form = CommentaireForm(instance=commentaire)  # Initialiser le formulaire avec le commentaire existant

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
def ajouter_article(request):
    categories = Categorie.objects.all()
    tags = Tag.objects.all()

    if request.method == "POST":
        titre = request.POST.get("titre")
        couverture = request.FILES.get("couverture")
        resume = request.POST.get("resume")
        contenu = request.POST.get("contenu")
        categorie_id = request.POST.get("categorie")
        tags_ids = request.POST.getlist("tags")
        statut = request.POST.get("statut") == "on"
        date_publication = request.POST.get("date_publication")
        
        categorie = Categorie.objects.get(id=categorie_id) if categorie_id else None
        tags_selected = Tag.objects.filter(id__in=tags_ids)

        article = Article.objects.create(
            titre=titre,
            couverture=couverture,
            resume=resume,
            contenu=contenu,
            slug=slugify(titre),
            statut=statut,
            auteur_id=request.user,
            categorie_id=categorie,
            date_de_publication=date_publication,
        )
        article.tag_ids.set(tags_selected)

        return redirect("index")

    return render(request, "soumettre_article.html", {"categories": categories, "tags": tags})


@login_required
def mes_articles(request):

    articles = Article.objects.filter(auteur_id=request.user).order_by('-created_at')  # Récupère les articles de l'utilisateur connecté
    categories = Categorie.objects.all()
    tags = Tag.objects.all()
    return render(request, "mes_articles.html", {"articles": articles,"categories": categories, "tags": tags})

@login_required
def modifier_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, auteur_id=request.user)

    if request.method == "POST":
        article.titre = request.POST.get("titre")
        article.resume = request.POST.get("resume")
        article.contenu = request.POST.get("contenu")

        # Gestion de l'image (si un nouveau fichier est fourni)
        if "couverture" in request.FILES:
            article.couverture = request.FILES["couverture"]

        # Mise à jour de la catégorie
        categorie_id = request.POST.get("categorie")
        article.categorie_id = Categorie.objects.get(id=categorie_id) if categorie_id else None

        # Mise à jour des tags
        tags_ids = request.POST.getlist("tags")
        article.tag_ids.set(Tag.objects.filter(id__in=tags_ids))

        # Mise à jour du statut de publication
        article.statut = request.POST.get("statut") == "on"

        article.save()
        return redirect("mes_articles")

    return redirect("mes_articles")

@login_required
def supprimer_article(request, article_id):
    article = get_object_or_404(Article, id=article_id, auteur_id=request.user)
    article.delete()
    return redirect("mes_articles")