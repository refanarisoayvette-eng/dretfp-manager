"""
Script pour creer des formateurs de test.
"""
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profil, Etablissement


def main():
    etab = Etablissement.objects.first()
    
    formateurs = [
        ('prof_rakoto', 'Rakoto', 'Jean', '0341234567'),
        ('prof_rasoa', 'Rasoa', 'Marie', '0342345678'),
        ('prof_randria', 'Randria', 'Paul', '0343456789'),
    ]
    
    for username, nom, prenom, tel in formateurs:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': prenom,
                'last_name': nom,
                'email': f'{username}@dretfp.mg',
                'is_staff': False,
            }
        )
        if created:
            user.set_password('Dretfp2027!')
            user.save()
            print(f"✅ Utilisateur cree : {username}")
        
        profil, p_created = Profil.objects.get_or_create(
            utilisateur=user,
            defaults={'role': 'FORMATEUR', 'etablissement': etab, 'telephone': tel}
        )
        if not p_created:
            profil.role = 'FORMATEUR'
            profil.etablissement = etab
            profil.telephone = tel
            profil.save()
        
        print(f"   → Profil : {profil.get_role_display()}")
    
    print(f"\n🎉 {Profil.objects.filter(role='FORMATEUR').count()} formateur(s) en base")
    print("   Mot de passe : Dretfp2027!")


if __name__ == '__main__':
    main()