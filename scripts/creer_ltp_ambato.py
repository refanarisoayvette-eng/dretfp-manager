"""Creer l'etablissement LTP AMBATOFINANDRAHANA."""
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Etablissement

etab, created = Etablissement.objects.get_or_create(
    nom='LTP AMBATOFINANDRAHANA',
    defaults={
        'type_etablissement': 'LTP',
        'district': "Amoron'i Mania",
        'region': "Amoron'i Mania",
    }
)

if created:
    print(f"[+] Cree : {etab.nom}")
else:
    print(f"[=] Existe : {etab.nom}")

print(f"\nTotal etablissements : {Etablissement.objects.count()}")