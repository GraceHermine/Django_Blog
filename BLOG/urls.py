from django.urls import path 

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("contact/", views.contact, name="contact"),
    path("blog/", views.blog, name="blog"),
    path("<slug:slug>", views.blog_single, name="blog-single"),
    path("about/", views.about, name="about"),
    
]
