# Guide de Migration depuis MS Access

Ce guide vous aide à migrer votre application Access existante vers l'application web.

## Étape 1 : Exporter les données depuis Access

### Option A : Export manuel (recommandé pour débuter)

1. **Ouvrir votre base Access**
2. **Exporter chaque table en CSV** :
   - Table Convives → Clic droit → Exporter → Fichier texte → CSV
   - Table Régimes → Exporter en CSV
   - Table Menus → Exporter en CSV

### Option B : Script VBA d'export (pour gros volumes)

Copiez ce code dans un module VBA dans Access :

```vba
Sub ExporterToutesLesTables()
    Dim db As DAO.Database
    Dim tdf As DAO.TableDef
    Dim cheminExport As String
    
    ' Définir le chemin d'export
    cheminExport = "C:\Export\"
    
    ' Créer le dossier si nécessaire
    If Dir(cheminExport, vbDirectory) = "" Then
        MkDir cheminExport
    End If
    
    Set db = CurrentDb
    
    ' Parcourir toutes les tables
    For Each tdf In db.TableDefs
        ' Ignorer les tables système
        If Left(tdf.Name, 4) <> "MSys" Then
            ' Exporter en CSV
            DoCmd.TransferText acExportDelim, , tdf.Name, _
                cheminExport & tdf.Name & ".csv", True
            Debug.Print "Exporté : " & tdf.Name
        End If
    Next tdf
    
    MsgBox "Export terminé dans " & cheminExport
End Sub
```

## Étape 2 : Importer les données dans l'application web

### Méthode 1 : Import manuel (petits volumes < 50 convives)

1. **Démarrer l'application web**
2. **Créer les régimes** :
   - Menu Régimes → Ajouter chaque régime
3. **Créer les menus** :
   - Menu Menus → Ajouter chaque menu
4. **Créer les convives** :
   - Menu Convives → Nouveau convive
   - Remplir les informations depuis votre CSV

### Méthode 2 : Script d'import automatique (volumes > 50 convives)

Créez un fichier `import_csv.py` :

```python
import csv
import sys
from app import app, db, Convive, Regime, Menu

def importer_regimes(fichier_csv):
    """Importer les régimes depuis un CSV"""
    with app.app_context():
        with open(fichier_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                regime = Regime(nom=row['nom'])
                db.session.add(regime)
        db.session.commit()
        print(f"✓ Régimes importés depuis {fichier_csv}")

def importer_menus(fichier_csv):
    """Importer les menus depuis un CSV"""
    with app.app_context():
        with open(fichier_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                menu = Menu(nom=row['nom'])
                db.session.add(menu)
        db.session.commit()
        print(f"✓ Menus importés depuis {fichier_csv}")

def importer_convives(fichier_csv):
    """Importer les convives depuis un CSV"""
    with app.app_context():
        # Charger les régimes et menus existants
        regimes = {r.nom: r.id for r in Regime.query.all()}
        menus = {m.nom: m.id for m in Menu.query.all()}
        
        with open(fichier_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convertir O/N en booléens
                def oui_non_to_bool(val):
                    return val.upper() == 'O' if val else False
                
                convive = Convive(
                    nom_prenom=row['nom_prenom'],
                    lieu_remise=row.get('lieu_remise', ''),
                    numero_boite=row.get('numero_boite', ''),
                    numero_voie=row.get('numero_voie', ''),
                    complement_commune=row.get('complement_commune', ''),
                    code_postal=row.get('code_postal', ''),
                    localite=row.get('localite', ''),
                    indication_acces=row.get('indication_acces', ''),
                    indications_complementaires=row.get('indications_complementaires', ''),
                    telephone=row.get('telephone', ''),
                    lundi=oui_non_to_bool(row.get('lundi', '')),
                    mardi=oui_non_to_bool(row.get('mardi', '')),
                    mercredi=oui_non_to_bool(row.get('mercredi', '')),
                    jeudi=oui_non_to_bool(row.get('jeudi', '')),
                    vendredi=oui_non_to_bool(row.get('vendredi', '')),
                    samedi=oui_non_to_bool(row.get('samedi', '')),
                    dimanche=oui_non_to_bool(row.get('dimanche', '')),
                    regime_id=regimes.get(row.get('regime', '')),
                    menu_id=menus.get(row.get('menu', '')),
                    tournee=row.get('tournee', ''),
                    actif=oui_non_to_bool(row.get('actif', 'O'))
                )
                db.session.add(convive)
        
        db.session.commit()
        print(f"✓ Convives importés depuis {fichier_csv}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python import_csv.py <type> <fichier.csv>")
        print("Types disponibles : regimes, menus, convives")
        sys.exit(1)
    
    type_import = sys.argv[1]
    fichier = sys.argv[2]
    
    if type_import == 'regimes':
        importer_regimes(fichier)
    elif type_import == 'menus':
        importer_menus(fichier)
    elif type_import == 'convives':
        importer_convives(fichier)
    else:
        print(f"Type inconnu : {type_import}")
        sys.exit(1)
```

**Utilisation du script d'import :**

```bash
# Importer les régimes
python import_csv.py regimes regimes.csv

# Importer les menus
python import_csv.py menus menus.csv

# Importer les convives
python import_csv.py convives convives.csv
```

## Étape 3 : Vérification

1. **Ouvrir l'application** : http://localhost:5000
2. **Vérifier les régimes** : Menu Régimes
3. **Vérifier les menus** : Menu Menus
4. **Vérifier les convives** : Menu Convives
5. **Configurer les jours de livraison** : Menu Configuration

## Étape 4 : Test complet

1. **Créer une commande test** :
   - Menu Commandes
   - Sélectionner une semaine
   - Cocher quelques cases
   - Enregistrer

2. **Tester l'export** :
   - Menu Export CSV
   - Mode "Semaine complète"
   - Télécharger le CSV
   - Vérifier le format

## Mapping des champs Access → Application Web

| Champ Access | Champ Application | Type |
|-------------|------------------|------|
| Nom | nom_prenom | Texte (38) |
| Adresse1 | numero_voie | Texte (38) |
| Adresse2 | complement_commune | Texte (38) |
| CP | code_postal | Texte (5) |
| Ville | localite | Texte (38) |
| Tel | telephone | Texte (10) |
| Regime | regime_id | Relation |
| Menu | menu_id | Relation |
| Tournee | tournee | Texte (5) |
| Lundi | lundi | O/N → Bool |
| Mardi | mardi | O/N → Bool |
| ... | ... | ... |
| Actif | actif | O/N → Bool |

## Problèmes courants et solutions

### Problème : Encodage des caractères
**Solution** : Lors de l'export depuis Access, choisir UTF-8 comme encodage

### Problème : Séparateur CSV
**Solution** : Access peut utiliser ";" ou ",". Adapter le script d'import si nécessaire

### Problème : Dates
**Solution** : L'application web utilise le format ISO (YYYY-MM-DD)

### Problème : Valeurs O/N
**Solution** : Le script d'import convertit automatiquement O → True, N → False

## Différences importantes Access vs Web

| Aspect | MS Access | Application Web |
|--------|-----------|----------------|
| Utilisateurs simultanés | 1-5 (limité) | Illimité |
| Accès | Local/Réseau | Internet |
| Installation | Office requis | Navigateur uniquement |
| Sauvegarde | Fichier .accdb | Base SQLite |
| Formulaires | Access forms | HTML/CSS/JS |
| Rapports | Access reports | Export CSV |

## Avantages de la migration

✅ **Accessibilité** : Utilisable depuis n'importe quel appareil avec navigateur  
✅ **Modernité** : Interface moderne et responsive  
✅ **Fiabilité** : Pas de corruption de fichier Access  
✅ **Évolutivité** : Facile d'ajouter de nouvelles fonctionnalités  
✅ **Multi-plateforme** : Windows, Mac, Linux, Mobile  

## Besoin d'aide ?

Si vous rencontrez des difficultés lors de la migration, contactez-moi avec :
- Vos fichiers CSV exportés
- Les messages d'erreur éventuels
- Des captures d'écran de votre structure Access

Je peux créer un script d'import sur-mesure pour votre cas spécifique.
