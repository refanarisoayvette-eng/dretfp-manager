#!/usr/bin/env bash
set -o errexit

echo "========================================================"
echo "  BUILD DRETFP MANAGER"
echo "========================================================"

echo "[1/5] Installation des dependances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[2/5] Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

echo "[3/5] Application des migrations..."
python manage.py migrate

echo "[4/5] Creation admin + etablissements..."
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

echo "[5/5] Import du canevas PTA 2027..."
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

python manage.py shell << 'PYEOF'
from core.models import Etablissement, Produit, LigneBudgetaire
print("=" * 50)
print(f"Etablissements : {Etablissement.objects.count()}")
print(f"Produits       : {Produit.objects.count()}")
print(f"Lignes         : {LigneBudgetaire.objects.count()}")
print("=" * 50)
PYEOF

echo "BUILD TERMINE !"