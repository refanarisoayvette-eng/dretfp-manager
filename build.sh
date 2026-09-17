#!/usr/bin/env bash
set -o errexit

echo "========================================================"
echo "  BUILD DRETFP MANAGER"
echo "========================================================"

echo "[1/6] Installation des dependances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[2/6] Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

echo "[3/6] Application des migrations..."
python manage.py migrate

echo "[4/6] Creation admin + etablissements..."
python manage.py shell << 'PYEOF'
from django.contrib.auth.models import User
from core.models import Etablissement

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@dretfp.mg', 'Dretfp2027!')
    print('OK : Admin cree')
else:
    print('OK : Admin existe')

ETABS = [
    ('CFP AMBOSITRA', 'CFP'), ('LTP AMBATOFINANDRAHANA', 'LTP'),
    ('CFP AMBOHIMITOMBO', 'CFP'), ('CFPF FANDRIANA', 'CFPF'),
    ('LTP AMBOSITRA', 'LTP'), ('LTPA FANDRIANA', 'LTPA'),
    ('LTP MIARINAVARATRA', 'LTP'), ('LTP FAHIZAY', 'LTP'),
    ('LTP KIANJANDRAKEFINA', 'LTP'), ('CFP FIADANANA FANDRIANA', 'CFP'),
    ('CFP AMBATOFINANDRAHANA', 'CFP'), ('LTP MANANDRIANA', 'LTP'),
    ('DRETFP', 'INPF'),
]

for nom, t in ETABS:
    Etablissement.objects.get_or_create(
        nom=nom,
        defaults={'type_etablissement': t, 'district': "Amoron'i Mania", 'region': "Amoron'i Mania"}
    )

print(f'Total etablissements : {Etablissement.objects.count()}')
PYEOF

echo "[5/6] Import du canevas PTA 2027..."
echo "Repertoire : $(pwd)"
echo "Fichiers dans donnees/source/ :"
ls -la donnees/source/ || echo "Dossier introuvable"

set +o errexit

if [ -f "donnees/source/PTA_2027.xlsx" ]; then
    echo "Fichier Excel trouve. Import en cours..."
    python scripts/import_pta_2027.py
    echo "Code retour import : $?"
else
    echo "ERREUR : donnees/source/PTA_2027.xlsx introuvable !"
fi

set -o errexit

echo "[6/6] Creation des comptes chefs..."
python manage.py shell << 'PYEOF'
from django.contrib.auth.models import User
from core.models import Profil, Etablissement

CHEFS = [
    ('chef_cfp_ambositra', 'CFP AMBOSITRA'),
    ('chef_ltp_ambatofinandrahana', 'LTP AMBATOFINANDRAHANA'),
    ('chef_cfp_ambohimitombo', 'CFP AMBOHIMITOMBO'),
    ('chef_cfpf_fandriana', 'CFPF FANDRIANA'),
    ('chef_ltp_ambositra', 'LTP AMBOSITRA'),
    ('chef_ltpa_fandriana', 'LTPA FANDRIANA'),
    ('chef_ltp_miarinavaratra', 'LTP MIARINAVARATRA'),
    ('chef_ltp_fahizay', 'LTP FAHIZAY'),
    ('chef_ltp_kianjandrakefina', 'LTP KIANJANDRAKEFINA'),
    ('chef_cfp_fiadanana', 'CFP FIADANANA FANDRIANA'),
    ('chef_cfp_ambatofinandrahana', 'CFP AMBATOFINANDRAHANA'),
    ('chef_ltp_manandriana', 'LTP MANANDRIANA'),
    ('chef_dretfp', 'DRETFP'),
]

for username, etab_nom in CHEFS:
    try:
        etab = Etablissement.objects.get(nom=etab_nom)
    except Etablissement.DoesNotExist:
        print(f'! {etab_nom} introuvable')
        continue

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': 'Chef',
            'last_name': etab.nom,
            'email': f'{username}@dretfp.mg',
            'is_staff': False,
            'is_active': True,
        }
    )
    if created:
        user.set_password('Dretfp2027!')
        user.save()
        print(f'+ {username}')

    Profil.objects.get_or_create(
        utilisateur=user,
        defaults={'role': 'CHEF_ETAB', 'etablissement': etab}
    )

print(f'Total chefs : {Profil.objects.filter(role="CHEF_ETAB").count()}')
PYEOF

echo "========================================================"
echo "  VERIFICATION FINALE"
echo "========================================================"
python manage.py shell << 'PYEOF'
from django.contrib.auth.models import User
from core.models import Etablissement, Produit, LigneBudgetaire, Profil

print(f"Etablissements : {Etablissement.objects.count()}")
print(f"Produits       : {Produit.objects.count()}")
print(f"Lignes         : {LigneBudgetaire.objects.count()}")
print(f"Admins         : {User.objects.filter(is_superuser=True).count()}")
print(f"Chefs          : {Profil.objects.filter(role='CHEF_ETAB').count()}")
PYEOF

echo "========================================================"
echo "  BUILD TERMINE !"
echo "========================================================"