#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Creer automatiquement l'admin
python manage.py shell << 'EOF'
from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@dretfp.mg', 'Dretfp2027!')
    print('OK : Admin cree')
else:
    print('OK : Admin existe deja')
EOF

echo "BUILD TERMINE !"