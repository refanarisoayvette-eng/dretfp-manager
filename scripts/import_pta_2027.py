"""
Import du nouveau canevas PTA 2027 (un seul fichier, une seule feuille).
Gere les cellules fusionnees et les differents formats d'etablissement.

Utilisation :
    python scripts/import_pta_2027.py
"""

import os
import sys
import django
import openpyxl
import decimal
import re
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import (
    Etablissement, Programme, Activite, SousActivite,
    Produit, PCOP, LigneBudgetaire
)


FICHIER_EXCEL = 'donnees/source/PTA_2027.xlsx'
FEUILLE = "DRETFP AMORON'i MANIA"


# Liste blanche stricte des etablissements valides
ETABLISSEMENTS_VALIDES = [
    'CFP AMBOSITRA',
    'LTP AMBATOFINANDRAHANA',
    'CFP AMBOHIMITOMBO',
    'CFPF FANDRIANA',
    'LTP AMBOSITRA',
    'LTPA FANDRIANA',
    'LTP MIARINAVARATRA',
    'LTP FAHIZAY',
    'LTP KIANJANDRAKEFINA',
    'CFP FIADANANA FANDRIANA',
    'CFP AMBATOFINANDRAHANA',
    'LTP MANANDRIANA',
    'DRETFP',
]


def normaliser_etablissement(val):
    """Retourne le nom normalise s'il est valide, sinon None."""
    if not val:
        return None
    val_str = str(val).strip()
    if not val_str or len(val_str) < 3:
        return None
    
    # Comparaison case-insensitive
    val_upper = val_str.upper()
    for etab in ETABLISSEMENTS_VALIDES:
        if etab.upper() == val_upper:
            return etab
        # Tolere les variantes (sans espaces, etc.)
        if etab.upper().replace(' ', '') == val_upper.replace(' ', ''):
            return etab
    
    return None


def detecter_fin_donnees(ws):
    """Detecte la derniere ligne avec des donnees."""
    derniere = 1
    for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
        if row and any(v is not None and str(v).strip() for v in row):
            derniere = row_num
    return derniere


def main():
    print("=" * 70)
    print("  IMPORT DU CANEVAS PTA 2027")
    print("=" * 70)
    print()
    
    if not os.path.exists(FICHIER_EXCEL):
        print(f"X ERREUR : '{FICHIER_EXCEL}' n'existe pas.")
        return
    
    print(f"Fichier : {FICHIER_EXCEL}")
    wb = openpyxl.load_workbook(FICHIER_EXCEL, data_only=True)
    
    if FEUILLE not in wb.sheetnames:
        print(f"X Feuille '{FEUILLE}' introuvable.")
        print(f"  Feuilles disponibles : {wb.sheetnames}")
        return
    
    ws = wb[FEUILLE]
    derniere = detecter_fin_donnees(ws)
    print(f"Feuille : {FEUILLE}")
    print(f"Lignes  : {derniere} (sur {ws.max_row})")
    print()
    
    # Stats
    stats = {
        'etablissements': set(),
        'programmes': set(),
        'activites': set(),
        'sous_activites': set(),
        'produits': 0,
        'pcops': set(),
        'lignes': 0,
        'ignorees': 0,
    }
    
    # Memoire pour cellules fusionnees
    dernier_programme = None
    derniere_activite = None
    derniere_sous_activite = None
    derniere_zone = None
    dernier_etab = None
    
    for row_num, row in enumerate(ws.iter_rows(min_row=2, max_row=derniere, values_only=True), start=2):
        if not row or len(row) < 8:
            stats['ignorees'] += 1
            continue
        
        # Colonnes : A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7, I=8, J=9, K=10, L=11
        programme_val = row[0] if len(row) > 0 else None
        activite_val = row[1] if len(row) > 1 else None
        sous_activite_val = row[2] if len(row) > 2 else None
        produit_val = row[3] if len(row) > 3 else None
        zone_val = row[4] if len(row) > 4 else None
        unite_val = row[5] if len(row) > 5 else None
        cible_val = row[6] if len(row) > 6 else None
        etab_val = row[7] if len(row) > 7 else None
        source_val = row[8] if len(row) > 8 else None
        fce_val = row[9] if len(row) > 9 else None
        pcop_code_val = row[10] if len(row) > 10 else None
        pcop_lib_val = row[11] if len(row) > 11 else None
        
        # Heriter des valeurs precedentes (cellules fusionnees)
        if programme_val:
            dernier_programme = programme_val
        else:
            programme_val = dernier_programme
        
        if activite_val:
            derniere_activite = activite_val
        else:
            activite_val = derniere_activite
        
        if sous_activite_val:
            derniere_sous_activite = sous_activite_val
        else:
            sous_activite_val = derniere_sous_activite
        
        if zone_val:
            derniere_zone = zone_val
        else:
            zone_val = derniere_zone
        
        if etab_val:
            dernier_etab = etab_val
        else:
            etab_val = dernier_etab
        
        # Ignorer les lignes vides
        if not any([activite_val, produit_val, sous_activite_val]):
            stats['ignorees'] += 1
            continue
        
        # Ignorer les formules SUM
        if isinstance(programme_val, str) and programme_val.startswith('='):
            continue
        
 # ⚠️ DETECTION INTELLIGENTE DE L'ETABLISSEMENT
        # Le canevas a parfois des colonnes decalees
        # On cherche dans TOUTES les colonnes
        nom_etab = None
        
        for val in [etab_val, zone_val, source_val, fce_val, pcop_code_val, pcop_lib_val,
                    produit_val, unite_val, cible_val]:
            nom_etab = normaliser_etablissement(val)
            if nom_etab:
                break
        
        if not nom_etab:
            stats['ignorees'] += 1
            continue
        
        try:
            # Etablissement
            etab = Etablissement.objects.get(nom=nom_etab)
            stats['etablissements'].add(etab.nom)
            
            # Programme
            code_str = None
            if programme_val:
                try:
                    code_str = str(int(float(programme_val)))
                except (ValueError, TypeError):
                    code_str = None
            
            if not code_str:
                stats['ignorees'] += 1
                continue
            
            programme, _ = Programme.objects.get_or_create(
                code=code_str,
                defaults={'libelle': f'Programme {code_str}'}
            )
            stats['programmes'].add(code_str)
            
            # Activite
            if not activite_val:
                stats['ignorees'] += 1
                continue
            
            activite, _ = Activite.objects.get_or_create(
                programme=programme,
                libelle=str(activite_val).strip()[:300]
            )
            stats['activites'].add(activite.id)
            
            # Si produit vide mais sous_activite rempli -> sous_activite = produit
            if not produit_val and sous_activite_val:
                produit_val = sous_activite_val
                sous_activite_val = None
            
            # Sous-activite
            if sous_activite_val:
                sous_act, _ = SousActivite.objects.get_or_create(
                    activite=activite,
                    libelle=str(sous_activite_val).strip()[:300]
                )
            else:
                sous_act, _ = SousActivite.objects.get_or_create(
                    activite=activite,
                    libelle="General"
                )
            stats['sous_activites'].add(sous_act.id)
            
            # Produit
            if not produit_val:
                stats['ignorees'] += 1
                continue
            
            unite = str(unite_val).strip() if unite_val else 'Nombre'
            if unite not in ['Nombre', 'Pack', 'Litre', 'Jour', 'Carte', 'Piece', 'Sac', 'm3']:
                unite = 'Nombre'

            cible = Decimal('0')
            if cible_val:
                try:
                    # Extraire le premier nombre trouve dans la chaine
                    import re
                    cible_str = str(cible_val).strip()
                    match = re.search(r'\d+\.?\d*', cible_str)
                    if match:
                        cible = Decimal(match.group())
                except (ValueError, TypeError, decimal.InvalidOperation):
                    cible = Decimal('0')
            
            produit, created = Produit.objects.get_or_create(
                sous_activite=sous_act,
                libelle=str(produit_val).strip()[:300],
                defaults={'unite': unite, 'cible': cible}
            )
            if created:
                stats['produits'] += 1
            
            # PCOP
            pcop = None
            if pcop_code_val:
                try:
                    pc_str = str(int(float(pcop_code_val)))
                except (ValueError, TypeError):
                    pc_str = str(pcop_code_val).strip()
                
                pcop, _ = PCOP.objects.get_or_create(
                    code=pc_str[:10],
                    defaults={'libelle': str(pcop_lib_val)[:300] if pcop_lib_val else f'Code {pc_str}'}
                )
                stats['pcops'].add(pcop.code)
            
            # Source financement
            src_upper = str(source_val).upper() if source_val else ''
            fce_upper = str(fce_val).upper() if fce_val else ''
            
            if 'FCE' in fce_upper or 'FCE' in src_upper:
                source_fin = 'FCE'
            else:
                source_fin = 'RPI'
            
            # Ligne budgetaire
            ligne, l_created = LigneBudgetaire.objects.get_or_create(
                etablissement=etab,
                produit=produit,
                source_financement=source_fin,
                defaults={'pcop': pcop, 'statut': 'Planifie'}
            )
            if l_created:
                stats['lignes'] += 1
        
        except Exception as e:
            print(f"  ! Erreur ligne {row_num} : {e}")
            continue
    
    # Resume
    print()
    print("=" * 70)
    print("  RESUME DE L'IMPORTATION")
    print("=" * 70)
    print(f"  Etablissements     : {len(stats['etablissements'])}")
    print(f"  Programmes         : {len(stats['programmes'])}")
    print(f"  Activites          : {len(stats['activites'])}")
    print(f"  Sous-activites     : {len(stats['sous_activites'])}")
    print(f"  Nouveaux produits  : {stats['produits']}")
    print(f"  Codes PCOP         : {len(stats['pcops'])}")
    print(f"  Nouvelles lignes   : {stats['lignes']}")
    print(f"  Lignes ignorees    : {stats['ignorees']}")
    print()
    print(f"  📊 ETAT FINAL EN BASE :")
    print(f"     Etablissements     : {Etablissement.objects.count()}")
    print(f"     Programmes         : {Programme.objects.count()}")
    print(f"     Activites          : {Activite.objects.count()}")
    print(f"     Sous-activites     : {SousActivite.objects.count()}")
    print(f"     Produits           : {Produit.objects.count()}")
    print(f"     Codes PCOP         : {PCOP.objects.count()}")
    print(f"     Lignes budgetaires : {LigneBudgetaire.objects.count()}")
    print()
    print("🎉 IMPORTATION TERMINEE !")
    print("=" * 70)


if __name__ == '__main__':
    main()