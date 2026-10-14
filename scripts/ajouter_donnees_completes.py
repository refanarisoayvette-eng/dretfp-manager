"""
Ajouter les donnees completes pour les 13 etablissements :
- Filieres
- Matieres
- Salles
- Formateurs

Utilisation :
    python scripts/ajouter_donnees_completes.py
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Etablissement, Filiere, Matiere, Salle, Profil


# ============================================================
# DONNEES PAR ETABLISSEMENT
# ============================================================

DONNEES = {
    'CFP AMBOSITRA': {
        'salles': [
            ('Salle 101', 40, 'Salle de cours', 'Batiment B'),
            ('Salle 102', 40, 'Salle de cours', 'Batiment B'),
            ('Atelier Bois', 25, 'Atelier', 'Batiment A'),
            ('Atelier Mecanique', 20, 'Atelier', 'Batiment A'),
            ('Salle Informatique', 15, 'Salle informatique', 'Batiment C'),
        ],
        'filieres': [
            {
                'code': 'BTP', 'nom': 'Batiment et Travaux Publics', 'niveau': 'CAP', 'nb': 30, 'duree': 2,
                'matieres': [
                    ('MATH', 'Mathematiques appliquees', 'Theorique', 60, 0, 4),
                    ('DESS', 'Dessin technique', 'Theorique et Pratique', 20, 40, 4),
                    ('MACON', 'Maconnerie', 'Pratique', 0, 120, 5),
                    ('COFF', 'Coffrage et Beton Arme', 'Pratique', 10, 80, 4),
                    ('TOPO', 'Topographie', 'Theorique et Pratique', 30, 30, 3),
                    ('SECU', 'Securite sur chantier', 'Theorique', 20, 0, 2),
                ],
            },
            {
                'code': 'MEB', 'nom': 'Menuiserie Ebenisterie Bois', 'niveau': 'CAP', 'nb': 25, 'duree': 2,
                'matieres': [
                    ('BOIS', 'Technologie du bois', 'Theorique et Pratique', 30, 60, 4),
                    ('DESS', 'Dessin technique', 'Theorique et Pratique', 20, 40, 4),
                    ('FABR', 'Fabrication meubles', 'Pratique', 0, 120, 5),
                    ('MATH', 'Mathematiques', 'Theorique', 40, 0, 3),
                    ('SECU', 'Securite atelier', 'Theorique', 15, 0, 2),
                ],
            },
            {
                'code': 'MEC', 'nom': 'Mecanique Generale', 'niveau': 'CAP', 'nb': 20, 'duree': 2,
                'matieres': [
                    ('MOTEUR', 'Moteurs thermiques', 'Theorique et Pratique', 30, 80, 5),
                    ('DESS', 'Dessin technique', 'Theorique et Pratique', 20, 40, 4),
                    ('USIN', 'Usinage', 'Pratique', 10, 90, 4),
                    ('MATH', 'Mathematiques', 'Theorique', 40, 0, 3),
                ],
            },
            {
                'code': 'INFO', 'nom': 'Informatique et Bureautique', 'niveau': 'BEP', 'nb': 15, 'duree': 2,
                'matieres': [
                    ('WORD', 'Word - Traitement de texte', 'Pratique', 0, 40, 3),
                    ('EXCEL', 'Excel - Tableur', 'Pratique', 0, 60, 4),
                    ('INTERNET', 'Internet et messagerie', 'Pratique', 0, 30, 2),
                    ('MAINT', 'Maintenance informatique', 'Theorique et Pratique', 20, 40, 3),
                ],
            },
            {
                'code': 'AGR', 'nom': 'Agriculture et Elevage', 'niveau': 'AMB', 'nb': 50, 'duree': 1,
                'matieres': [
                    ('CULT', 'Techniques culturales', 'Theorique et Pratique', 30, 60, 4),
                    ('ELEV', 'Elevage', 'Theorique et Pratique', 20, 50, 4),
                    ('SOL', 'Science du sol', 'Theorique', 30, 0, 3),
                ],
            },
        ],
        'formateurs': [
            ('prof_rakoto_amb', 'Rakoto', 'Jean', '0341234567'),
            ('prof_rasoa_amb', 'Rasoa', 'Marie', '0342345678'),
            ('prof_randria_amb', 'Randria', 'Paul', '0343456789'),
        ],
    },
    'CFP AMBOHIMITOMBO': {
        'salles': [
            ('Salle A1', 35, 'Salle de cours', 'Batiment Principal'),
            ('Atelier Bois', 20, 'Atelier', 'Batiment Annexe'),
        ],
        'filieres': [
            {
                'code': 'BTP', 'nom': 'Batiment et Travaux Publics', 'niveau': 'AMB', 'nb': 40, 'duree': 1,
                'matieres': [
                    ('MACON', 'Maconnerie', 'Pratique', 10, 60, 5),
                    ('PLAN', 'Lecture de plans', 'Theorique', 20, 0, 3),
                ],
            },
            {
                'code': 'COUT', 'nom': 'Couture et Confection', 'niveau': 'AMB', 'nb': 35, 'duree': 1,
                'matieres': [
                    ('COUP', 'Coupe et couture', 'Pratique', 10, 60, 5),
                    ('MODE', 'Modelage', 'Theorique et Pratique', 15, 20, 3),
                ],
            },
            {
                'code': 'CUIS', 'nom': 'Cuisine et Restauration', 'niveau': 'AMB', 'nb': 25, 'duree': 1,
                'matieres': [
                    ('TECH', 'Techniques culinaires', 'Pratique', 0, 60, 5),
                    ('HYG', 'Hygiene alimentaire', 'Theorique', 20, 0, 3),
                ],
            },
            {
                'code': 'ELEC', 'nom': 'Electricite de base', 'niveau': 'AMB', 'nb': 30, 'duree': 1,
                'matieres': [
                    ('INST', 'Installations electriques', 'Pratique', 10, 50, 5),
                    ('SECU', 'Securite electrique', 'Theorique', 15, 0, 3),
                ],
            },
        ],
        'formateurs': [
            ('prof_ambohi_1', 'Rakoto', 'Pierre', '0345000001'),
            ('prof_ambohi_2', 'Rasoa', 'Claudine', '0345000002'),
        ],
    },
    'CFP FIADANANA FANDRIANA': {
        'salles': [
            ('Salle F1', 30, 'Salle de cours', 'Batiment F'),
            ('Atelier Mixte', 25, 'Atelier', 'Batiment F'),
        ],
        'filieres': [
            {
                'code': 'MENU', 'nom': 'Menuiserie', 'niveau': 'CAP', 'nb': 25, 'duree': 2,
                'matieres': [
                    ('BOIS', 'Technologie bois', 'Theorique et Pratique', 20, 60, 5),
                    ('DESS', 'Dessin', 'Theorique et Pratique', 20, 40, 3),
                ],
            },
            {
                'code': 'MACO', 'nom': 'Maconnerie', 'niveau': 'CAP', 'nb': 30, 'duree': 2,
                'matieres': [
                    ('MACON', 'Maconnerie', 'Pratique', 10, 80, 5),
                    ('PLAN', 'Lecture de plans', 'Theorique', 30, 0, 3),
                ],
            },
            {
                'code': 'COUT', 'nom': 'Couture', 'niveau': 'CAP', 'nb': 20, 'duree': 2,
                'matieres': [
                    ('COUT', 'Couture pratique', 'Pratique', 10, 80, 5),
                    ('MODE', 'Modelage', 'Theorique et Pratique', 15, 30, 3),
                ],
            },
            {
                'code': 'AGR', 'nom': 'Agriculture', 'niveau': 'AMB', 'nb': 40, 'duree': 1,
                'matieres': [
                    ('CULT', 'Techniques culturales', 'Theorique et Pratique', 20, 60, 5),
                    ('SOL', 'Science du sol', 'Theorique', 25, 0, 3),
                ],
            },
        ],
        'formateurs': [
            ('prof_fiad_1', 'Rasoa', 'Gisele', '0346000001'),
            ('prof_fiad_2', 'Randria', 'Marc', '0346000002'),
        ],
    },
    'CFP AMBATOFINANDRAHANA': {
        'salles': [
            ('Salle 1', 35, 'Salle de cours', 'Batiment Principal'),
            ('Atelier Agricole', 30, 'Atelier', 'Hangar'),
        ],
        'filieres': [
            {
                'code': 'BTP', 'nom': 'Batiment et Travaux Publics', 'niveau': 'CAP', 'nb': 30, 'duree': 2,
                'matieres': [
                    ('MACON', 'Maconnerie', 'Pratique', 10, 80, 5),
                    ('DESS', 'Dessin technique', 'Theorique et Pratique', 20, 40, 4),
                ],
            },
            {
                'code': 'AGR', 'nom': 'Agriculture', 'niveau': 'AMB', 'nb': 45, 'duree': 1,
                'matieres': [
                    ('CULT', 'Techniques culturales', 'Theorique et Pratique', 20, 60, 5),
                    ('SOL', 'Science du sol', 'Theorique', 25, 0, 3),
                ],
            },
            {
                'code': 'ELEV', 'nom': 'Elevage', 'niveau': 'AMB', 'nb': 30, 'duree': 1,
                'matieres': [
                    ('ELEV', 'Techniques d\'elevage', 'Theorique et Pratique', 20, 60, 5),
                    ('VET', 'Veterinaire de base', 'Theorique', 25, 0, 3),
                ],
            },
            {
                'code': 'INFO', 'nom': 'Informatique', 'niveau': 'BEP', 'nb': 20, 'duree': 2,
                'matieres': [
                    ('WORD', 'Word', 'Pratique', 0, 40, 3),
                    ('EXCEL', 'Excel', 'Pratique', 0, 60, 4),
                ],
            },
        ],
        'formateurs': [
            ('prof_ambato_1', 'Rakoto', 'Felix', '0347000001'),
            ('prof_ambato_2', 'Rasoa', 'Nadia', '0347000002'),
        ],
    },
    'CFPF FANDRIANA': {
        'salles': [
            ('Salle A1', 35, 'Salle de cours', 'Batiment Principal'),
            ('Salle A2', 35, 'Salle de cours', 'Batiment Principal'),
            ('Atelier Couture', 20, 'Atelier', 'Batiment Annexe'),
            ('Atelier Cuisine', 15, 'Atelier', 'Batiment Annexe'),
        ],
        'filieres': [
            {
                'code': 'COUT', 'nom': 'Couture et Confection', 'niveau': 'CAP', 'nb': 25, 'duree': 2,
                'matieres': [
                    ('COUP', 'Coupe et couture', 'Pratique', 20, 100, 5),
                    ('MODE', 'Histoire de la mode', 'Theorique', 30, 0, 2),
                    ('DESS', 'Dessin de mode', 'Theorique et Pratique', 20, 40, 3),
                    ('TISS', 'Connaissance des tissus', 'Theorique', 25, 0, 2),
                ],
            },
            {
                'code': 'CUIS', 'nom': 'Cuisine et Restauration', 'niveau': 'CAP', 'nb': 20, 'duree': 2,
                'matieres': [
                    ('TECH', 'Techniques culinaires', 'Pratique', 10, 120, 5),
                    ('HYG', 'Hygiene alimentaire', 'Theorique', 30, 0, 3),
                    ('GEST', 'Gestion de restaurant', 'Theorique et Pratique', 20, 20, 2),
                ],
            },
            {
                'code': 'PATI', 'nom': 'Patisserie', 'niveau': 'CAP', 'nb': 15, 'duree': 2,
                'matieres': [
                    ('PATI', 'Patisserie pratique', 'Pratique', 10, 100, 5),
                    ('DECO', 'Decoration patisserie', 'Theorique et Pratique', 15, 40, 3),
                    ('HYG', 'Hygiene alimentaire', 'Theorique', 20, 0, 2),
                ],
            },
            {
                'code': 'COSM', 'nom': 'Cosmetologie', 'niveau': 'FPQ', 'nb': 18, 'duree': 1,
                'matieres': [
                    ('SOIN', 'Soins du visage', 'Pratique', 0, 60, 4),
                    ('COIF', 'Coiffure', 'Pratique', 0, 80, 5),
                    ('PROD', 'Produits cosmetiques', 'Theorique', 20, 0, 2),
                ],
            },
            {
                'code': 'HOT', 'nom': 'Hotellerie', 'niveau': 'FPQ', 'nb': 15, 'duree': 1,
                'matieres': [
                    ('ACC', 'Accueil hotelier', 'Theorique et Pratique', 20, 40, 4),
                    ('GEST', 'Gestion hoteliere', 'Theorique', 30, 0, 3),
                ],
            },
        ],
        'formateurs': [
            ('prof_fand_1', 'Rasoa', 'Helene', '0348000001'),
            ('prof_fand_2', 'Randria', 'Michel', '0348000002'),
            ('prof_fand_3', 'Rakoto', 'Sophie', '0348000003'),
        ],
    },
    'LTP AMBOSITRA': {
        'salles': [
            ('Salle 201', 45, 'Salle de cours', 'Batiment 1'),
            ('Salle 202', 45, 'Salle de cours', 'Batiment 1'),
            ('Atelier Electronique', 20, 'Atelier', 'Batiment 2'),
            ('Atelier Froid', 15, 'Atelier', 'Batiment 2'),
            ('Labo Physique', 25, 'Laboratoire', 'Batiment 3'),
        ],
        'filieres': [
            {
                'code': 'ELEC', 'nom': 'Electronique', 'niveau': 'BAC', 'nb': 30, 'duree': 3,
                'matieres': [
                    ('ELEC', 'Electronique analogique', 'Theorique et Pratique', 40, 60, 5),
                    ('NUM', 'Electronique numerique', 'Theorique et Pratique', 30, 50, 4),
                    ('MATH', 'Mathematiques', 'Theorique', 60, 0, 4),
                    ('PHY', 'Physique', 'Theorique et Pratique', 40, 30, 4),
                ],
            },
            {
                'code': 'FROID', 'nom': 'Froid et Climatisation', 'niveau': 'BAC', 'nb': 25, 'duree': 3,
                'matieres': [
                    ('FROID', 'Technologie du froid', 'Theorique et Pratique', 40, 60, 5),
                    ('FLUI', 'Fluides frigorigenes', 'Theorique', 30, 0, 3),
                    ('MATH', 'Mathematiques', 'Theorique', 60, 0, 4),
                    ('PHY', 'Physique', 'Theorique et Pratique', 40, 30, 4),
                ],
            },
            {
                'code': 'ELEC2', 'nom': 'Electricite', 'niveau': 'CAP', 'nb': 30, 'duree': 2,
                'matieres': [
                    ('INST', 'Installations electriques', 'Pratique', 20, 100, 5),
                    ('SCHEMA', 'Schemas electriques', 'Theorique et Pratique', 30, 40, 4),
                    ('SECU', 'Securite electrique', 'Theorique', 20, 0, 3),
                ],
            },
            {
                'code': 'MEC', 'nom': 'Mecanique', 'niveau': 'BAC', 'nb': 25, 'duree': 3,
                'matieres': [
                    ('DESS', 'Dessin industriel', 'Theorique et Pratique', 30, 50, 4),
                    ('USIN', 'Usinage', 'Pratique', 10, 90, 5),
                    ('MATH', 'Mathematiques', 'Theorique', 60, 0, 4),
                    ('MATER', 'Resistance des materiaux', 'Theorique', 40, 0, 4),
                ],
            },
            {
                'code': 'SCI', 'nom': 'Sciences', 'niveau': 'BAC', 'nb': 40, 'duree': 3,
                'matieres': [
                    ('MATH', 'Mathematiques', 'Theorique', 80, 0, 5),
                    ('PHY', 'Physique', 'Theorique et Pratique', 50, 40, 5),
                    ('CHIM', 'Chimie', 'Theorique et Pratique', 40, 30, 4),
                    ('SVT', 'Sciences de la Vie et de la Terre', 'Theorique et Pratique', 40, 20, 4),
                ],
            },
        ],
        'formateurs': [
            ('prof_ltpamb_1', 'Rakoto', 'Pierre', '0349000001'),
            ('prof_ltpamb_2', 'Rasoa', 'Claudine', '0349000002'),
            ('prof_ltpamb_3', 'Randria', 'Henri', '0349000003'),
        ],
    },
    'LTP AMBATOFINANDRAHANA': {
        'salles': [
            ('Salle 301', 40, 'Salle de cours', 'Batiment Principal'),
            ('Atelier Technique', 20, 'Atelier', 'Batiment Technique'),
        ],
        'filieres': [
            {
                'code': 'ELEC', 'nom': 'Electricite', 'niveau': 'CAP', 'nb': 25, 'duree': 2,
                'matieres': [
                    ('INST', 'Installations electriques', 'Pratique', 10, 80, 5),
                    ('SCHEMA', 'Schemas', 'Theorique et Pratique', 20, 40, 4),
                ],
            },
            {
                'code': 'MEC', 'nom': 'Mecanique', 'niveau': 'CAP', 'nb': 20, 'duree': 2,
                'matieres': [
                    ('USIN', 'Usinage', 'Pratique', 10, 80, 5),
                    ('DESS', 'Dessin', 'Theorique et Pratique', 20, 40, 4),
                ],
            },
            {
                'code': 'INFO', 'nom': 'Informatique', 'niveau': 'BEP', 'nb': 20, 'duree': 2,
                'matieres': [
                    ('WORD', 'Word', 'Pratique', 0, 40, 3),
                    ('EXCEL', 'Excel', 'Pratique', 0, 60, 4),
                ],
            },
        ],
        'formateurs': [
            ('prof_ltpambato_1', 'Rakoto', 'Robert', '0350000001'),
            ('prof_ltpambato_2', 'Rasoa', 'Lala', '0350000002'),
        ],
    },
    'LTP MIARINAVARATRA': {
        'salles': [
            ('Salle 401', 40, 'Salle de cours', 'Batiment Principal'),
            ('Atelier Agregats', 20, 'Atelier', 'Batiment Technique'),
        ],
        'filieres': [
            {
                'code': 'AGRE', 'nom': 'Agregats et Materiaux', 'niveau': 'CAP', 'nb': 25, 'duree': 2,
                'matieres': [
                    ('BETON', 'Technologie du beton', 'Theorique et Pratique', 30, 60, 5),
                    ('GRAN', 'Granulats', 'Theorique', 25, 0, 3),
                ],
            },
            {
                'code': 'TOPO', 'nom': 'Topographie', 'niveau': 'CAP', 'nb': 20, 'duree': 2,
                'matieres': [
                    ('TOPO', 'Topographie', 'Theorique et Pratique', 30, 60, 5),
                    ('MESU', 'Mesures et calculs', 'Theorique', 30, 0, 3),
                ],
            },
            {
                'code': 'DESS', 'nom': 'Dessin BTP', 'niveau': 'CAP', 'nb': 25, 'duree': 2,
                'matieres': [
                    ('DESS', 'Dessin technique', 'Theorique et Pratique', 30, 80, 5),
                    ('DAO', 'DAO - Autocad', 'Pratique', 10, 50, 4),
                ],
            },
            {
                'code': 'MATH', 'nom': 'Mathematiques', 'niveau': 'BAC', 'nb': 30, 'duree': 3,
                'matieres': [
                    ('MATH', 'Mathematiques', 'Theorique', 80, 0, 5),
                    ('PHY', 'Physique', 'Theorique et Pratique', 40, 30, 4),
                ],
            },
        ],
        'formateurs': [
            ('prof_miar_1', 'Rakoto', 'Robert', '0351000001'),
            ('prof_miar_2', 'Rasoa', 'Nadia', '0351000002'),
        ],
    },
    'LTP FAHIZAY': {
        'salles': [
            ('Salle 501', 40, 'Salle de cours', 'Batiment Principal'),
        ],
        'filieres': [
            {
                'code': 'ELEC', 'nom': 'Electricite', 'niveau': 'CAP', 'nb': 20, 'duree': 2,
                'matieres': [
                    ('INST', 'Installations electriques', 'Pratique', 10, 80, 5),
                    ('SCHEMA', 'Schemas', 'Theorique et Pratique', 20, 40, 4),
                ],
            },
            {
                'code': 'MEC', 'nom': 'Mecanique', 'niveau': 'CAP', 'nb': 20, 'duree': 2,
                'matieres': [
                    ('USIN', 'Usinage', 'Pratique', 10, 80, 5),
                    ('DESS', 'Dessin', 'Theorique et Pratique', 20, 40, 4),
                ],
            },
            {
                'code': 'INFO', 'nom': 'Informatique', 'niveau': 'BEP', 'nb': 15, 'duree': 2,
                'matieres': [
                    ('WORD', 'Word', 'Pratique', 0, 40, 3),
                    ('EXCEL', 'Excel', 'Pratique', 0, 60, 4),
                ],
            },
        ],
        'formateurs': [
            ('prof_fahizay_1', 'Rakoto', 'Georges', '0352000001'),
        ],
    },
    'LTP KIANJANDRAKEFINA': {
        'salles': [
            ('Salle 601', 40, 'Salle de cours', 'Batiment Principal'),
            ('Atelier BTP', 25, 'Atelier', 'Batiment Annexe'),
        ],
        'filieres': [
            {
                'code': 'BTP', 'nom': 'Batiment et Travaux Publics', 'niveau': 'CAP', 'nb': 30, 'duree': 2,
                'matieres': [
                    ('MACON', 'Maconnerie', 'Pratique', 10, 100, 5),
                    ('DESS', 'Dessin technique', 'Theorique et Pratique', 30, 40, 4),
                ],
            },
            {
                'code': 'MEB', 'nom': 'Menuiserie', 'niveau': 'CAP', 'nb': 25, 'duree': 2,
                'matieres': [
                    ('BOIS', 'Technologie bois', 'Theorique et Pratique', 20, 60, 5),
                    ('FABR', 'Fabrication', 'Pratique', 0, 80, 4),
                ],
            },
            {
                'code': 'AGR', 'nom': 'Agriculture', 'niveau': 'AMB', 'nb': 35, 'duree': 1,
                'matieres': [
                    ('CULT', 'Cultures', 'Theorique et Pratique', 20, 60, 5),
                    ('SOL', 'Science du sol', 'Theorique', 25, 0, 3),
                ],
            },
            {
                'code': 'ELEC', 'nom': 'Electricite', 'niveau': 'CAP', 'nb': 25, 'duree': 2,
                'matieres': [
                    ('INST', 'Installations electriques', 'Pratique', 10, 80, 5),
                    ('SCHEMA', 'Schemas', 'Theorique et Pratique', 20, 40, 4),
                ],
            },
        ],
        'formateurs': [
            ('prof_kianja_1', 'Randria', 'David', '0353000001'),
            ('prof_kianja_2', 'Rasoa', 'Fanja', '0353000002'),
        ],
    },
    'LTP MANANDRIANA': {
        'salles': [
            ('Salle 701', 35, 'Salle de cours', 'Batiment Principal'),
        ],
        'filieres': [
            {
                'code': 'MEC', 'nom': 'Mecanique', 'niveau': 'CAP', 'nb': 20, 'duree': 2,
                'matieres': [
                    ('USIN', 'Usinage', 'Pratique', 10, 80, 5),
                    ('DESS', 'Dessin', 'Theorique et Pratique', 20, 40, 4),
                ],
            },
            {
                'code': 'ELEC', 'nom': 'Electricite', 'niveau': 'CAP', 'nb': 20, 'duree': 2,
                'matieres': [
                    ('INST', 'Installations', 'Pratique', 10, 80, 5),
                    ('SECU', 'Securite', 'Theorique', 20, 0, 3),
                ],
            },
            {
                'code': 'INFO', 'nom': 'Informatique', 'niveau': 'BEP', 'nb': 15, 'duree': 2,
                'matieres': [
                    ('WORD', 'Word', 'Pratique', 0, 40, 3),
                    ('EXCEL', 'Excel', 'Pratique', 0, 60, 4),
                ],
            },
        ],
        'formateurs': [
            ('prof_manan_1', 'Rakoto', 'Jacques', '0354000001'),
        ],
    },
    'LTPA FANDRIANA': {
        'salles': [
            ('Salle Agricole', 40, 'Salle de cours', 'Batiment Principal'),
            ('Atelier Agricole', 25, 'Atelier', 'Hangar'),
            ('Ferme Ecole', 50, 'Ferme', 'Terrain'),
        ],
        'filieres': [
            {
                'code': 'PROD', 'nom': 'Production vegetale', 'niveau': 'AMB', 'nb': 40, 'duree': 1,
                'matieres': [
                    ('CULT', 'Techniques culturales', 'Theorique et Pratique', 20, 60, 5),
                    ('SOL', 'Science du sol', 'Theorique', 25, 0, 3),
                    ('BOTA', 'Botanique', 'Theorique', 20, 0, 2),
                ],
            },
            {
                'code': 'ELEV', 'nom': 'Elevage', 'niveau': 'AMB', 'nb': 35, 'duree': 1,
                'matieres': [
                    ('ELEV', 'Techniques d\'elevage', 'Theorique et Pratique', 20, 60, 5),
                    ('ZOO', 'Zoologie', 'Theorique', 25, 0, 3),
                    ('VET', 'Veterinaire de base', 'Theorique', 20, 0, 3),
                ],
            },
            {
                'code': 'AGRO', 'nom': 'Agroalimentaire', 'niveau': 'AMB', 'nb': 30, 'duree': 1,
                'matieres': [
                    ('TRANS', 'Transformation alimentaire', 'Theorique et Pratique', 20, 60, 5),
                    ('HYG', 'Hygiene', 'Theorique', 20, 0, 3),
                ],
            },
            {
                'code': 'AGRI', 'nom': 'Agriculture generale', 'niveau': 'AMB', 'nb': 35, 'duree': 1,
                'matieres': [
                    ('CULT', 'Cultures vivrieres', 'Theorique et Pratique', 20, 60, 5),
                    ('SOL', 'Fertilisation des sols', 'Theorique', 25, 0, 3),
                ],
            },
        ],
        'formateurs': [
            ('prof_ltpa_1', 'Randria', 'David', '0355000001'),
            ('prof_ltpa_2', 'Rasoa', 'Lala', '0355000002'),
        ],
    },
}


# ============================================================
# FONCTIONS
# ============================================================

def creer_salles(etab, salles_data):
    """Cree les salles d'un etablissement."""
    count = 0
    for nom, capacite, type_salle, batiment in salles_data:
        salle, created = Salle.objects.get_or_create(
            etablissement=etab,
            nom=nom,
            defaults={
                'capacite': capacite,
                'type_salle': type_salle,
                'batiment': batiment,
                'actif': True,
            }
        )
        if created:
            count += 1
    return count


def creer_formateurs(etab, formateurs_data):
    """Cree les formateurs (User + Profil)."""
    count = 0
    for username, nom, prenom, tel in formateurs_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': prenom,
                'last_name': nom,
                'email': f'{username}@dretfp.mg',
                'is_staff': False,
                'is_active': True,
            }
        )
        if created:
            user.set_password('Dretfp2027!')
            user.save()
            count += 1
        
        Profil.objects.get_or_create(
            utilisateur=user,
            defaults={
                'role': 'FORMATEUR',
                'etablissement': etab,
                'telephone': tel,
            }
        )
    return count


def creer_filieres_et_matieres(etab, filieres_data):
    """Cree les filieres et leurs matieres."""
    count_fil = 0
    count_mat = 0
    
    for fil_data in filieres_data:
        filiere, created = Filiere.objects.get_or_create(
            etablissement=etab,
            code=fil_data['code'],
            defaults={
                'nom': fil_data['nom'],
                'niveau': fil_data['niveau'],
                'nb_apprenants': fil_data['nb'],
                'duree_annees': fil_data['duree'],
                'actif': True,
            }
        )
        if created:
            count_fil += 1
        
        # Matieres
        for code, nom, type_mat, h_theo, h_prat, coef in fil_data['matieres']:
            matiere, m_created = Matiere.objects.get_or_create(
                filiere=filiere,
                code=code,
                defaults={
                    'nom': nom,
                    'type_matiere': type_mat,
                    'heures_theorie': h_theo,
                    'heures_pratique': h_prat,
                    'coefficient': coef,
                    'actif': True,
                }
            )
            if m_created:
                count_mat += 1
    
    return count_fil, count_mat


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():
    print("=" * 70)
    print("  AJOUT DES DONNEES COMPLETES")
    print("  Filieres + Matieres + Salles + Formateurs")
    print("=" * 70)
    print()
    
    total_salles = 0
    total_formateurs = 0
    total_filieres = 0
    total_matieres = 0
    
    for nom_etab, data in DONNEES.items():
        try:
            etab = Etablissement.objects.get(nom=nom_etab)
        except Etablissement.DoesNotExist:
            print(f"[!] {nom_etab} introuvable - ignore")
            continue
        
        print(f"\n[{nom_etab}]")
        print("-" * 60)
        
        # Salles
        nb = creer_salles(etab, data['salles'])
        total_salles += nb
        print(f"  Salles creees       : {nb}")
        
        # Formateurs
        nb = creer_formateurs(etab, data['formateurs'])
        total_formateurs += nb
        print(f"  Formateurs crees    : {nb}")
        
        # Filieres + Matieres
        nb_f, nb_m = creer_filieres_et_matieres(etab, data['filieres'])
        total_filieres += nb_f
        total_matieres += nb_m
        print(f"  Filieres creees     : {nb_f}")
        print(f"  Matieres creees     : {nb_m}")
    
    # Resume
    print()
    print("=" * 70)
    print("  RESUME GLOBAL")
    print("=" * 70)
    print(f"  Salles creees       : {total_salles}")
    print(f"  Formateurs crees    : {total_formateurs}")
    print(f"  Filieres creees     : {total_filieres}")
    print(f"  Matieres creees     : {total_matieres}")
    print()
    print("  ETAT EN BASE :")
    print(f"     Etablissements     : {Etablissement.objects.count()}")
    print(f"     Salles             : {Salle.objects.count()}")
    print(f"     Formateurs         : {Profil.objects.filter(role='FORMATEUR').count()}")
    print(f"     Filieres           : {Filiere.objects.count()}")
    print(f"     Matieres           : {Matiere.objects.count()}")
    print()
    print("=" * 70)
    print("  TERMINE !")
    print("=" * 70)
    print()
    print("  Mot de passe des formateurs : Dretfp2027!")


if __name__ == '__main__':
    main()