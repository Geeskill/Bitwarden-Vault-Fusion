import json
import sys

# --- COULEURS ET STYLES ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f" {text}")
    print(f"{'='*60}{Colors.ENDC}")

def get_essential_signature(item):
    """
    Signature unique : Nom + User + Password + URL.
    """
    name = item.get('name', '').strip()
    
    login = item.get('login', {})
    username = login.get('username', '')
    if username is None: username = ""
    
    password = login.get('password', '')
    if password is None: password = ""
    
    uris = login.get('uris', [])
    first_url = ""
    if uris and len(uris) > 0:
        first_url = uris[0].get('uri', '')

    return (name, username, password, first_url)

def main():
    if len(sys.argv) != 3:
        print(f"{Colors.FAIL}Usage: python3 visual_merge.py fichier1.json fichier2.json{Colors.ENDC}")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    output_file = "fusion_finale.json"

    print_header("?? DÉMARRAGE DE LA FUSION INTELLIGENTE")
    print(f"{Colors.CYAN}?? Fichier Base   : {file1_path}")
    print(f"?? Fichier Apport : {file2_path}{Colors.ENDC}")

    # 1. Chargement
    try:
        data1 = json.load(open(file1_path, 'r', encoding='utf-8'))
        data2 = json.load(open(file2_path, 'r', encoding='utf-8'))
    except Exception as e:
        print(f"{Colors.FAIL}? Erreur de lecture : {e}{Colors.ENDC}")
        sys.exit(1)

    items1 = data1.get('items', [])
    items2 = data2.get('items', [])

    merged_items = []
    seen_signatures = set()
    names_in_base = set()

    # Stats
    count_base = 0
    count_added = 0
    count_skipped = 0
    conflicts = []

    # 2. Traitement du Fichier 1 (Base)
    print(f"\n{Colors.BLUE}--- Analyse du fichier de base ({len(items1)} entrées) ---{Colors.ENDC}")
    for item in items1:
        sig = get_essential_signature(item)
        seen_signatures.add(sig)
        names_in_base.add(item.get('name'))
        merged_items.append(item)
        count_base += 1
    
    print(f"? {count_base} entrées chargées depuis la base.")

    # 3. Fusion du Fichier 2
    print(f"\n{Colors.BLUE}--- Comparaison et Fusion avec le fichier d'apport ---{Colors.ENDC}")
    
    doublons_list = [] # Pour affichage
    added_list = []    # Pour affichage

    for item in items2:
        sig = get_essential_signature(item)
        name = item.get('name', 'Sans nom')

        if sig in seen_signatures:
            # DOUBLON PARFAIT
            count_skipped += 1
            doublons_list.append(name)
        else:
            # NOUVEAU ou DIFFÉRENT
            count_added += 1
            merged_items.append(item)
            added_list.append(name)
            
            # Vérifier si c'est un conflit (Même nom mais contenu différent)
            if name in names_in_base:
                user = item.get('login', {}).get('username', 'N/A')
                conflicts.append(f"{name} (User: {user})")

    # 4. Affichage des détails
    if doublons_list:
        print(f"\n{Colors.WARNING}??  DOUBLONS IGNORÉS (Identiques à 100%) : {len(doublons_list)}{Colors.ENDC}")
        # On n'affiche que les 10 premiers pour ne pas spammer si y'en a 300
        for d in doublons_list[:10]:
            print(f"   ???  {d}")
        if len(doublons_list) > 10:
            print(f"   ... et {len(doublons_list)-10} autres.")

    if added_list:
        print(f"\n{Colors.GREEN}? NOUVELLES ENTRÉES AJOUTÉES : {len(added_list)}{Colors.ENDC}")
        for a in added_list:
            if any( c.startswith(a) for c in conflicts):
                print(f"   ??  {a} {Colors.FAIL}[Conflit potentiel : Mot de passe différent]{Colors.ENDC}")
            else:
                print(f"   ? {a}")

    # 5. Sauvegarde
    final_data = data1
    final_data['items'] = merged_items
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=2)

    # 6. Résumé Final
    print_header("RÉSULTAT FINAL")
    print(f"?? Base initiale :      {Colors.BOLD}{len(items1)}{Colors.ENDC}")
    print(f"?? Apport fichier 2 :   {Colors.BOLD}{len(items2)}{Colors.ENDC}")
    print(f"-----------------------------------")
    print(f"{Colors.WARNING}?? Doublons supprimés : {count_skipped}{Colors.ENDC}")
    print(f"{Colors.GREEN}?? Ajouts réels :       {count_added}{Colors.ENDC}")
    print(f"-----------------------------------")
    print(f"{Colors.CYAN}?? TOTAL FINAL :        {len(merged_items)} entrées{Colors.ENDC}")
    
    if conflicts:
        print(f"\n{Colors.FAIL}{Colors.BOLD}??  ATTENTION : {len(conflicts)} entrées ont le même nom mais un mot de passe différent.{Colors.ENDC}")
        print("Elles ont été AJOUTÉES. Vous aurez donc 2 lignes pour ces sites dans Bitwarden.")
        print("Il faudra les vérifier manuellement après import.")

    print(f"\n?? Fichier généré : {Colors.BOLD}{output_file}{Colors.ENDC}")

if __name__ == "__main__":
    main()
