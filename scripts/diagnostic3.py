import os, sys, django, openpyxl

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

FICHIER_EXCEL = 'FUSION_CANEVAS_TPA_2027.xlsx'
wb = openpyxl.load_workbook(FICHIER_EXCEL, data_only=True)

villes = ['AMBATOFINANDRAHANA', 'AMBOSITRA', 'FANDRIANA',
          'MIARINAVARATRA', 'AMBOHIMITOMBO', 'AMBINDA']
prefixes = ['LTP ', 'LTPA ', 'CFP ', 'CFPF ', 'INPF ', 'CNFPPSH ']

etabs_trouves = set()

# Écrire dans un fichier
with open('diagnostic_etabs.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 60 + "\n")
    f.write("  DIAGNOSTIC DES ÉTABLISSEMENTS\n")
    f.write("=" * 60 + "\n\n")
    
    for nom in wb.sheetnames:
        ws = wb[nom]
        headers = list(ws.iter_rows(min_row=1, max_row=1, values_only=True))[0]
        idx_etab = None
        for i, h in enumerate(headers):
            if h and ('DIRECTION' in str(h).upper() or 'ETABLISSEMENT' in str(h).upper()):
                idx_etab = i
                break
        
        if idx_etab is None:
            f.write(f"\n[{nom}] : Pas de colonne ETABLISSEMENT\n")
            continue
        
        f.write(f"\n[{nom}] colonne {idx_etab}\n")
        
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row or len(row) <= idx_etab:
                continue
            val = row[idx_etab]
            if not val:
                continue
            val_str = str(val).strip()
            upper = val_str.upper()
            
            f.write(f"  → '{val_str}'\n")
            
            if any(upper.startswith(p) for p in prefixes) and any(v in upper for v in villes):
                etabs_trouves.add(val_str)
    
    f.write("\n" + "=" * 60 + "\n")
    f.write(f"  ÉTABLISSEMENTS VALIDES : {len(etabs_trouves)}\n")
    f.write("=" * 60 + "\n")
    for e in sorted(etabs_trouves):
        f.write(f"  - {e}\n")

print(f"✅ Diagnostic écrit dans diagnostic_etabs.txt")
print(f"   {len(etabs_trouves)} établissements valides trouvés.")