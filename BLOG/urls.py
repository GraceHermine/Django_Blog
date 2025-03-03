from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("blog/", views.blog, name="blog"),
    path("<slug:slug>", views.blog_single, name="blog-single"),
    path("about/", views.about, name="about"),
    path('comment/update/<int:comment_id>/', views.update_comment, name='update_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path("ajouter-article/", views.ajouter_article, name='ajouter_article'),
    path("mes-articles/", views.mes_articles, name='mes_articles'),
    path("modifier-article/<int:article_id>/", views.modifier_article, name='modifier_article'),
    path("supprimer-article/<int:article_id>/", views.supprimer_article, name='supprimer_article'),
]
