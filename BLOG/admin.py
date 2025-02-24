from django.contrib import admin
from .models import Categorie, Tag, Commentaire,Article,About,Vission,Team


# Register your models here.
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'statut', 'created_at', 'last_updated_at')

    list_display_links = ['nom',]

    list_filter = ('statut',)

    search_fields = ('nom',)

    ordering = ['nom',]

    list_per_page = 10

    date_hierarchy = 'created_at'

    fieldsets = [
            (
                'Infos', 
                {
                    'fields': ['nom', 'description'],
                },
            ),
            (
                'Standards', 
                {
                    'fields': ['statut', ]
                }
            ),
            ]

    actions = ('active','desactive')

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Categorie, CategorieAdmin)



class TagAdmin(admin.ModelAdmin):
    list_display = ('nom', 'statut', 'created_at', 'last_updated_at')

    list_display_links = ['nom',]

    list_filter = ('statut',)

    search_fields = ('nom',)

    ordering = ['nom',]

    list_per_page = 5

    date_hierarchy = 'created_at'

    actions = ('active','desactive')

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Tag,TagAdmin)



class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'statut','auteur_id', 'created_at', 'last_updated_at', 'est_pulie', 'date_de_publication')
    list_display_links = ['titre',]
    list_filter = ('est_pulie', 'categorie_id','tag_ids',)

    search_fields = ('titre',)

    ordering = ['titre',]

    list_per_page = 5

    filter_horizontal = ('tag_ids',)

    date_hierarchy = 'date_de_publication'

    actions = ('active','desactive')

    def active(self,request,queryset):
        queryset.update(statut=True)
        self.message_user(request, 'La selection a été activé avec succès')
    active.short_description = 'Activer'

    def desactive(self, request, queryset):
        queryset.update(statut=False)
        self.message_user(request, 'La sélection a été désactiver avec succès')
    desactive.short_description = 'Desactiver'

def _register(model, admin_class):
    admin.site.register(model, admin_class)

_register(Article, ArticleAdmin)


class CommentaireAdmin(admin.ModelAdmin):
    list_display = ("auteur_id", "article_id", "created_at", "statut")
    search_fields = ("auteur_id__username", "contenu")
    list_filter = ('statut', 'created_at')
    date_hierarchy = 'created_at'
    ordering = ['created_at',]

_register(Commentaire, CommentaireAdmin)



admin.site.register(About)
admin.site.register(Vission)
admin.site.register(Team)