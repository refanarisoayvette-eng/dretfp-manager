"""
Script pour creer les comptes des 7 chefs d'etablissement.
Mot de passe par defaut : Dretfp2027!

Utilisation :
    python scripts/creer_comptes_chefs.py
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profil, Etablissement


CHEFS = [
    {'username': 'chef_cfp_ambositra', 'etablissement': 'CFP AMBOSITRA'},
    {'username': 'chef_cfpf_fandriana', 'etablissement': 'CFPF FANDRIANA'},
    {'username': 'chef_cfp_fiadanana', 'etablissement': 'CFP FIADANANA FANDRIANA'},
    {'username': 'chef_ltp_ambositra', 'etablissement': 'LTP AMBOSITRA'},
    {'username': 'chef_ltp_miarinavaratra', 'etablissement': 'LTP MIARINAVARATRA'},
    {'username': 'chef_ltpa_fandriana', 'etablissement': 'LTPA FANDRIANA'},
    {'username': 'chef_ltpa_ambinda', 'etablissement': 'LTPA AMBINDA FANDRIANA'},
]


def main():
    print("=" * 60)
    print("  CREATION DES COMPTES CHEFS D'ETABLISSEMENT")
    print("=" * 60)
    print()
    
    mot_de_passe = 'Dretfp2027!'
    crees = 0
    existants = 0
    
    for chef in CHEFS:
        try:
            etab = Etablissement.objects.get(nom=chef['etablissement'])
        except Etablissement.DoesNotExist:
            print(f"! Etablissement '{chef['etablissement']}' non trouve - ignore")
            continue
        
        user, created = User.objects.get_or_create(
            username=chef['username'],
            defaults={
                'first_name': 'Chef',
                'last_name': etab.nom,
                'email': f"{chef['username']}@dretfp.mg",
                'is_staff': False,
                'is_active': True,
            }
        )
        
        if created:
            user.set_password(mot_de_passe)
            user.save()
            crees += 1
            print(f"[+] Cree : {chef['username']}")
        else:
            existants += 1
            print(f"[=] Existe : {chef['username']}")
        
        Profil.objects.get_or_create(
            utilisateur=user,
            defaults={'role': 'CHEF_ETAB', 'etablissement': etab}
        )
        
        print(f"    -> Role : Chef d'etablissement")
        print(f"    -> Etablissement : {etab.nom}")
        print()
    
    print("=" * 60)
    print(f"  Comptes crees    : {crees}")
    print(f"  Comptes existants : {existants}")
    print("=" * 60)
    print()
    print(f"  MOT DE PASSE : {mot_de_passe}")
    print()


if __name__ == '__main__':
    main()