# Application de Gestion des Livraisons de Repas

Application web complète pour gérer les livraisons de repas à domicile, avec export CSV au format spécifique requis.

## Fonctionnalités

- **Gestion des convives** : CRUD complet avec toutes les informations (adresse, téléphone, régime, menu, tournée, jours)
- **Gestion des régimes** : Liste personnalisable des régimes alimentaires
- **Gestion des menus** : Liste des menus disponibles
- **Configuration des livraisons** : Définir quel jour de livraison correspond à chaque journée alimentaire
- **Commandes hebdomadaires** : Interface pour enregistrer les commandes de chaque convive par semaine
- **Export CSV** : Export au format requis (semaine complète ou journée spécifique)

## Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Télécharger l'application**
   - Téléchargez tous les fichiers de l'application dans un dossier

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Lancer l'application**
   ```bash
   python app.py
   ```

4. **Accéder à l'application**
   - Ouvrez votre navigateur web
   - Allez à l'adresse : `http://localhost:5000`

## Utilisation

### 1. Configuration initiale

#### a) Ajouter des régimes (optionnel)
- Menu : **Régimes**
- Régimes par défaut : Sans sel, Sans sucre, Sans sel ni sucre
- Vous pouvez ajouter vos propres régimes

#### b) Ajouter des menus (optionnel)
- Menu : **Menus**
- Ajoutez les types de menus disponibles

#### c) Configurer les jours de livraison
- Menu : **Configuration**
- Définissez pour chaque journée alimentaire (lundi à dimanche) quel jour elle sera livrée
- Exemple : Si vous livrez les repas du lundi ET du mardi le même jour (lundi), configurez :
  - Lundi → Lundi
  - Mardi → Lundi

### 2. Gestion des convives

- Menu : **Convives**
- Cliquez sur **"Nouveau convive"** pour ajouter un convive
- Remplissez toutes les informations :
  - Informations générales (nom, téléphone)
  - Adresse complète
  - Régime et menu
  - Tournée
  - Jours de consommation habituels (cochez les jours où le convive mange normalement)

### 3. Enregistrer les commandes

- Menu : **Commandes**
- Sélectionnez une date (n'importe quel jour de la semaine souhaitée)
- Cliquez sur **"Charger la semaine"**
- Cochez les cases correspondant aux jours où chaque convive commande
- Cliquez sur **"Enregistrer les commandes"**

### 4. Exporter le CSV

- Menu : **Export CSV**
- Choisissez le mode :
  - **Semaine complète** : Exporte toutes les livraisons de la semaine
  - **Journée spécifique** : Exporte uniquement les livraisons d'un jour
- Sélectionnez la date
- Cliquez sur **"Télécharger le CSV"**

## Format du CSV

Le fichier CSV exporté contient les colonnes suivantes :
- Action (toujours "CREER")
- Date de début souhaitée (date de livraison)
- Référence Bénéficiaire
- Nom Prénom ou Raison sociale
- Adresse complète (plusieurs colonnes)
- Nombre d'objets (nombre de repas)
- Téléphone
- Email (vide)
- Métadonnées (régime et dates de consommation)
- Paramètres Internes (tournée)

### Exemple de ligne CSV
```
CREER;23/02/2026;107_2-3;Mme AURIAT Janine;;;152 Av de la Marquisie ;;19600;ST PANTALEON DE LARCHE;;06.87.66.60.83 belle fille;2,00;05 55 86 08 46;;{'Regime':'','JourConso':'23/02/2026, 24/02/2026'};{'ROUND':'CS9830'}
```

## Logique de fonctionnement

### Jours de livraison
- Chaque **journée alimentaire** (jour où le repas est consommé) a un **jour de livraison** associé
- Cette configuration est globale pour tous les convives
- Exemple : Les repas du lundi et mardi peuvent être livrés le même jour (lundi)

### Commandes
- Les commandes sont enregistrées par semaine
- Chaque convive peut commander pour n'importe quel jour (parmi ses jours habituels)
- Le système regroupe automatiquement les repas par jour de livraison dans l'export

### Export
- **Mode Semaine** : Une ligne par convive et par jour de livraison avec tous les repas de ce jour
- **Mode Jour** : Uniquement les livraisons du jour sélectionné
- Le nombre d'objets correspond au nombre de repas livrés ce jour-là
- Les dates de consommation sont listées dans les métadonnées

## Hébergement en ligne

Pour mettre l'application en ligne, plusieurs options :

### Option 1 : Heroku (gratuit avec compte)
1. Créer un compte sur https://heroku.com
2. Installer Heroku CLI
3. Créer un fichier `Procfile` :
   ```
   web: python app.py
   ```
4. Déployer :
   ```bash
   heroku create nom-de-votre-app
   git init
   git add .
   git commit -m "Initial commit"
   git push heroku master
   ```

### Option 2 : Railway (simple et gratuit)
1. Créer un compte sur https://railway.app
2. Connecter votre dépôt GitHub
3. Railway détecte automatiquement Flask et déploie

### Option 3 : PythonAnywhere (gratuit)
1. Créer un compte sur https://www.pythonanywhere.com
2. Uploader les fichiers
3. Configurer l'application web dans le dashboard

### Option 4 : Hébergement mutualisé avec Python
- OVH, Ionos, O2switch (si support Python)
- Installer Python et Flask
- Configurer avec un serveur WSGI (Gunicorn)

## Structure des fichiers

```
livraisons-app/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── README.md             # Ce fichier
├── templates/            # Templates HTML
│   ├── base.html
│   ├── index.html
│   ├── convives.html
│   ├── regimes.html
│   ├── menus.html
│   ├── configuration.html
│   ├── commandes.html
│   └── export.html
└── static/
    └── css/
        └── style.css     # Styles CSS
```

## Base de données

- SQLite (fichier `livraisons.db` créé automatiquement)
- Parfaite pour 1-2 utilisateurs
- Pas de configuration requise
- Sauvegarde simple : copier le fichier `.db`

## Support et assistance

Si vous avez besoin d'aide :
1. Vérifiez que Python est bien installé : `python --version`
2. Vérifiez que Flask est installé : `pip list | grep Flask`
3. Consultez les logs dans le terminal où vous avez lancé l'application

## Migration depuis Access

Pour migrer vos données Access existantes :
1. Exportez vos tables Access en CSV
2. Utilisez l'interface web pour créer les convives, régimes, et menus
3. Ou créez un script Python pour importer automatiquement les CSV dans la base SQLite

## Améliorations futures possibles

- Authentification utilisateur
- Historique des exports
- Statistiques et rapports
- Envoi automatique par email
- API REST pour intégration avec d'autres systèmes
- Import CSV des convives
- Gestion multi-utilisateurs avec permissions

## Licence

Application développée pour un usage interne. Tous droits réservés.
