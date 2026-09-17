"""
Ajouter les nouveaux etablissements du nouveau canevas.
"""
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Etablissement


NOUVEAUX_ETABLISSEMENTS = [
    {
        'nom': 'CFP AMBOHIMITOMBO',
        'type_etablissement': 'CFP',
        'district': "Amoron'i Mania",
        'region': "Amoron'i Mania",
    },
    {
        'nom': 'LTP FAHIZAY',
        'type_etablissement': 'LTP',
        'district': "Amoron'i Mania",
        'region': "Amoron'i Mania",
    },
    {
        'nom': 'LTP KIANJANDRAKEFINA',
        'type_etablissement': 'LTP',
        'district': "Amoron'i Mania",
        'region': "Amoron'i Mania",
    },
    {
        'nom': 'CFP AMBATOFINANDRAHANA',
        'type_etablissement': 'CFP',
        'district': "Amoron'i Mania",
        'region': "Amoron'i Mania",
    },
    {
        'nom': 'LTP MANANDRIANA',
        'type_etablissement': 'LTP',
        'district': "Amoron'i Mania",
        'region': "Amoron'i Mania",
    },
    {
        'nom': 'DRETFP',
        'type_etablissement': 'INPF',
        'district': "Amoron'i Mania",
        'region': "Amoron'i Mania",
    },
]


def main():
    print("=" * 60)
    print("  AJOUT DES NOUVEAUX ETABLISSEMENTS")
    print("=" * 60)
    print()
    
    crees = 0
    existants = 0
    
    for data in NOUVEAUX_ETABLISSEMENTS:
        etab, created = Etablissement.objects.get_or_create(
            nom=data['nom'],
            defaults={
                'type_etablissement': data['type_etablissement'],
                'district': data['district'],
                'region': data['region'],
            }
        )
        if created:
            crees += 1
            print(f"[+] Cree : {etab.nom} ({etab.get_type_etablissement_display()})")
        else:
            existants += 1
            print(f"[=] Existe : {etab.nom}")
    
    print()
    print("=" * 60)
    print(f"  Crees    : {crees}")
    print(f"  Existants : {existants}")
    print(f"  Total     : {Etablissement.objects.count()}")
    print("=" * 60)


if __name__ == '__main__':
    main()