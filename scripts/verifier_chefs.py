"""Verifier les comptes chefs crees."""
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Profil

print("=" * 70)
print("  LISTE DES CHEFS D'ETABLISSEMENT")
print("=" * 70)

chefs = Profil.objects.filter(role='CHEF_ETAB')
for i, p in enumerate(chefs, start=1):
    etab_nom = p.etablissement.nom if p.etablissement else '-'
    print(f"  {i}. {p.utilisateur.username:<30} -> {etab_nom}")

print("=" * 70)
print(f"  Total : {chefs.count()} chefs")
print("=" * 70)