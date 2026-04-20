import feedparser
import requests
import re
import sys
from urllib.parse import quote

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

CATEGORIES = "Bakery & Pâtisserie · Bistro & Brasserie · Café & Coffee · Fine Dining · Seafood · Wine & Bar · Casual & Street Food · Italian & Pizza · Market & Specialty · Steakhouse"

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
    seen = set()
    for video in videos:
        title = video.get('title', '')
        description = video.get('summary', '')
        candidates = extract_place_candidates(description)
        for candidate in candidates:
            key = candidate.lower()
            if key not in existing_lower and key not in seen:
                seen.add(key)
                new_places.append({
                    'place': candidate,
                    'video_title': title,
                    'video_url': video.get('link', '')
                })
    return new_places

def geocode(place_name):
    try:
        params = {"q": f"{place_name}, Paris, France", "format": "json", "limit": 1}
        headers = {"User-Agent": "LesFrenchiesFoodMap/1.0"}
        r = requests.get("https://nominatim.openstreetmap.org/search",
                         params=params, headers=headers, timeout=8)
        data = r.json()
        if data:
            return round(float(data[0]["lat"]), 4), round(float(data[0]["lon"]), 4)
    except Exception:
        pass
    return None, None

def build_issue_body(new_places):
    lines = [
        "## 🗺️ Potential new places from Les Frenchies",
        "",
        "The scraper found these in recent videos. For each confirmed place:",
        "1. Click the map link to verify the geocoded location is accurate",
        "2. Fill in the CAPS fields in the JS stub",
        "3. Paste the object into the `places` array in `paris-food-map.html`",
        "4. Add the name to `EXISTING_PLACES` in `scripts/scrape.py` so it won't flag again",
        "",
        "---",
        "",
    ]

    for p in new_places:
        place = p['place']
        lat, lng = geocode(place)

        lines.append(f"### {place}")
        lines.append(f"📹 [{p['video_title']}]({p['video_url']})")
        lines.append("")

        if lat:
            map_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lng}&zoom=17"
            lines.append(f"📍 Geocoded: `{lat}, {lng}` · [verify on map]({map_url})")
        else:
            search_url = f"https://nominatim.openstreetmap.org/search?q={quote(place + ' Paris')}&format=json"
            lines.append(f"📍 Could not geocode · [search manually]({search_url})")

        lines.append("")

        lat_str = str(lat) if lat else "XX.XXXX"
        lng_str = str(lng) if lng else "X.XXXX"
        stub = (
            f'  {{name:"{place}", cat:"CATEGORY", arr:X, price:"€€",\n'
            f'   lat:{lat_str}, lng:{lng_str}, michelin:0,\n'
            f'   meals:["lunch","dinner"], tags:[], review:"REVIEW",\n'
            f'   source:"Les Frenchies Travel"}},'
        )

        lines.append("```js")
        lines.append(stub)
        lines.append("```")
        lines.append("")
        lines.append(f"**Categories:** {CATEGORIES}")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)

videos = get_recent_videos()
new_places = find_new_places(videos)

if new_places:
    body = build_issue_body(new_places)
    with open('new_places.txt', 'w') as f:
        f.write(body)
    print(f"Found {len(new_places)} potential new places.")
    sys.exit(1)
else:
    print("No new places found.")
