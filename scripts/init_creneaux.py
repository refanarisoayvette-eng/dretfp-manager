"""
Script pour initialiser les creneaux horaires.
Utilisation :
    python scripts/init_creneaux.py
"""

import os
import sys
import django
from datetime import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import CreneauHoraire


def main():
    print("=" * 60)
    print("  INITIALISATION DES CRENEAUX HORAIRES")
    print("=" * 60)
    print()
    
    creneaux = [
        ('Matin 1', time(8, 0), time(10, 0), 1),
        ('Matin 2', time(10, 15), time(12, 0), 2),
        ('Apres-midi 1', time(14, 0), time(16, 0), 3),
        ('Apres-midi 2', time(16, 15), time(18, 0), 4),
        ('Soiree', time(18, 30), time(20, 30), 5),
    ]
    
    for nom, debut, fin, ordre in creneaux:
        c, created = CreneauHoraire.objects.get_or_create(
            nom=nom,
            defaults={
                'heure_debut': debut,
                'heure_fin': fin,
                'ordre': ordre,
            }
        )
        statut = "✅ Cree" if created else "ℹ️  Existe deja"
        print(f"  {statut} : {c.nom} ({c.heure_debut.strftime('%H:%M')} - {c.heure_fin.strftime('%H:%M')})")
    
    print()
    print(f"  Total creneaux en base : {CreneauHoraire.objects.count()}")
    print()
    print("🎉 INITIALISATION TERMINEE !")


if __name__ == '__main__':
    main()