from django.contrib import admin
from .models import (
    Etablissement, Programme, Activite, SousActivite,
    Produit, PCOP, LigneBudgetaire, Profil, DemandeReinitialisation,
    PTA, ActivitePTA,
    Salle, Filiere, Matiere, CreneauHoraire, EmploiDuTemps
)


@admin.register(Etablissement)
class EtablissementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type_etablissement', 'district', 'actif')
    list_filter = ('type_etablissement', 'district', 'actif')
    search_fields = ('nom', 'district')


@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('code', 'libelle')
    search_fields = ('code', 'libelle')


@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'programme')
    list_filter = ('programme',)
    search_fields = ('libelle',)


@admin.register(SousActivite)
class SousActiviteAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'activite')
    list_filter = ('activite',)
    search_fields = ('libelle',)


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'sous_activite', 'unite', 'cible')
    list_filter = ('unite',)
    search_fields = ('libelle',)


@admin.register(PCOP)
class PCOPAdmin(admin.ModelAdmin):
    list_display = ('code', 'libelle')
    search_fields = ('code', 'libelle')


@admin.register(LigneBudgetaire)
class LigneBudgetaireAdmin(admin.ModelAdmin):
    list_display = ('etablissement', 'produit', 'source_financement', 'montant_prevu', 'montant_realise', 'statut')
    list_filter = ('source_financement', 'statut', 'etablissement')
    search_fields = ('produit__libelle', 'etablissement__nom')
    date_hierarchy = 'date_creation'


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'role', 'etablissement')
    list_filter = ('role', 'etablissement')
    search_fields = ('utilisateur__username',)


@admin.register(DemandeReinitialisation)
class DemandeReinitialisationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'statut', 'date_demande', 'date_traitement')
    list_filter = ('statut', 'date_demande')
    search_fields = ('utilisateur__username', 'email_contact')
    readonly_fields = ('date_demande', 'date_traitement')
    actions = ['reinitialiser_mot_de_passe']
    
    def reinitialiser_mot_de_passe(self, request, queryset):
        from django.utils.crypto import get_random_string
        from django.utils import timezone
        count = 0
        for demande in queryset.filter(statut='En attente'):
            nouveau_mdp = 'Dretfp' + get_random_string(6)
            user = demande.utilisateur
            user.set_password(nouveau_mdp)
            user.save()
            demande.nouveau_mot_de_passe = nouveau_mdp
            demande.statut = 'Traitee'
            demande.date_traitement = timezone.now()
            demande.save()
            count += 1
        self.message_user(request, f"{count} mot(s) de passe reinitialise(s).")
    
    reinitialiser_mot_de_passe.short_description = "Reinitialiser le mot de passe"


@admin.register(PTA)
class PTAAdmin(admin.ModelAdmin):
    list_display = ('etablissement', 'annee', 'titre', 'statut', 'responsable', 'date_creation')
    list_filter = ('annee', 'statut', 'etablissement')
    search_fields = ('titre', 'etablissement__nom', 'responsable')
    date_hierarchy = 'date_creation'


@admin.register(ActivitePTA)
class ActivitePTAAdmin(admin.ModelAdmin):
    list_display = ('titre', 'PTA', 'statut', 'taux_avancement', 'responsable', 'date_debut', 'date_fin')
    list_filter = ('statut', 'PTA__annee', 'PTA__etablissement')
    search_fields = ('titre', 'responsable')
    list_editable = ('statut', 'taux_avancement')


@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'etablissement', 'capacite', 'type_salle', 'actif')
    list_filter = ('etablissement', 'actif', 'type_salle')
    search_fields = ('nom', 'batiment')


@admin.register(Filiere)
class FiliereAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'etablissement', 'niveau', 'nb_apprenants', 'actif')
    list_filter = ('etablissement', 'niveau', 'actif')
    search_fields = ('code', 'nom')


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'filiere', 'type_matiere', 'heures_total', 'coefficient', 'actif')
    list_filter = ('filiere', 'type_matiere', 'actif')
    search_fields = ('code', 'nom')


@admin.register(CreneauHoraire)
class CreneauHoraireAdmin(admin.ModelAdmin):
    list_display = ('nom', 'heure_debut', 'heure_fin', 'ordre')
    list_editable = ('ordre',)
    ordering = ('ordre',)


@admin.register(EmploiDuTemps)
class EmploiDuTempsAdmin(admin.ModelAdmin):
    list_display = ('filiere', 'jour', 'creneau', 'matiere', 'salle', 'formateur', 'annee_scolaire')
    list_filter = ('jour', 'annee_scolaire', 'filiere__etablissement', 'creneau')
    search_fields = ('matiere', 'filiere__code', 'filiere__nom')