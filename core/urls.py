from django.urls import path
from . import views

urlpatterns = [
    # Pages principales
    path('', views.accueil, name='accueil'),
    path('tableau-bord/', views.tableau_bord, name='tableau_bord'),
    path('etablissements/', views.liste_etablissements, name='liste_etablissements'),
    path('statistiques/', views.statistiques, name='statistiques'),
    
    # Inscription
    path('inscription/', views.inscription, name='inscription'),
    
    # Mot de passe oublie
    path('mot-de-passe-oublie/', views.mot_de_passe_oublie, name='mot_de_passe_oublie'),
    path('demandes/', views.liste_demandes, name='liste_demandes'),
    path('demandes/<int:demande_id>/traiter/', views.traiter_demande, name='traiter_demande'),
    
    # Budgets
    path('budgets/', views.liste_budgets, name='liste_budgets'),
    path('budgets/ajouter/', views.ajouter_budget, name='ajouter_budget'),
    path('budgets/<int:ligne_id>/editer/', views.editer_budget, name='editer_budget'),
    path('budgets/<int:ligne_id>/supprimer/', views.supprimer_budget, name='supprimer_budget'),
    
    # Activites
    path('activites/', views.liste_activites, name='liste_activites'),
    path('activites/ajouter/', views.ajouter_activite, name='ajouter_activite'),
    path('activites/<int:activite_id>/editer/', views.editer_activite, name='editer_activite'),
    path('activites/<int:activite_id>/supprimer/', views.supprimer_activite, name='supprimer_activite'),
    
    # PTA
    path('pta/', views.liste_pta, name='liste_pta'),
    path('pta/ajouter/', views.ajouter_pta, name='ajouter_pta'),
    path('pta/<int:pta_id>/', views.detail_pta, name='detail_pta'),
    path('pta/<int:pta_id>/editer/', views.editer_pta, name='editer_pta'),
    path('pta/<int:pta_id>/supprimer/', views.supprimer_pta, name='supprimer_pta'),
    path('pta/<int:pta_id>/activite/ajouter/', views.ajouter_activite_pta, name='ajouter_activite_pta'),
    path('pta/activite/<int:activite_id>/editer/', views.editer_activite_pta, name='editer_activite_pta'),
    path('pta/activite/<int:activite_id>/supprimer/', views.supprimer_activite_pta, name='supprimer_activite_pta'),
    
    # Exports PTA
    path('pta/<int:pta_id>/export/pdf/', views.export_pta_pdf, name='export_pta_pdf'),
    path('pta/<int:pta_id>/export/excel/', views.export_activites_pta_excel, name='export_activites_pta_excel'),
    path('pta/export/excel/', views.export_pta_excel, name='export_pta_excel'),
    path('pta/export/csv/', views.export_pta_csv, name='export_pta_csv'),
    
    # Salles
    path('salles/', views.liste_salles, name='liste_salles'),
    path('salles/ajouter/', views.ajouter_salle, name='ajouter_salle'),
    path('salles/<int:salle_id>/editer/', views.editer_salle, name='editer_salle'),
    path('salles/<int:salle_id>/supprimer/', views.supprimer_salle, name='supprimer_salle'),
    path('salles/export/pdf/', views.export_salles_pdf, name='export_salles_pdf'),
    
    # Filieres
    path('filieres/', views.liste_filieres, name='liste_filieres'),
    path('filieres/ajouter/', views.ajouter_filiere, name='ajouter_filiere'),
    path('filieres/<int:filiere_id>/editer/', views.editer_filiere, name='editer_filiere'),
    path('filieres/<int:filiere_id>/supprimer/', views.supprimer_filiere, name='supprimer_filiere'),
    path('filieres/export/pdf/', views.export_filieres_pdf, name='export_filieres_pdf'),
    path('filieres/export/excel/', views.export_filieres_excel, name='export_filieres_excel'),
    
    # Matieres
    path('matieres/', views.liste_matieres, name='liste_matieres'),
    path('matieres/ajouter/', views.ajouter_matiere, name='ajouter_matiere'),
    path('matieres/<int:matiere_id>/editer/', views.editer_matiere, name='editer_matiere'),
    path('matieres/<int:matiere_id>/supprimer/', views.supprimer_matiere, name='supprimer_matiere'),
    path('matieres/export/pdf/', views.export_matieres_pdf, name='export_matieres_pdf'),
    
    # Formateurs
    path('formateurs/', views.liste_formateurs, name='liste_formateurs'),
    path('formateurs/export/pdf/', views.export_formateurs_pdf, name='export_formateurs_pdf'),
    
    # Emploi du temps
    path('emplois/', views.liste_emplois, name='liste_emplois'),
    path('emplois/hebdomadaire/', views.vue_hebdomadaire, name='vue_hebdomadaire'),
    path('emplois/ajouter/', views.ajouter_emploi, name='ajouter_emploi'),
    path('emplois/<int:emploi_id>/editer/', views.editer_emploi, name='editer_emploi'),
    path('emplois/<int:emploi_id>/supprimer/', views.supprimer_emploi, name='supprimer_emploi'),
    path('emplois/<int:filiere_id>/export/pdf/', views.export_emploi_pdf, name='export_emploi_pdf'),
    
    # Exports Budgets
    path('export/budgets.csv', views.export_budgets_csv, name='export_budgets_csv'),
    path('export/budgets.xlsx', views.export_budgets_excel, name='export_budgets_excel'),
    
    # Rapports
    path('rapports/', views.rapports, name='rapports'),
    path('rapports/global.pdf', views.rapport_pdf_global, name='rapport_pdf_global'),
    
    # API pour graphiques
    path('api/sources/', views.api_sources, name='api_sources'),
    path('api/etablissements/', views.api_etablissements, name='api_etablissements'),
    path('api/produits/', views.api_produits, name='api_produits'),
    path('api/statuts/', views.api_statuts, name='api_statuts'),
    path('api/top-etablissements/', views.api_top_etablissements, name='api_top_etablissements'),
    path('api/types-etablissements/', views.api_types_etablissements, name='api_types_etablissements'),
    path('api/rpi-fce-par-etab/', views.api_rpi_fce_par_etab, name='api_rpi_fce_par_etab'),
    path('api/top-etablissements-montant/', views.api_top_etablissements_montant, name='api_top_etablissements_montant'),
    path('api/produits-par-etab/', views.api_produits_par_etab, name='api_produits_par_etab'),
    path('api/taux-execution-etab/', views.api_taux_execution_etab, name='api_taux_execution_etab'),
    path('api/statuts-detail/', views.api_statuts_detail, name='api_statuts_detail'),
]