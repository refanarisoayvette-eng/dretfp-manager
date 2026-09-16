# 📖 GUIDE DE DÉPLOIEMENT - DRETFP MANAGER

## 🎯 Objectif

Installer DRETFP Manager sur un serveur local de la DRETFP
pour qu'il soit accessible à tous les utilisateurs du réseau.

---

## 📋 Prérequis (sur le PC serveur DRETFP)

- Windows 10/11
- Python 3.12+
- PostgreSQL 16+
- Le dossier `dretfp_manager` (transféré depuis ton PC)
- Réseau local

---

## 📦 ÉTAPE 1 : Transférer le projet

1. Copier `dretfp_manager` sur une clé USB
2. Coller dans `C:\dretfp_manager` sur le serveur

**NE PAS transférer :**
- `venv/`
- `__pycache__/`
- `staticfiles/`
- `db.sqlite3`

**INCLURE impérativement :**
- `deploiement/`
- `core/`
- `config/`
- `scripts/`
- `templates/`
- `static/`
- `donnees/`
- `manage.py`

---

## 🔧 ÉTAPE 2 : Installer Python

1. Aller sur https://www.python.org/downloads/
2. **COCHER** ✅ "Add Python to PATH"
3. Installer

**Vérifier** dans Invite de commandes :
```cmd
python --version