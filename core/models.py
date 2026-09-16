from django.db import models
from django.contrib.auth.models import User


# ============================================================
# ETABLISSEMENT
# ============================================================

class Etablissement(models.Model):
    TYPES = [
        ('LTP', 'Lycee Technique et Professionnel'),
        ('CFP', 'Centre de Formation Professionnelle'),
        ('CFPF', 'Centre de Formation Professionnelle et de Formation'),
        ('LTPA', 'Lycee Technique et Professionnel Agricole'),
        ('INPF', 'Institut National de Formation Professionnelle'),
        ('CNFPPSH', 'Centre National de Formation des Personnels'),
    ]
    
    nom = models.CharField(max_length=200, unique=True, verbose_name="Nom")
    type_etablissement = models.CharField(max_length=10, choices=TYPES, verbose_name="Type")
    district = models.CharField(max_length=100, verbose_name="District")
    region = models.CharField(max_length=100, default="Amoron'i Mania", verbose_name="Region")
    responsable = models.CharField(max_length=200, blank=True, verbose_name="Responsable")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Etablissement"
        verbose_name_plural = "Etablissements"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.type_etablissement})"


# ============================================================
# PROGRAMME
# ============================================================

class Programme(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    libelle = models.CharField(max_length=200, verbose_name="Libelle")
    description = models.TextField(blank=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Programme"
        verbose_name_plural = "Programmes"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.libelle}"


# ============================================================
# ACTIVITE
# ============================================================

class Activite(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE, verbose_name="Programme")
    libelle = models.CharField(max_length=300, verbose_name="Libelle")
    objectif = models.TextField(blank=True, verbose_name="Objectif")
    
    class Meta:
        verbose_name = "Activite"
        verbose_name_plural = "Activites"
        ordering = ['programme', 'libelle']
    
    def __str__(self):
        return self.libelle


# ============================================================
# SOUS-ACTIVITE
# ============================================================

class SousActivite(models.Model):
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE, verbose_name="Activite")
    libelle = models.CharField(max_length=300, verbose_name="Libelle")
    
    class Meta:
        verbose_name = "Sous-activite"
        verbose_name_plural = "Sous-activites"
        ordering = ['activite', 'libelle']
    
    def __str__(self):
        return f"{self.activite.libelle} -> {self.libelle}"


# ============================================================
# PRODUIT
# ============================================================

class Produit(models.Model):
    UNITES = [
        ('Nombre', 'Nombre'), ('Pack', 'Pack'), ('Litre', 'Litre'),
        ('Jour', 'Jour'), ('Carte', 'Carte'), ('Piece', 'Piece'),
        ('Sac', 'Sac'), ('m3', 'Metre cube'),
    ]
    
    sous_activite = models.ForeignKey(SousActivite, on_delete=models.CASCADE, verbose_name="Sous-activite")
    libelle = models.CharField(max_length=300, verbose_name="Libelle")
    unite = models.CharField(max_length=20, choices=UNITES, verbose_name="Unite")
    cible = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Cible")
    
    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['sous_activite', 'libelle']
    
    def __str__(self):
        return f"{self.libelle} ({self.cible} {self.unite})"


# ============================================================
# PCOP
# ============================================================

class PCOP(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    libelle = models.CharField(max_length=300, verbose_name="Libelle")
    
    class Meta:
        verbose_name = "Code PCOP"
        verbose_name_plural = "Codes PCOP"
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.libelle}"


# ============================================================
# LIGNE BUDGETAIRE
# ============================================================

class LigneBudgetaire(models.Model):
    SOURCES = [
        ('RPI', 'RPI'), ('FCE', 'FCE'),
        ('UNESCO', 'UNESCO'), ('Partenaire', 'Partenaire'),
    ]
    STATUTS = [
        ('Planifie', 'Planifie'), ('Engage', 'Engage'),
        ('Liquide', 'Liquide'), ('Paye', 'Paye'),
    ]
    
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE, verbose_name="Etablissement")
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE, verbose_name="Produit")
    pcop = models.ForeignKey(PCOP, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Code PCOP")
    source_financement = models.CharField(max_length=20, choices=SOURCES, verbose_name="Source")
    montant_prevu = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Montant prevu (Ar)")
    montant_realise = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Montant realise (Ar)")
    statut = models.CharField(max_length=20, choices=STATUTS, default='Planifie', verbose_name="Statut")
    date_debut = models.DateField(null=True, blank=True, verbose_name="Date debut")
    date_fin = models.DateField(null=True, blank=True, verbose_name="Date fin")
    remarque = models.TextField(blank=True, verbose_name="Remarque")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ligne budgetaire"
        verbose_name_plural = "Lignes budgetaires"
        ordering = ['etablissement', 'produit']
    
    def __str__(self):
        return f"{self.etablissement.nom} - {self.produit.libelle} ({self.source_financement})"
    
    @property
    def taux_execution(self):
        if self.montant_prevu > 0:
            return round((self.montant_realise / self.montant_prevu) * 100, 2)
        return 0


# ============================================================
# PROFIL UTILISATEUR
# ============================================================

class Profil(models.Model):
    ROLES = [
        ('DRETFP', 'Administrateur DRETFP'),
        ('CHEF_ETAB', "Chef d'etablissement"),
        ('AGENT', 'Agent'),
        ('FORMATEUR', 'Formateur'),
        ('LECTEUR', 'Lecture seule'),
    ]
    
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    role = models.CharField(max_length=20, choices=ROLES, default='AGENT', verbose_name="Role")
    etablissement = models.ForeignKey(Etablissement, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Etablissement")
    telephone = models.CharField(max_length=20, blank=True, verbose_name="Telephone")
    
    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"
    
    def __str__(self):
        return f"{self.utilisateur.username} - {self.get_role_display()}"


# ============================================================
# DEMANDE DE REINITIALISATION
# ============================================================

class DemandeReinitialisation(models.Model):
    STATUTS = [
        ('En attente', 'En attente'),
        ('Traitee', 'Traitee'),
        ('Rejetee', 'Rejetee'),
    ]
    
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    email_contact = models.EmailField(blank=True, verbose_name="Email de contact")
    message = models.TextField(blank=True, verbose_name="Message")
    statut = models.CharField(max_length=20, choices=STATUTS, default='En attente', verbose_name="Statut")
    nouveau_mot_de_passe = models.CharField(max_length=100, blank=True, verbose_name="Nouveau mot de passe")
    date_demande = models.DateTimeField(auto_now_add=True, verbose_name="Date de demande")
    date_traitement = models.DateTimeField(null=True, blank=True, verbose_name="Date de traitement")
    
    class Meta:
        verbose_name = "Demande de reinitialisation"
        verbose_name_plural = "Demandes de reinitialisation"
        ordering = ['-date_demande']
    
    def __str__(self):
        return f"{self.utilisateur.username} - {self.statut}"


# ============================================================
# PTA
# ============================================================

class PTA(models.Model):
    STATUTS = [
        ('Brouillon', 'Brouillon'), ('Valide', 'Valide'),
        ('En cours', 'En cours'), ('Termine', 'Termine'),
        ('Archive', 'Archive'),
    ]
    
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE, verbose_name="Etablissement")
    annee = models.IntegerField(default=2027, verbose_name="Annee")
    titre = models.CharField(max_length=200, verbose_name="Titre")
    statut = models.CharField(max_length=20, choices=STATUTS, default='Brouillon', verbose_name="Statut")
    responsable = models.CharField(max_length=200, blank=True, verbose_name="Responsable")
    date_debut = models.DateField(null=True, blank=True, verbose_name="Date debut")
    date_fin = models.DateField(null=True, blank=True, verbose_name="Date fin")
    remarque = models.TextField(blank=True, verbose_name="Remarque")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "PTA"
        verbose_name_plural = "PTA"
        ordering = ['-annee', 'etablissement']
        unique_together = ['etablissement', 'annee']
    
    def __str__(self):
        return f"PTA {self.annee} - {self.etablissement.nom}"
    
    @property
    def nb_activites(self):
        return self.activites.count()
    
    @property
    def taux_avancement(self):
        activites = self.activites.all()
        if not activites:
            return 0
        total = sum(a.taux_avancement for a in activites)
        return round(total / len(activites), 2)
    
    @property
    def budget_total(self):
        return self.activites.aggregate(total=models.Sum('budget_prevu'))['total'] or 0


# ============================================================
# ACTIVITE PTA
# ============================================================

class ActivitePTA(models.Model):
    STATUTS = [
        ('Non commence', 'Non commence'), ('En cours', 'En cours'),
        ('Termine', 'Termine'), ('Annule', 'Annule'), ('Reporte', 'Reporte'),
    ]
    
    PTA = models.ForeignKey(PTA, on_delete=models.CASCADE, related_name='activites', verbose_name="PTA")
    activite = models.ForeignKey(Activite, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Activite liee")
    titre = models.CharField(max_length=300, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    responsable = models.CharField(max_length=200, blank=True, verbose_name="Responsable")
    statut = models.CharField(max_length=20, choices=STATUTS, default='Non commence', verbose_name="Statut")
    taux_avancement = models.IntegerField(default=0, verbose_name="Taux d'avancement (%)")
    date_debut = models.DateField(null=True, blank=True, verbose_name="Date debut")
    date_fin = models.DateField(null=True, blank=True, verbose_name="Date fin")
    budget_prevu = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Budget prevu (Ar)")
    budget_realise = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Budget realise (Ar)")
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Activite PTA"
        verbose_name_plural = "Activites PTA"
        ordering = ['ordre', 'date_debut', 'titre']
    
    def __str__(self):
        return f"{self.PTA} - {self.titre[:50]}"


# ============================================================
# SALLE
# ============================================================

class Salle(models.Model):
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE, related_name='salles', verbose_name="Etablissement")
    nom = models.CharField(max_length=100, verbose_name="Nom de la salle")
    capacite = models.IntegerField(default=30, verbose_name="Capacite")
    type_salle = models.CharField(max_length=50, blank=True, verbose_name="Type de salle")
    batiment = models.CharField(max_length=100, blank=True, verbose_name="Batiment")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Salle"
        verbose_name_plural = "Salles"
        ordering = ['etablissement', 'nom']
        unique_together = ['etablissement', 'nom']
    
    def __str__(self):
        return f"{self.nom} ({self.etablissement.nom})"


# ============================================================
# FILIERE
# ============================================================

class Filiere(models.Model):
    NIVEAUX = [
        ('CAP', 'CAP'), ('BEP', 'BEP'), ('BAC', 'Baccalaureat'),
        ('AMB', 'Apprentissage Metiers de Base'), ('FPQ', 'Formation Professionnelle Qualifiante'),
    ]
    
    etablissement = models.ForeignKey(Etablissement, on_delete=models.CASCADE, related_name='filieres', verbose_name="Etablissement")
    code = models.CharField(max_length=20, verbose_name="Code")
    nom = models.CharField(max_length=200, verbose_name="Nom de la filiere")
    niveau = models.CharField(max_length=10, choices=NIVEAUX, verbose_name="Niveau")
    nb_apprenants = models.IntegerField(default=0, verbose_name="Nb apprenants")
    duree_annees = models.IntegerField(default=2, verbose_name="Duree (annees)")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Filiere"
        verbose_name_plural = "Filieres"
        ordering = ['etablissement', 'code']
        unique_together = ['etablissement', 'code']
    
    def __str__(self):
        return f"{self.code} - {self.nom}"


# ============================================================
# MATIERE
# ============================================================

class Matiere(models.Model):
    TYPES = [
        ('Theorique', 'Theorique'),
        ('Pratique', 'Pratique'),
        ('Theorique et Pratique', 'Theorique et Pratique'),
        ('Sport', 'Education Physique et Sportive'),
    ]
    
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='matieres', verbose_name="Filiere")
    code = models.CharField(max_length=20, verbose_name="Code")
    nom = models.CharField(max_length=200, verbose_name="Nom de la matiere")
    type_matiere = models.CharField(max_length=30, choices=TYPES, default='Theorique', verbose_name="Type")
    heures_theorie = models.IntegerField(default=0, verbose_name="Heures theorie")
    heures_pratique = models.IntegerField(default=0, verbose_name="Heures pratique")
    coefficient = models.IntegerField(default=1, verbose_name="Coefficient")
    description = models.TextField(blank=True, verbose_name="Description")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Matiere"
        verbose_name_plural = "Matieres"
        ordering = ['filiere', 'code']
        unique_together = ['filiere', 'code']
    
    def __str__(self):
        return f"{self.code} - {self.nom}"
    
    @property
    def heures_total(self):
        return self.heures_theorie + self.heures_pratique


# ============================================================
# CRENEAU HORAIRE
# ============================================================

class CreneauHoraire(models.Model):
    nom = models.CharField(max_length=50, verbose_name="Nom")
    heure_debut = models.TimeField(verbose_name="Heure debut")
    heure_fin = models.TimeField(verbose_name="Heure fin")
    ordre = models.IntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        verbose_name = "Creneau horaire"
        verbose_name_plural = "Creneaux horaires"
        ordering = ['ordre', 'heure_debut']
    
    def __str__(self):
        return f"{self.nom} ({self.heure_debut.strftime('%H:%M')} - {self.heure_fin.strftime('%H:%M')})"


# ============================================================
# EMPLOI DU TEMPS
# ============================================================

class EmploiDuTemps(models.Model):
    JOURS = [
        ('Lundi', 'Lundi'), ('Mardi', 'Mardi'), ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi'), ('Vendredi', 'Vendredi'), ('Samedi', 'Samedi'),
    ]
    
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE, related_name='emplois', verbose_name="Filiere")
    creneau = models.ForeignKey(CreneauHoraire, on_delete=models.CASCADE, verbose_name="Creneau horaire")
    salle = models.ForeignKey(Salle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Salle")
    formateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Formateur")
    matiere = models.CharField(max_length=200, verbose_name="Matiere / Module")
    matiere_lien = models.ForeignKey(Matiere, on_delete=models.SET_NULL, null=True, blank=True, related_name='emplois', verbose_name="Matiere liee")
    jour = models.CharField(max_length=20, choices=JOURS, verbose_name="Jour")
    annee_scolaire = models.CharField(max_length=20, default='2026-2027', verbose_name="Annee scolaire")
    remarque = models.TextField(blank=True, verbose_name="Remarque")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Emploi du temps"
        verbose_name_plural = "Emplois du temps"
        ordering = ['jour', 'creneau__ordre']
    
    def __str__(self):
        return f"{self.filiere.code} - {self.jour} - {self.creneau.nom}"