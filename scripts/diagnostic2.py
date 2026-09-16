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

for nom in wb.sheetnames:
    ws = wb[nom]
    # Trouver index de la colonne ETABLISSEMENT
    headers = list(ws.iter_rows(min_row=1, max_row=1, values_only=True))[0]
    idx_etab = None
    for i, h in enumerate(headers):
        if h and ('DIRECTION' in str(h).upper() or 'ETABLISSEMENT' in str(h).upper()):
            idx_etab = i
            break
    
    if idx_etab is None:
        continue
    
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row or len(row) <= idx_etab:
            continue
        val = row[idx_etab]
        if not val:
            continue
        val_str = str(val).strip()
        upper = val_str.upper()
        
        if any(upper.startswith(p) for p in prefixes) and any(v in upper for v in villes):
            etabs_trouves.add(val_str)

print("=" * 60)
print(f"  ÉTABLISSEMENTS VALIDES TROUVÉS : {len(etabs_trouves)}")
print("=" * 60)
for e in sorted(etabs_trouves):
    print(f"  - {e}")