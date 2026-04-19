import feedparser
import requests
import re
import sys

FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UC5m1fPLNTZCgLjIzO5iy-Ng"

EXISTING_PLACES = [
    "Le Petit Vendôme","Cédric Grolet","BO&MIE","Boulangerie Joseph","Angelina",
    "Au Pied de Cochon","Le Louchébem","Ferdi","Café Nuances","Chez Suzette",
    "La Petite Samaritain","Big Fernand","Chez Denise","Frenchie","Frenchie Bar à Vins",
    "Frenchie To Go","Stohrer","Loulou","Kei","Le Grand Véfour","Racines","Saturne",
    "Le Bon Georges","Bouillon Chartier","Bambou","Café de la Paix","Drouant",
    "Le Bouillon Pigalle","La Brasserie Barbès","Le Baratin","Bones","Septime",
    "Clamato","Charbon","Le Servan","Café de Flore","Les Deux Magots","Brasserie Lipp",
    "Chez Georges","Au Bon Saint-Pourçain","La Crêperie de Josselin","Breizh Café",
    "Le Comptoir du Relais","Huîtrerie Régis","Fish La Boissonnerie","Semilla",
    "Café de la Mairie","Ladurée","Pierre Hermé","Eric Kayser","Poilâne",
    "Jacques Genin","Un Dimanche à Paris","Odette","Shakespeare and Company Café",
    "Le Procope","Allard","Le Relais de l'Entrecôte","Grom","Amorino",
    "L'As du Fallafel","Chez Marianne","Le Loir dans la Théière","Berthillon",
    "Ma Salle à Manger","Les Philosophes","Café Charlot","Le Progrès",
    "Du Pain et des Idées","Ten Belles","Café de l'Industrie","Le Dauphin",
    "Abri","Richer","Le Verre Volé","Chez Michel","Holybelly","KB CaféShop",
    "Beans on Fire","KB Roasters","Le Cambodge","Pink Mamma","Souls","Bouillon Chartier Est",
    "La Fontaine de Belleville","L'Aller Retour","Café Méricourt","Café Paul Bert",
    "Le Train Bleu","La Coupole","Le Dôme","Ciel de Paris","Brutus Crêperie",
    "La Boîte aux Lettres","Bouillon Pigalle","Le Coq & Fils","Le Refuge des Fondus","Ose",
    "Dersou","Septime La Cave","Le Chateaubriand","Le 6 Paul Bert","Bistrot Paul Bert",
    "Au Passage","Marché d'Aligre","Yard","Mokonuts","Tavline","Miznon",
    "Grand Appétit","Café de la Mosquée","Sola","Mavrommatis","Itacoa",
    "Les Papilles","Huîtres Garnier","Le Timbre","Le Cherche Midi","Arnaud Larher",
    "Benoit","Au Bourguignon du Marais","Le Hangar","Marché des Enfants Rouges",
    "L'Ami Louis","Chez Omar","Tomy & Co","Granterroirs","Nanashi",
    "Ellsworth","Champeaux","Pirouette","Spring","Verjus","Racines des Prés",
]

def get_recent_videos():
    feed = feedparser.parse(FEED_URL)
    return feed.entries[:10]

def extract_place_candidates(text):
    lines = text.split('\n')
    candidates = []
    for line in lines:
        line = line.strip()
        if any(c in line for c in ['🍽','🥐','☕','🍷','🥖','📍','→','-','•']) and len(line) > 3:
            clean = re.sub(r'[🍽🥐☕🍷🥖📍→\-•\*]', '', line).strip()
            clean = re.sub(r'\s+', ' ', clean)
            if 3 < len(clean) < 60:
                candidates.append(clean)
    return candidates

def find_new_places(videos):
    existing_lower = {p.lower() for p in EXISTING_PLACES}
    new_places = []
    for video in videos:
        title = video.get('title', '')
        description = video.get('summary', '')
        candidates = extract_place_candidates(description)
        for candidate in candidates:
            if candidate.lower() not in existing_lower:
                new_places.append({
                    'place': candidate,
                    'video_title': title,
                    'video_url': video.get('link', '')
                })
    return new_places

videos = get_recent_videos()
new_places = find_new_places(videos)

if new_places:
    with open('new_places.txt', 'w') as f:
        f.write("## Potential new places found in recent Les Frenchies videos\n\n")
        f.write("Review these and add any confirmed ones to the map.\n\n")
        for p in new_places:
            f.write(f"**{p['place']}**\n")
            f.write(f"Found in: [{p['video_title']}]({p['video_url']})\n\n")
    print(f"Found {len(new_places)} potential new places.")
    sys.exit(1)
else:
    print("No new places found.")
