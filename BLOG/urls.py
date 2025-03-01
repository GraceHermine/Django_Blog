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
    path('soumettre/', views.submit_article, name='soumettre_article'),
    path('update/<int:article_id>/', views.update_article, name='update_article'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),
]
