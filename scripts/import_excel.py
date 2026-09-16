"""
Script d'importation du fichier FUSION_CANEVAS_TPA_2027.xlsx
vers la base de données Django.

Utilisation :
    python scripts/import_excel.py
"""

import os
import sys
import django
import openpyxl
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import (
    Etablissement, Programme, Activite, SousActivite,
    Produit, PCOP, LigneBudgetaire
)


# ============================================================
# CONFIGURATION
# ============================================================

FICHIER_EXCEL = 'FUSION_CANEVAS_TPA_2027.xlsx'

# Feuilles à traiter
FEUILLES_A_TRAITER = [
    'Feuille 1',
    'DRETFP ET SES ETABLISSEMENTS',
    'DRETFP ET SES ETABLISSEMENTS (1',
    'DRETFP ET SES ETABLISSEMENTS (5',
    'CFPF FANDRIANA',
    'CFP AMBOSITRA',
]

# ⚠️ LISTE BLANCHE STRICTE : SEULEMENT ces établissements
ETABLISSEMENTS_VALIDES = [
    'CFP AMBOSITRA',
    'CFP FIADANANA FANDRIANA',
    'CFPF FANDRIANA',
    'LTP AMBOSITRA',
    'LTP MIARINAVARATRA',
    'LTPA Ambinda Fandriana',
    'LTPA Fandriana',
]

# Correspondance nom dans Excel → nom normalisé
NORMALISATION_ETAB = {
    'CFP AMBOSITRA': 'CFP AMBOSITRA',
    'CFP FIADANANA FANDRIANA': 'CFP FIADANANA FANDRIANA',
    'CFPF FANDRIANA': 'CFPF FANDRIANA',
    'LTP AMBOSITRA': 'LTP AMBOSITRA',
    'LTP MIARINAVARATRA': 'LTP MIARINAVARATRA',
    'LTPA AMBINDA FANDRIANA': 'LTPA Ambinda Fandriana',
    'LTPA FANDRIANA': 'LTPA Fandriana',
}


# ============================================================
# FONCTIONS UTILITAIRES
# ============================================================

def normaliser_etablissement(val):
    """Retourne le nom normalisé si val est un établissement valide, sinon None."""
    if not val:
        return None
    val_upper = str(val).strip().upper()
    
    for etab in ETABLISSEMENTS_VALIDES:
        if etab.upper() == val_upper:
            return NORMALISATION_ETAB.get(val_upper, etab)
    
    return None


def get_or_create_etablissement(nom_normalise):
    """Récupère ou crée un établissement (nom déjà validé)."""
    if not nom_normalise:
        return None
    
    upper = nom_normalise.upper()
    type_etab = 'LTP'
    if 'CFPF' in upper:
        type_etab = 'CFPF'
    elif 'CFP' in upper:
        type_etab = 'CFP'
    elif 'LTPA' in upper:
        type_etab = 'LTPA'
    elif 'LTP' in upper:
        type_etab = 'LTP'
    
    etab, created = Etablissement.objects.get_or_create(
        nom=nom_normalise,
        defaults={
            'type_etablissement': type_etab,
            'district': "Amoron'i Mania",
        }
    )
    if created:
        print(f"  + Établissement : {nom_normalise}")
    return etab


def get_or_create_programme(code):
    if not code:
        return None
    try:
        code_str = str(int(float(code)))
    except (ValueError, TypeError):
        return None
    
    libelles = {
        '319': 'Établissements de formation technique et professionnelle',
        '049': 'Direction Régionale (DRETFP)',
        '320': 'Programme 320',
        '321': 'Programme 321',
        '322': 'Programme 322',
    }
    
    programme, created = Programme.objects.get_or_create(
        code=code_str,
        defaults={'libelle': libelles.get(code_str, f'Programme {code_str}')}
    )
    return programme


def get_or_create_activite(programme, libelle):
    if not libelle or not programme:
        return None
    libelle = str(libelle).strip()[:300]
    if not libelle:
        return None
    activite, created = Activite.objects.get_or_create(
        programme=programme,
        libelle=libelle,
    )
    return activite


def get_or_create_sous_activite(activite, libelle):
    if not libelle or not activite:
        return None
    libelle = str(libelle).strip()[:300]
    if not libelle:
        return None
    sous_activite, created = SousActivite.objects.get_or_create(
        activite=activite,
        libelle=libelle,
    )
    return sous_activite


def get_or_create_produit(sous_activite, libelle, unite, cible):
    if not libelle or not sous_activite:
        return None
    libelle = str(libelle).strip()[:300]
    if not libelle:
        return None
    
    unite = str(unite).strip() if unite else 'Nombre'
    unites_valides = ['Nombre', 'Pack', 'Litre', 'Jour', 'Carte', 'Pièce', 'Sac', 'm3']
    if unite not in unites_valides:
        unite = 'Nombre'
    
    try:
        cible_val = Decimal(str(cible)) if cible else Decimal('0')
    except (ValueError, TypeError):
        cible_val = Decimal('0')
    
    produit, created = Produit.objects.get_or_create(
        sous_activite=sous_activite,
        libelle=libelle,
        defaults={'unite': unite, 'cible': cible_val}
    )
    return produit


def get_or_create_pcop(code, libelle=''):
    if not code:
        return None
    try:
        code_str = str(int(float(code)))
    except (ValueError, TypeError):
        code_str = str(code).strip()
    
    if not code_str:
        return None
    
    pcop, created = PCOP.objects.get_or_create(
        code=code_str[:10],
        defaults={'libelle': str(libelle).strip()[:300] if libelle else f'Code {code_str}'}
    )
    return pcop


# ============================================================
# IMPORTATION PRINCIPALE
# ============================================================

def importer():
    print("=" * 60)
    print("  IMPORTATION DU FICHIER EXCEL")
    print("=" * 60)
    print()
    
    if not os.path.exists(FICHIER_EXCEL):
        print(f"X ERREUR : Le fichier '{FICHIER_EXCEL}' n'existe pas.")
        return
    
    print(f"Ouverture du fichier : {FICHIER_EXCEL}")
    wb = openpyxl.load_workbook(FICHIER_EXCEL, data_only=True)
    
    # ⚠️ On compte UNIQUEMENT les vraies créations
    stats = {
        'etablissements': 0,
        'programmes': 0,
        'activites': 0,
        'sous_activites': 0,
        'produits': 0,
        'pcops': 0,
        'lignes': 0,
    }
    
    # Sets pour tracker les objets déjà vus (évite les faux compteurs)
    vus = {
        'programmes': set(),
        'activites': set(),
        'sous_activites': set(),
        'produits': set(),
        'pcops': set(),
        'lignes': set(),
    }
    
    for nom_feuille in FEUILLES_A_TRAITER:
        if nom_feuille not in wb.sheetnames:
            print(f"\n  ! Feuille '{nom_feuille}' introuvable, ignorée.")
            continue
        
        ws = wb[nom_feuille]
        print(f"\n--- Feuille : {nom_feuille} ({ws.max_row} lignes) ---")
        
        # Détection des colonnes
        headers = []
        for row in ws.iter_rows(min_row=1, max_row=1, values_only=True):
            headers = [str(h).strip().upper() if h else '' for h in row]
            break
        
        idx = {}
        for i, h in enumerate(headers):
            if ('SOUS ACTIVITE' in h or 'SOUS-ACTIVITE' in h 
                or 'SOUS ACTIVITÉ' in h or 'SOUS_ACTIVITE' in h):
                if 'sous_activite' not in idx:
                    idx['sous_activite'] = i
            elif 'PROGRAMME' in h and 'programme' not in idx:
                idx['programme'] = i
            elif ('ACTIVITE' in h or 'ACTIVITÉ' in h) and 'activite' not in idx:
                idx['activite'] = i
            elif 'PRODUIT' in h and 'produit' not in idx:
                idx['produit'] = i
            elif ('UNITE' in h or 'UNITÉ' in h) and 'unite' not in idx:
                idx['unite'] = i
            elif 'CIBLE' in h and 'QUANTIFI' in h and 'cible' not in idx:
                idx['cible'] = i
            elif 'CIBLE' in h and 'cible' not in idx:
                idx['cible'] = i
            elif ('DIRECTION' in h or 'ETABLISSEMENT' in h 
                  or 'ÉTABLISSEMENT' in h) and 'etablissement' not in idx:
                idx['etablissement'] = i
            elif 'SOURCE' in h and 'source' not in idx:
                idx['source'] = i
            elif ('PCOP_CODE' in h or ('PCOP' in h and 'CODE' in h)) and 'pcop_code' not in idx:
                idx['pcop_code'] = i
            elif ('PCOP_LIB' in h or ('PCOP' in h and 'LIB' in h)) and 'pcop_lib' not in idx:
                idx['pcop_lib'] = i
        
        print(f"  Colonnes : {idx}")
        
        for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
            if not row or len(row) < 4:
                continue
            
            def get_val(key):
                i = idx.get(key, -1)
                return row[i] if 0 <= i < len(row) else None
            
            programme_code = get_val('programme')
            activite_lib = get_val('activite')
            sous_activite_lib = get_val('sous_activite')
            produit_lib = get_val('produit')
            unite = get_val('unite')
            cible = get_val('cible')
            etab_nom = get_val('etablissement')
            source = get_val('source')
            pcop_code = get_val('pcop_code')
            pcop_lib = get_val('pcop_lib')
            
            if not any([activite_lib, produit_lib, sous_activite_lib]):
                continue
            
            if isinstance(programme_code, str) and programme_code.startswith('='):
                continue
            
            try:
                # Programme
                programme = get_or_create_programme(programme_code)
                if programme and programme.code not in vus['programmes']:
                    vus['programmes'].add(programme.code)
                    stats['programmes'] += 1
                
                # Activité
                activite = get_or_create_activite(programme, activite_lib)
                if activite and activite.id not in vus['activites']:
                    vus['activites'].add(activite.id)
                    stats['activites'] += 1
                
                # Sous-activité
                sous_activite = get_or_create_sous_activite(activite, sous_activite_lib)
                if sous_activite and sous_activite.id not in vus['sous_activites']:
                    vus['sous_activites'].add(sous_activite.id)
                    stats['sous_activites'] += 1
                
                # Produit
                produit = get_or_create_produit(sous_activite, produit_lib, unite, cible)
                if produit and produit.id not in vus['produits']:
                    vus['produits'].add(produit.id)
                    stats['produits'] += 1
                
                # PCOP
                pcop = get_or_create_pcop(pcop_code, pcop_lib)
                if pcop and pcop.code not in vus['pcops']:
                    vus['pcops'].add(pcop.code)
                    stats['pcops'] += 1
                
                # ✅ ÉTABLISSEMENT : LISTE BLANCHE STRICTE
                nom_normalise = normaliser_etablissement(etab_nom)
                etab = None
                if nom_normalise:
                    etab = get_or_create_etablissement(nom_normalise)
                    if etab:
                        stats['etablissements'] = Etablissement.objects.count()
                
                # Ligne budgétaire
                if etab and produit:
                    source_fin = 'FCE' if (source and 'FCE' in str(source).upper()) else 'RPI'
                    ligne, created = LigneBudgetaire.objects.get_or_create(
                        etablissement=etab,
                        produit=produit,
                        source_financement=source_fin,
                        defaults={'pcop': pcop, 'statut': 'Planifié'}
                    )
                    if created:
                        stats['lignes'] += 1
            
            except Exception as e:
                print(f"  ! Erreur ligne {row_num} ({nom_feuille}) : {e}")
                continue
    
    # Résumé
    print()
    print("=" * 60)
    print("  RÉSUMÉ DE L'IMPORTATION")
    print("=" * 60)
    print(f"  Établissements     : {stats['etablissements']}")
    print(f"  Programmes         : {stats['programmes']}")
    print(f"  Activités          : {stats['activites']}")
    print(f"  Sous-activités     : {stats['sous_activites']}")
    print(f"  Produits           : {stats['produits']}")
    print(f"  Codes PCOP         : {stats['pcops']}")
    print(f"  Lignes budgétaires : {stats['lignes']}")
    print()
    print("IMPORTATION TERMINÉE !")
    print("=" * 60)


if __name__ == '__main__':
    importer()