from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json
import csv
import io
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livraisons.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modèles de base de données
class Convive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_prenom = db.Column(db.String(38), nullable=False)
    lieu_remise = db.Column(db.String(38))
    numero_boite = db.Column(db.String(38))
    numero_voie = db.Column(db.String(38))
    complement_commune = db.Column(db.String(38))
    code_postal = db.Column(db.String(5))
    localite = db.Column(db.String(38))
    indication_acces = db.Column(db.String(90))
    indications_complementaires = db.Column(db.String(90))
    telephone = db.Column(db.String(10))
    lundi = db.Column(db.Boolean, default=False)
    mardi = db.Column(db.Boolean, default=False)
    mercredi = db.Column(db.Boolean, default=False)
    jeudi = db.Column(db.Boolean, default=False)
    vendredi = db.Column(db.Boolean, default=False)
    samedi = db.Column(db.Boolean, default=False)
    dimanche = db.Column(db.Boolean, default=False)
    regime_id = db.Column(db.Integer, db.ForeignKey('regime.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    tournee = db.Column(db.String(5))
    actif = db.Column(db.Boolean, default=True)
    
    regime = db.relationship('Regime', backref='convives')
    menu = db.relationship('Menu', backref='convives')
    commandes = db.relationship('Commande', backref='convive', cascade='all, delete-orphan')

class Regime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(15), unique=True, nullable=False)

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(15), unique=True, nullable=False)

class ConfigurationLivraison(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jour_alimentaire = db.Column(db.String(10), unique=True, nullable=False)  # lundi, mardi, etc.
    jour_livraison = db.Column(db.String(10), nullable=False)  # lundi, mardi, etc.

class Commande(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    convive_id = db.Column(db.Integer, db.ForeignKey('convive.id'), nullable=False)
    date_commande = db.Column(db.Date, nullable=False)
    semaine_annee = db.Column(db.Integer, nullable=False)  # Numéro de semaine
    annee = db.Column(db.Integer, nullable=False)
    lundi = db.Column(db.Boolean, default=False)
    mardi = db.Column(db.Boolean, default=False)
    mercredi = db.Column(db.Boolean, default=False)
    jeudi = db.Column(db.Boolean, default=False)
    vendredi = db.Column(db.Boolean, default=False)
    samedi = db.Column(db.Boolean, default=False)
    dimanche = db.Column(db.Boolean, default=False)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convives')
def convives():
    return render_template('convives.html')

@app.route('/regimes')
def regimes():
    return render_template('regimes.html')

@app.route('/menus')
def menus():
    return render_template('menus.html')

@app.route('/configuration')
def configuration():
    return render_template('configuration.html')

@app.route('/commandes')
def commandes():
    return render_template('commandes.html')

@app.route('/export')
def export_page():
    return render_template('export.html')

# API Routes - Convives
@app.route('/api/convives', methods=['GET'])
def get_convives():
    convives = Convive.query.filter_by(actif=True).all()
    return jsonify([{
        'id': c.id,
        'nom_prenom': c.nom_prenom,
        'lieu_remise': c.lieu_remise,
        'numero_boite': c.numero_boite,
        'numero_voie': c.numero_voie,
        'complement_commune': c.complement_commune,
        'code_postal': c.code_postal,
        'localite': c.localite,
        'indication_acces': c.indication_acces,
        'indications_complementaires': c.indications_complementaires,
        'telephone': c.telephone,
        'lundi': c.lundi,
        'mardi': c.mardi,
        'mercredi': c.mercredi,
        'jeudi': c.jeudi,
        'vendredi': c.vendredi,
        'samedi': c.samedi,
        'dimanche': c.dimanche,
        'regime_id': c.regime_id,
        'regime': c.regime.nom if c.regime else '',
        'menu_id': c.menu_id,
        'menu': c.menu.nom if c.menu else '',
        'tournee': c.tournee,
        'actif': c.actif
    } for c in convives])

@app.route('/api/convives', methods=['POST'])
def create_convive():
    data = request.json
    convive = Convive(
        nom_prenom=data['nom_prenom'],
        lieu_remise=data.get('lieu_remise'),
        numero_boite=data.get('numero_boite'),
        numero_voie=data.get('numero_voie'),
        complement_commune=data.get('complement_commune'),
        code_postal=data.get('code_postal'),
        localite=data.get('localite'),
        indication_acces=data.get('indication_acces'),
        indications_complementaires=data.get('indications_complementaires'),
        telephone=data.get('telephone'),
        lundi=data.get('lundi', False),
        mardi=data.get('mardi', False),
        mercredi=data.get('mercredi', False),
        jeudi=data.get('jeudi', False),
        vendredi=data.get('vendredi', False),
        samedi=data.get('samedi', False),
        dimanche=data.get('dimanche', False),
        regime_id=data.get('regime_id'),
        menu_id=data.get('menu_id'),
        tournee=data.get('tournee'),
        actif=True
    )
    db.session.add(convive)
    db.session.commit()
    return jsonify({'success': True, 'id': convive.id})

@app.route('/api/convives/<int:id>', methods=['PUT'])
def update_convive(id):
    convive = Convive.query.get_or_404(id)
    data = request.json
    
    convive.nom_prenom = data['nom_prenom']
    convive.lieu_remise = data.get('lieu_remise')
    convive.numero_boite = data.get('numero_boite')
    convive.numero_voie = data.get('numero_voie')
    convive.complement_commune = data.get('complement_commune')
    convive.code_postal = data.get('code_postal')
    convive.localite = data.get('localite')
    convive.indication_acces = data.get('indication_acces')
    convive.indications_complementaires = data.get('indications_complementaires')
    convive.telephone = data.get('telephone')
    convive.lundi = data.get('lundi', False)
    convive.mardi = data.get('mardi', False)
    convive.mercredi = data.get('mercredi', False)
    convive.jeudi = data.get('jeudi', False)
    convive.vendredi = data.get('vendredi', False)
    convive.samedi = data.get('samedi', False)
    convive.dimanche = data.get('dimanche', False)
    convive.regime_id = data.get('regime_id')
    convive.menu_id = data.get('menu_id')
    convive.tournee = data.get('tournee')
    
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/convives/<int:id>', methods=['DELETE'])
def delete_convive(id):
    convive = Convive.query.get_or_404(id)
    convive.actif = False
    db.session.commit()
    return jsonify({'success': True})

# API Routes - Régimes
@app.route('/api/regimes', methods=['GET'])
def get_regimes():
    regimes = Regime.query.all()
    return jsonify([{'id': r.id, 'nom': r.nom} for r in regimes])

@app.route('/api/regimes', methods=['POST'])
def create_regime():
    data = request.json
    regime = Regime(nom=data['nom'])
    db.session.add(regime)
    db.session.commit()
    return jsonify({'success': True, 'id': regime.id})

@app.route('/api/regimes/<int:id>', methods=['DELETE'])
def delete_regime(id):
    regime = Regime.query.get_or_404(id)
    db.session.delete(regime)
    db.session.commit()
    return jsonify({'success': True})

# API Routes - Menus
@app.route('/api/menus', methods=['GET'])
def get_menus():
    menus = Menu.query.all()
    return jsonify([{'id': m.id, 'nom': m.nom} for m in menus])

@app.route('/api/menus', methods=['POST'])
def create_menu():
    data = request.json
    menu = Menu(nom=data['nom'])
    db.session.add(menu)
    db.session.commit()
    return jsonify({'success': True, 'id': menu.id})

@app.route('/api/menus/<int:id>', methods=['DELETE'])
def delete_menu(id):
    menu = Menu.query.get_or_404(id)
    db.session.delete(menu)
    db.session.commit()
    return jsonify({'success': True})

# API Routes - Configuration Livraison
@app.route('/api/configuration', methods=['GET'])
def get_configuration():
    configs = ConfigurationLivraison.query.all()
    return jsonify([{
        'id': c.id,
        'jour_alimentaire': c.jour_alimentaire,
        'jour_livraison': c.jour_livraison
    } for c in configs])

@app.route('/api/configuration', methods=['POST'])
def save_configuration():
    data = request.json
    
    # Supprimer l'ancienne configuration
    ConfigurationLivraison.query.delete()
    
    # Créer la nouvelle configuration
    for item in data:
        config = ConfigurationLivraison(
            jour_alimentaire=item['jour_alimentaire'],
            jour_livraison=item['jour_livraison']
        )
        db.session.add(config)
    
    db.session.commit()
    return jsonify({'success': True})

# API Routes - Commandes
@app.route('/api/commandes/semaine/<int:semaine>/<int:annee>', methods=['GET'])
def get_commandes_semaine(semaine, annee):
    commandes = Commande.query.filter_by(semaine_annee=semaine, annee=annee).all()
    return jsonify([{
        'id': c.id,
        'convive_id': c.convive_id,
        'convive_nom': c.convive.nom_prenom,
        'lundi': c.lundi,
        'mardi': c.mardi,
        'mercredi': c.mercredi,
        'jeudi': c.jeudi,
        'vendredi': c.vendredi,
        'samedi': c.samedi,
        'dimanche': c.dimanche
    } for c in commandes])

@app.route('/api/commandes', methods=['POST'])
def save_commandes():
    data = request.json
    semaine = data['semaine']
    annee = data['annee']
    
    # Supprimer les commandes existantes pour cette semaine
    Commande.query.filter_by(semaine_annee=semaine, annee=annee).delete()
    
    # Créer les nouvelles commandes
    for item in data['commandes']:
        commande = Commande(
            convive_id=item['convive_id'],
            date_commande=datetime.now().date(),
            semaine_annee=semaine,
            annee=annee,
            lundi=item.get('lundi', False),
            mardi=item.get('mardi', False),
            mercredi=item.get('mercredi', False),
            jeudi=item.get('jeudi', False),
            vendredi=item.get('vendredi', False),
            samedi=item.get('samedi', False),
            dimanche=item.get('dimanche', False)
        )
        db.session.add(commande)
    
    db.session.commit()
    return jsonify({'success': True})

# Export CSV
@app.route('/api/export/csv', methods=['POST'])
def export_csv():
    data = request.json
    mode = data['mode']  # 'semaine' ou 'jour'
    date_str = data['date']  # Format: 'YYYY-MM-DD'
    
    date_reference = datetime.strptime(date_str, '%Y-%m-%d').date()
    
    # Obtenir la configuration de livraison
    config_dict = {}
    configs = ConfigurationLivraison.query.all()
    for c in configs:
        config_dict[c.jour_alimentaire] = c.jour_livraison
    
    # Calculer la semaine
    semaine = date_reference.isocalendar()[1]
    annee = date_reference.year
    
    # Obtenir les commandes
    commandes = Commande.query.filter_by(semaine_annee=semaine, annee=annee).all()
    
    # Préparer les données CSV
    rows = []
    jours_semaine = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    
    # Calculer le lundi de la semaine
    lundi_semaine = date_reference - timedelta(days=date_reference.weekday())
    
    for commande in commandes:
        convive = commande.convive
        
        # Pour chaque jour de la semaine
        for idx, jour in enumerate(jours_semaine):
            jour_commandé = getattr(commande, jour, False)
            
            # Si mode = jour, filtrer seulement le jour demandé
            if mode == 'jour':
                date_jour = lundi_semaine + timedelta(days=idx)
                if date_jour != date_reference or not jour_commandé:
                    continue
            else:
                if not jour_commandé:
                    continue
            
            # Obtenir le jour de livraison
            jour_livraison_nom = config_dict.get(jour, jour)
            jour_livraison_idx = jours_semaine.index(jour_livraison_nom) if jour_livraison_nom in jours_semaine else idx
            date_livraison = lundi_semaine + timedelta(days=jour_livraison_idx)
            date_conso = lundi_semaine + timedelta(days=idx)
            
            # Vérifier si cette ligne existe déjà pour ce jour de livraison
            existing_row = None
            for row in rows:
                if (row['convive_id'] == convive.id and 
                    row['date_livraison'] == date_livraison):
                    existing_row = row
                    break
            
            if existing_row:
                # Ajouter la date de consommation
                existing_row['dates_conso'].append(date_conso)
                existing_row['nb_objets'] += 1
            else:
                # Créer une nouvelle ligne
                reference = f"{convive.id}_{date_livraison.strftime('%d/%m/%Y')}"
                
                regime_nom = convive.regime.nom if convive.regime else ''
                
                rows.append({
                    'convive_id': convive.id,
                    'date_livraison': date_livraison,
                    'dates_conso': [date_conso],
                    'nb_objets': 1,
                    'reference': reference,
                    'nom_prenom': convive.nom_prenom or '',
                    'lieu_remise': convive.lieu_remise or '',
                    'numero_boite': convive.numero_boite or '',
                    'numero_voie': convive.numero_voie or '',
                    'complement_commune': convive.complement_commune or '',
                    'code_postal': convive.code_postal or '',
                    'localite': convive.localite or '',
                    'indication_acces': convive.indication_acces or '',
                    'indications_complementaires': convive.indications_complementaires or '',
                    'telephone': convive.telephone or '',
                    'regime': regime_nom,
                    'tournee': convive.tournee or ''
                })
    
    # Trier par date de livraison et tournée
    rows.sort(key=lambda x: (x['date_livraison'], x['tournee']))
    
    # Créer le fichier CSV
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    
    # Header
    writer.writerow([
        'Action',
        'Date de début souhaitée',
        'Référence Bénéficiaire',
        'Nom Prenom ou Raison sociale',
        'Lieu de remise',
        'Numero ou Boite aux lettres - Couloir-Escalier',
        'Numero et libelle de voie',
        'Complement commune ou service postal',
        'Code postal',
        'Localite',
        'Indication d\'acces au beneficiaire',
        'indications complementaires',
        'Nombre d\'objets',
        'Numéro de téléphone',
        'Email',
        'Metadonnées',
        'Paramètres Internes'
    ])
    
    # Données
    for row in rows:
        dates_conso_str = ', '.join([d.strftime('%d/%m/%Y') for d in row['dates_conso']])
        metadonnees = f"{{'Regime':'{row['regime']}','JourConso':'{dates_conso_str}'}}"
        parametres = f"{{'ROUND':'{row['tournee']}'}}"
        
        writer.writerow([
            'CREER',
            row['date_livraison'].strftime('%d/%m/%Y'),
            row['reference'],
            row['nom_prenom'],
            row['lieu_remise'],
            row['numero_boite'],
            row['numero_voie'],
            row['complement_commune'],
            row['code_postal'],
            row['localite'],
            row['indication_acces'],
            row['indications_complementaires'],
            f"{row['nb_objets']:.2f}".replace('.', ','),
            row['telephone'],
            '',
            metadonnees,
            parametres
        ])
    
    # Préparer la réponse
    output.seek(0)
    filename = f"livraisons_{date_str}.csv"
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

# Initialisation de la base de données
def init_db():
    with app.app_context():
        db.create_all()
        
        # Créer les régimes par défaut
        if Regime.query.count() == 0:
            regimes_default = ['Sans sel', 'Sans sucre', 'Sans sel ni sucre']
            for r in regimes_default:
                db.session.add(Regime(nom=r))
        
        # Créer la configuration par défaut
        if ConfigurationLivraison.query.count() == 0:
            jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
            for jour in jours:
                db.session.add(ConfigurationLivraison(
                    jour_alimentaire=jour,
                    jour_livraison='lundi' if jour in ['lundi', 'mardi'] else jour
                ))
        
        db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
