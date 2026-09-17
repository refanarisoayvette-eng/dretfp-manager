"""Verifier quels etablissements ont ete importes."""
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Etablissement, LigneBudgetaire


TOUS_ETABS = [
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

print("=" * 70)
print("  VERIFICATION DES ETABLISSEMENTS IMPORTES")
print("=" * 70)
print()

for nom in TOUS_ETABS:
    try:
        etab = Etablissement.objects.get(nom=nom)
        nb_lignes = LigneBudgetaire.objects.filter(etablissement=etab).count()
        if nb_lignes > 0:
            print(f"  OK    {nom:<35} : {nb_lignes} lignes")
        else:
            print(f"  VIDE  {nom:<35} : 0 ligne")
    except Etablissement.DoesNotExist:
        print(f"  ABSENT {nom}")

print()
print("=" * 70)