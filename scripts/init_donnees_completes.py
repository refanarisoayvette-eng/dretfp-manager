"""
Script d'initialisation des donnees completes pour DRETFP Manager.
Cree : salles, filieres, matieres, formateurs et emplois du temps.

Utilisation :
    python scripts/init_donnees_completes.py
"""

import os
import sys
import django
from datetime import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import (
    Etablissement, Salle, Filiere, Matiere, Profil,
    CreneauHoraire, EmploiDuTemps
)


# ============================================================
# CONFIGURATION DES DONNEES PAR ETABLISSEMENT
# ============================================================

DONNEES_ETABLISSEMENTS = {
    'CFP AMBOSITRA': {
        'salles': [
            ('Salle 101', 40, 'Salle de cours', 'Batiment B'),
            ('Salle 102', 40, 'Salle de cours', 'Batiment B'),
            ('Atelier Bois', 25, 'Atelier', 'Batiment A'),
            ('Atelier Mecanique', 20, 'Atelier', 'Batiment A'),
            ('Salle Informatique', 15, 'Salle informatique', 'Batiment C'),
        ],
        'filieres': [
            ('BTP', 'Batiment et Travaux Publics', 'CAP', 30, 2),
            ('MEB', 'Menuiserie Ebenisterie Bois', 'CAP', 25, 2),
            ('MEC', 'Mecanique Generale', 'CAP', 20, 2),
            ('INFO', 'Informatique et Bureautique', 'BEP', 15, 2),
            ('AGR', 'Agriculture et Elevage', 'AMB', 50, 1),
        ],
        'matieres_par_filiere': {
            'BTP': [
                ('MATH', 'Mathematiques appliquees', 'Theorique', 60, 0, 4),
                ('DESS', 'Dessin technique', 'Theorique et Pratique', 20, 40, 4),
                ('MACON', 'Maconnerie', 'Pratique', 0, 120, 5),
                ('COFF', 'Coffrage et Beton Arme', 'Pratique', 10, 80, 4),
                ('TOPO', 'Topographie', 'Theorique et Pratique', 30, 30, 3),
                ('SECU', 'Securite sur chantier', 'Theorique', 20, 0, 2),
            ],
            'MEB': [
                ('BOIS', 'Technologie du bois', 'Theorique et Pratique', 30, 60, 4),
                ('DESS', 'Dessin technique', 'Theorique et Pratique', 20, 40, 4),
                ('FABR', 'Fabrication meubles', 'Pratique', 0, 120, 5),
                ('MATH', 'Mathematiques', 'Theorique', 40, 0, 3),
                ('SECU', 'Securite atelier', 'Theorique', 15, 0, 2),
            ],
            'MEC': [
                ('MOTEUR', 'Moteurs thermiques', 'Theorique et Pratique', 30, 80, 5),
                ('DESS', 'Dessin technique', 'Theorique et Pratique', 20, 40, 4),
                ('USIN', 'Usinage', 'Pratique', 10, 90, 4),
                ('MATH', 'Mathematiques', 'Theorique', 40, 0, 3),
                ('ELEC', 'Electricite automobile', 'Theorique et Pratique', 20, 30, 3),
            ],
            'INFO': [
                ('WORD', 'Word - Traitement de texte', 'Pratique', 0, 40, 3),
                ('EXCEL', 'Excel - Tableur', 'Pratique', 0, 60, 4),
                ('INTERNET', 'Internet et messagerie', 'Pratique', 0, 30, 2),
                ('MAINT', 'Maintenance informatique', 'Theorique et Pratique', 20, 40, 3),
                ('BUREAU', 'Logiciels bureautiques', 'Theorique et Pratique', 10, 50, 3),
            ],
            'AGR': [
                ('CULT', 'Techniques culturales', 'Theorique et Pratique', 30, 60, 4),
                ('ELEV', 'Elevage', 'Theorique et Pratique', 20, 50, 4),
                ('SOL', 'Science du sol', 'Theorique', 30, 0, 3),
                ('MACH', 'Machinisme agricole', 'Theorique et Pratique', 10, 30, 3),
            ],
        },
        'formateurs': [
            ('prof_rakoto', 'Rakoto', 'Jean', '0341234567', 'BTP'),
            ('prof_rasoa', 'Rasoa', 'Marie', '0342345678', 'MEB'),
            ('prof_randria', 'Randria', 'Paul', '0343456789', 'MEC'),
            ('prof_rabe', 'Rabe', 'Luc', '0344567890', 'INFO'),
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
            ('COUT', 'Couture et Confection', 'CAP', 25, 2),
            ('CUIS', 'Cuisine et Restauration', 'CAP', 20, 2),
            ('PATI', 'Patisserie', 'CAP', 15, 2),
            ('COSM', 'Cosmetologie', 'FPQ', 18, 1),
        ],
        'matieres_par_filiere': {
            'COUT': [
                ('COUP', 'Coupe et couture', 'Pratique', 20, 100, 5),
                ('MODE', 'Histoire de la mode', 'Theorique', 30, 0, 2),
                ('DESS', 'Dessin de mode', 'Theorique et Pratique', 20, 40, 3),
                ('TISS', 'Connaissance des tissus', 'Theorique', 25, 0, 2),
            ],
            'CUIS': [
                ('TECH', 'Techniques culinaires', 'Pratique', 10, 120, 5),
                ('HYG', 'Hygiene alimentaire', 'Theorique', 30, 0, 3),
                ('GEST', 'Gestion de restaurant', 'Theorique et Pratique', 20, 20, 2),
            ],
            'PATI': [
                ('PATI', 'Patisserie pratique', 'Pratique', 10, 100, 5),
                ('DECO', 'Decoration patisserie', 'Theorique et Pratique', 15, 40, 3),
                ('HYG', 'Hygiene alimentaire', 'Theorique', 20, 0, 2),
            ],
            'COSM': [
                ('SOIN', 'Soins du visage', 'Pratique', 0, 60, 4),
                ('COIF', 'Coiffure', 'Pratique', 0, 80, 5),
                ('PROD', 'Produits cosmetiques', 'Theorique', 20, 0, 2),
            ],
        },
        'formateurs': [
            ('prof_rasoa2', 'Rasoa', 'Helene', '0345000001', 'COUT'),
            ('prof_randria2', 'Randria', 'Michel', '0345000002', 'CUIS'),
            ('prof_rakoto2', 'Rakoto', 'Sophie', '0345000003', 'PATI'),
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
            ('ELEC', 'Electronique', 'BAC', 30, 3),
            ('FROID', 'Froid et Climatisation', 'BAC', 25, 3),
            ('ELEC2', 'Electricite', 'CAP', 30, 2),
            ('MEC', 'Mecanique', 'BAC', 25, 3),
            ('SCI', 'Sciences', 'BAC', 40, 3),
        ],
        'matieres_par_filiere': {
            'ELEC': [
                ('ELEC', 'Electronique analogique', 'Theorique et Pratique', 40, 60, 5),
                ('NUM', 'Electronique numerique', 'Theorique et Pratique', 30, 50, 4),
                ('MATH', 'Mathematiques', 'Theorique', 60, 0, 4),
                ('PHY', 'Physique', 'Theorique et Pratique', 40, 30, 4),
                ('INFO', 'Informatique industrielle', 'Theorique et Pratique', 20, 40, 3),
            ],
            'FROID': [
                ('FROID', 'Technologie du froid', 'Theorique et Pratique', 40, 60, 5),
                ('FLUI', 'Fluides frigorigenes', 'Theorique', 30, 0, 3),
                ('MATH', 'Mathematiques', 'Theorique', 60, 0, 4),
                ('PHY', 'Physique', 'Theorique et Pratique', 40, 30, 4),
            ],
            'ELEC2': [
                ('INST', 'Installations electriques', 'Pratique', 20, 100, 5),
                ('SCHEMA', 'Schemas electriques', 'Theorique et Pratique', 30, 40, 4),
                ('SECU', 'Securite electrique', 'Theorique', 20, 0, 3),
                ('MATH', 'Mathematiques', 'Theorique', 40, 0, 3),
            ],
            'MEC': [
                ('DESS', 'Dessin industriel', 'Theorique et Pratique', 30, 50, 4),
                ('USIN', 'Usinage', 'Pratique', 10, 90, 5),
                ('MATH', 'Mathematiques', 'Theorique', 60, 0, 4),
                ('MATER', 'Resistance des materiaux', 'Theorique', 40, 0, 4),
            ],
            'SCI': [
                ('MATH', 'Mathematiques', 'Theorique', 80, 0, 5),
                ('PHY', 'Physique', 'Theorique et Pratique', 50, 40, 5),
                ('CHIM', 'Chimie', 'Theorique et Pratique', 40, 30, 4),
                ('SVT', 'Sciences de la Vie et de la Terre', 'Theorique et Pratique', 40, 20, 4),
            ],
        },
        'formateurs': [
            ('prof_amb1', 'Rakoto', 'Pierre', '0346000001', 'ELEC'),
            ('prof_amb2', 'Rasoa', 'Claudine', '0346000002', 'FROID'),
            ('prof_amb3', 'Randria', 'Henri', '0346000003', 'MEC'),
            ('prof_amb4', 'Rabe', 'Anne', '0346000004', 'SCI'),
        ],
    },
    'LTP MIARINAVARATRA': {
        'salles': [
            ('Salle 301', 40, 'Salle de cours', 'Batiment Principal'),
            ('Salle 302', 40, 'Salle de cours', 'Batiment Principal'),
            ('Atelier Agreg', 20, 'Atelier', 'Batiment Technique'),
        ],
        'filieres': [
            ('AGRE', 'Agregats et Materiaux', 'CAP', 25, 2),
            ('TOPO', 'Topographie', 'CAP', 20, 2),
            ('DESS', 'Dessin BTP', 'CAP', 25, 2),
        ],
        'matieres_par_filiere': {
            'AGRE': [
                ('BETON', 'Technologie du beton', 'Theorique et Pratique', 30, 60, 5),
                ('GRAN', 'Granulats', 'Theorique', 25, 0, 3),
                ('MATH', 'Mathematiques', 'Theorique', 40, 0, 3),
            ],
            'TOPO': [
                ('TOPO', 'Topographie', 'Theorique et Pratique', 30, 60, 5),
                ('MESU', 'Mesures et calculs', 'Theorique', 30, 0, 3),
                ('DESS', 'Dessin topographique', 'Pratique', 10, 40, 3),
            ],
            'DESS': [
                ('DESS', 'Dessin technique', 'Theorique et Pratique', 30, 80, 5),
                ('DAO', 'DAO - Autocad', 'Pratique', 10, 50, 4),
                ('MATH', 'Mathematiques', 'Theorique', 40, 0, 3),
            ],
        },
        'formateurs': [
            ('prof_miar1', 'Rakoto', 'Robert', '0347000001', 'AGRE'),
            ('prof_miar2', 'Rasoa', 'Nadia', '0347000002', 'TOPO'),
        ],
    },
    'LTPA FANDRIANA': {
        'salles': [
            ('Salle Agricole', 40, 'Salle de cours', 'Batiment Principal'),
            ('Atelier Agricole', 25, 'Atelier', 'Hangar'),
            ('Ferme Ecole', 50, 'Ferme', 'Terrain'),
        ],
        'filieres': [
            ('PROD', 'Production vegetale', 'AMB', 40, 1),
            ('ELEV', 'Elevage', 'AMB', 35, 1),
            ('AGRO', 'Agroalimentaire', 'AMB', 30, 1),
        ],
        'matieres_par_filiere': {
            'PROD': [
                ('CULT', 'Techniques culturales', 'Theorique et Pratique', 20, 60, 5),
                ('SOL', 'Science du sol', 'Theorique', 25, 0, 3),
                ('BOTA', 'Botanique', 'Theorique', 20, 0, 2),
            ],
            'ELEV': [
                ('ELEV', 'Techniques d\'elevage', 'Theorique et Pratique', 20, 60, 5),
                ('ZOO', 'Zoologie', 'Theorique', 25, 0, 3),
                ('VET', 'Veterinaire de base', 'Theorique', 20, 0, 3),
            ],
            'AGRO': [
                ('TRANS', 'Transformation alimentaire', 'Theorique et Pratique', 20, 60, 5),
                ('HYG', 'Hygiene', 'Theorique', 20, 0, 3),
                ('GEST', 'Gestion d\'entreprise', 'Theorique', 25, 0, 3),
            ],
        },
        'formateurs': [
            ('prof_ltpa1', 'Randria', 'David', '0348000001', 'PROD'),
            ('prof_ltpa2', 'Rasoa', 'Lala', '0348000002', 'ELEV'),
            ('prof_ltpa3', 'Rabe', 'Fanja', '0348000003', 'AGRO'),
        ],
    },
    'LTPA AMBINDA FANDRIANA': {
        'salles': [
            ('Salle 1', 35, 'Salle de cours', 'Batiment Principal'),
            ('Hangar Agricole', 30, 'Atelier', 'Exterieur'),
        ],
        'filieres': [
            ('AGRI', 'Agriculture generale', 'AMB', 35, 1),
            ('ANIM', 'Production animale', 'AMB', 30, 1),
        ],
        'matieres_par_filiere': {
            'AGRI': [
                ('CULT', 'Cultures vivrieres', 'Theorique et Pratique', 20, 60, 5),
                ('SOL', 'Fertilisation des sols', 'Theorique', 25, 0, 3),
            ],
            'ANIM': [
                ('ELEV', 'Elevage bovin', 'Theorique et Pratique', 20, 60, 5),
                ('NUTR', 'Nutrition animale', 'Theorique', 25, 0, 3),
            ],
        },
        'formateurs': [
            ('prof_ambinda1', 'Rakoto', 'Felix', '0349000001', 'AGRI'),
        ],
    },
    'CFP FIADANANA FANDRIANA': {
        'salles': [
            ('Salle F1', 30, 'Salle de cours', 'Batiment F'),
            ('Atelier Mixte', 25, 'Atelier', 'Batiment F'),
        ],
        'filieres': [
            ('MENU', 'Menuiserie', 'CAP', 25, 2),
            ('MAÇON', 'Maconnerie', 'CAP', 25, 2),
            ('COUT', 'Couture', 'CAP', 20, 2),
        ],
        'matieres_par_filiere': {
            'MENU': [
                ('BOIS', 'Technologie bois', 'Theorique et Pratique', 20, 60, 5),
                ('DESS', 'Dessin', 'Theorique et Pratique', 20, 40, 3),
            ],
            'MAÇON': [
                ('MACON', 'Maconnerie', 'Pratique', 10, 80, 5),
                ('PLAN', 'Lecture de plans', 'Theorique', 30, 0, 3),
            ],
            'COUT': [
                ('COUT', 'Couture pratique', 'Pratique', 10, 80, 5),
                ('MODE', 'Modelage', 'Theorique et Pratique', 15, 30, 3),
            ],
        },
        'formateurs': [
            ('prof_fiad1', 'Rasoa', 'Gisele', '0341000001', 'COUT'),
            ('prof_fiad2', 'Randria', 'Marc', '0341000002', 'MENU'),
        ],
    },
}


# ============================================================
# FONCTIONS
# ============================================================

def creer_creneaux():
    """Cree les creneaux horaires de base."""
    print("\n📅 Creation des creneaux horaires...")
    creneaux = [
        ('Matin 1', time(8, 0), time(10, 0), 1),
        ('Matin 2', time(10, 15), time(12, 0), 2),
        ('Apres-midi 1', time(14, 0), time(16, 0), 3),
        ('Apres-midi 2', time(16, 15), time(18, 0), 4),
    ]
    for nom, debut, fin, ordre in creneaux:
        c, created = CreneauHoraire.objects.get_or_create(
            nom=nom,
            defaults={'heure_debut': debut, 'heure_fin': fin, 'ordre': ordre}
        )
        if created:
            print(f"   ✅ Cree : {c.nom}")
    print(f"   Total : {CreneauHoraire.objects.count()} creneaux")


def creer_formateur(username, nom, prenom, tel, etablissement, specialite):
    """Cree un formateur (User + Profil)."""
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
    
    profil, p_created = Profil.objects.get_or_create(
        utilisateur=user,
        defaults={
            'role': 'FORMATEUR',
            'etablissement': etablissement,
            'telephone': tel,
        }
    )
    if not p_created:
        profil.role = 'FORMATEUR'
        profil.etablissement = etablissement
        profil.telephone = tel
        profil.save()
    
    return user, created


def creer_emploi_du_temps(filiere, formateurs_dispo, creneaux):
    """Cree un emploi du temps pour une filiere."""
    matieres = Matiere.objects.filter(filiere=filiere)[:5]
    if not matieres:
        return 0
    
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi']
    nb_crees = 0
    
    for i, jour in enumerate(jours):
        for j, creneau in enumerate(creneaux[:2]):  # Matin 1 et Matin 2
            matiere_idx = (i * 2 + j) % len(matieres)
            matiere = matieres[matiere_idx]
            
            # Choisir un formateur
            formateur = formateurs_dispo[i % len(formateurs_dispo)] if formateurs_dispo else None
            
            # Choisir une salle
            salle = Salle.objects.filter(etablissement=filiere.etablissement).first()
            
            emploi, created = EmploiDuTemps.objects.get_or_create(
                filiere=filiere,
                jour=jour,
                creneau=creneau,
                defaults={
                    'matiere': matiere.nom,
                    'matiere_lien': matiere,
                    'salle': salle,
                    'formateur': formateur,
                    'annee_scolaire': '2026-2027',
                }
            )
            if created:
                nb_crees += 1
    
    return nb_crees


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

def main():
    print("=" * 70)
    print("  INITIALISATION DES DONNEES COMPLETES")
    print("  DRETFP Manager - Amoron'i Mania")
    print("=" * 70)
    
    # 1. Creneaux
    creer_creneaux()
    creneaux = list(CreneauHoraire.objects.all().order_by('ordre'))
    
    # 2. Traitement par etablissement
    total_salles = 0
    total_filieres = 0
    total_matieres = 0
    total_formateurs = 0
    total_emplois = 0
    
    for nom_etab, donnees in DONNEES_ETABLISSEMENTS.items():
        print(f"\n{'─' * 70}")
        print(f"  🏫 {nom_etab}")
        print(f"{'─' * 70}")
        
        # Recuperer l'etablissement
        try:
            etab = Etablissement.objects.get(nom=nom_etab)
        except Etablissement.DoesNotExist:
            print(f"   ⚠️  Etablissement non trouve, ignore.")
            continue
        
        # 2.1 Salles
        print(f"\n  🚪 Salles...")
        for nom_salle, capacite, type_salle, batiment in donnees['salles']:
            salle, created = Salle.objects.get_or_create(
                etablissement=etab,
                nom=nom_salle,
                defaults={
                    'capacite': capacite,
                    'type_salle': type_salle,
                    'batiment': batiment,
                }
            )
            if created:
                total_salles += 1
                print(f"     ✅ {nom_salle} ({capacite} places)")
        
        # 2.2 Filieres
        print(f"\n  🎓 Filieres...")
        for code, nom, niveau, nb, duree in donnees['filieres']:
            filiere, created = Filiere.objects.get_or_create(
                etablissement=etab,
                code=code,
                defaults={
                    'nom': nom,
                    'niveau': niveau,
                    'nb_apprenants': nb,
                    'duree_annees': duree,
                }
            )
            if created:
                total_filieres += 1
                print(f"     ✅ {code} - {nom}")
            
            # 2.3 Matieres pour cette filiere
            if code in donnees.get('matieres_par_filiere', {}):
                for mat_code, mat_nom, mat_type, h_theo, h_prat, coef in donnees['matieres_par_filiere'][code]:
                    matiere, m_created = Matiere.objects.get_or_create(
                        filiere=filiere,
                        code=mat_code,
                        defaults={
                            'nom': mat_nom,
                            'type_matiere': mat_type,
                            'heures_theorie': h_theo,
                            'heures_pratique': h_prat,
                            'coefficient': coef,
                        }
                    )
                    if m_created:
                        total_matieres += 1
        
        # 2.4 Formateurs
        print(f"\n  👨‍🏫 Formateurs...")
        formateurs_crees = []
        for username, nom, prenom, tel, specialite in donnees.get('formateurs', []):
            user, created = creer_formateur(username, nom, prenom, tel, etab, specialite)
            formateurs_crees.append(user)
            if created:
                total_formateurs += 1
                print(f"     ✅ {prenom} {nom} ({username})")
        
        # 2.5 Emplois du temps
        print(f"\n  📅 Emplois du temps...")
        filieres_etab = Filiere.objects.filter(etablissement=etab)
        for filiere in filieres_etab:
            nb = creer_emploi_du_temps(filiere, formateurs_crees, creneaux)
            if nb > 0:
                total_emplois += nb
                print(f"     ✅ {filiere.code} : {nb} creneaux")
    
    # 3. Resume
    print(f"\n{'═' * 70}")
    print(f"  📊 RESUME DE L'INITIALISATION")
    print(f"{'═' * 70}")
    print(f"  Salles creees        : {total_salles}")
    print(f"  Filieres creees      : {total_filieres}")
    print(f"  Matieres creees      : {total_matieres}")
    print(f"  Formateurs crees     : {total_formateurs}")
    print(f"  Creneaux emploi cree : {total_emplois}")
    print()
    print(f"  📈 TOTAL EN BASE :")
    print(f"     Salles          : {Salle.objects.count()}")
    print(f"     Filieres        : {Filiere.objects.count()}")
    print(f"     Matieres        : {Matiere.objects.count()}")
    print(f"     Formateurs      : {Profil.objects.filter(role='FORMATEUR').count()}")
    print(f"     Creneaux emploi : {EmploiDuTemps.objects.count()}")
    print()
    print(f"  🔑 Mot de passe formateurs : Dretfp2027!")
    print()
    print(f"🎉 INITIALISATION TERMINEE !")
    print(f"{'═' * 70}")


if __name__ == '__main__':
    main()