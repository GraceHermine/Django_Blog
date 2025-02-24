from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from BLOG.models import Article,Vission,Team,About,Formulaire
from django.utils.text import slugify
from django.db.models import Count



def index(request):
    articles = Article.objects.filter(est_pulie=True)  # Filtrer les articles publiés
    pagination = Paginator(articles, 6)  # 6 articles par page
    numero_page = request.GET.get('page')
    page_objet = pagination.get_page(numero_page)

    datas = {
        'active_index': 'active',
        'page_objet': page_objet,
    }

    return render(request, 'index.html', datas)

# def article_detail(request, slug):
#     article = get_object_or_404(Article, slug=slug)  # Utilisation de get_object_or_404
#     return render(request, 'article_detail.html', {'article': article})


def contact(request):
    if request.method == 'POST':
        form = Formulaire(request.POST)
        if form.is_valid():
            form.save()
            nom = form.cleaned_data['nom']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']

            send_mail(
                'Merci pour votre message',
                f'Bonjour {nom},\n\nMerci pour votre message. Nous vous répondrons bientôt.',
                'hermine@monsite.com',
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Merci pour votre message, nous vous répondrons bientôt.')
            return redirect('contact')  
    else:
        form = Formulaire()  

    datas = {
        'active_contact': 'active',
        'form': form,
    }
    return render(request, 'contact.html', datas)


def blog(request,):
    produits = Article.objects.filter(est_pulie=True)
    datas = {
        'active_blog' : 'active',
        'produits':produits,

    }
    return render (request, 'blog.html', datas)


def blog_single(request, slug):
    duplicates = Article.objects.values('slug').annotate(count=Count('slug')).filter(count__gt=1)
    print(duplicates)
    # article =Article.objects.get(pk=pk)
    article = get_object_or_404(Article, slug=slug)
    if article.titre != article.slug:
        article.slug = slugify(article.titre)
        article.save()  # Sauvegarde l'article avec le nouveau slug

    datas = {
        'active_blog' : 'active',
        'article':article,

    }
    return render (request, 'blog-single.html', datas)


def about(request):
    datas = {
        'active_about': 'active',
        'about_content' : About.objects.first(),
        'visions' : Vission.objects.all(),
        'team_members' : Team.objects.all(),
        
    }
    return render (request, 'about.html', datas)
# Create your views her:e.
