from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Spotify gerçek şarkı linkleri
SPOTIFY_SONGS = {
    "podyum": [
        {"title": "Runway", "artist": "Nina Kraviz", "url": "https://open.spotify.com/track/7bBpIRK114sENgSjXztpT8", "cover": None},
        {"title": "Genesis", "artist": "Grimes", "url": "https://open.spotify.com/track/3cjXFFB8i5vUwMFnv5O6hh", "cover": None},
        {"title": "Technologic", "artist": "Daft Punk", "url": "https://open.spotify.com/track/0LSLM0zuWRkEYemF7JcfEE", "cover": None},
        {"title": "Fashion", "artist": "David Bowie", "url": "https://open.spotify.com/track/5UoEZnjS46KRyOaEk9nSLe", "cover": None}
    ],
    "gece": [
        {"title": "Midnight City", "artist": "M83", "url": "https://open.spotify.com/track/1eyzqe2QqGZUmfcPZtrIyt", "cover": None},
        {"title": "Nightcall", "artist": "Kavinsky", "url": "https://open.spotify.com/track/0U0ldCRmgCqhVvD6ksG63j", "cover": None},
        {"title": "Blinding Lights", "artist": "The Weeknd", "url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b", "cover": None}
    ],
    "eski": [
        {"title": "The Night We Met", "artist": "Lord Huron", "url": "https://open.spotify.com/track/0QZ5yyl6B6utIWkxeBDxQN", "cover": None},
        {"title": "Someone Like You", "artist": "Adele", "url": "https://open.spotify.com/track/1kz9NMR2W2MZ4OK6w7ztiU", "cover": None}
    ],
    "güçlü": [
        {"title": "Stronger", "artist": "Kanye West", "url": "https://open.spotify.com/track/5Qh3KPKBueFbGnpcwU8NpU", "cover": None},
        {"title": "Seven Nation Army", "artist": "The White Stripes", "url": "https://open.spotify.com/track/3m6KkYKdnbffMpGd9Pm9FP", "cover": None}
    ],
    "yağmur": [
        {"title": "Purple Rain", "artist": "Prince", "url": "https://open.spotify.com/track/54X78diSLoUDI3joC2bjMz", "cover": None},
        {"title": "November Rain", "artist": "Guns N' Roses", "url": "https://open.spotify.com/track/3YRCqOhFifThpSRFJ1VWFM", "cover": None}
    ],
    "davet": [
        {"title": "Uptown Funk", "artist": "Mark Ronson", "url": "https://open.spotify.com/track/32OlwWuMpZ6b0aN2RZOeMS", "cover": None},
        {"title": "Fancy", "artist": "Iggy Azalea", "url": "https://open.spotify.com/track/3oiMJQAWVaxSubJjlWwxvd", "cover": None}
    ]
}

def analyze_scenario(scenario, language="tr"):
    print(f"🔍 ANALİZ EDİLEN SENARYO: {scenario}")
    
    lower = scenario.lower()
    
    if "podyum" in lower or "runway" in lower or "yürü" in lower:
        return {
            "tags": ["podyum", "ulaşılmaz", "moda"],
            "category": "podyum",
            "psychology_note": "Podyum hayalleri, kendini ifade etme ve görünür olma arzusunu yansıtır. Bu tür daydream'ler, özgüven inşasında olumlu bir araç olabilir. Müzik, bu enerjini ortaya çıkarır ve sana ait olduğun sahneyi hatırlatır.",
            "mood": "powerful"
        }
    elif "gece" in lower or "şehir" in lower or "araba" in lower:
        return {
            "tags": ["gece", "şehir", "yalnız"],
            "category": "gece",
            "psychology_note": "Gece ve şehir temalı hayaller, genellikle özgürlük arayışını ve günlük hayatın baskılarından kaçışı simgeler. Yalnız ama güçlü hissetmek, aslında kendinle barışık olmanın bir göstergesidir.",
            "mood": "melancholic"
        }
    elif "eski" in lower or "aşk" in lower or "sevgi" in lower:
        return {
            "tags": ["eski aşk", "özlem", "dönüşüm"],
            "category": "eski",
            "psychology_note": "Eski aşk temalı senaryolar, geçmişle hesaplaşma ve dönüşüm sürecinin bir parçasıdır. Kendini yeniden inşa ettiğin bu anlar, aslında büyümenin en değerli anlarıdır.",
            "mood": "emotional"
        }
    elif "güçlü" in lower or "soğuk" in lower or "ulaşılmaz" in lower:
        return {
            "tags": ["güçlü", "ulaşılmaz", "kontrol"],
            "category": "güçlü",
            "psychology_note": "Güçlü ve ulaşılmaz hissetme ihtiyacı, genellikle kontrol ihtiyacından gelir. Bu duyguyu sağlıklı bir şekilde yaşamak, özsaygını güçlendirir.",
            "mood": "powerful"
        }
    elif "yağmur" in lower or "cam" in lower:
        return {
            "tags": ["yağmur", "hüzün", "içe dönüş"],
            "category": "yağmur",
            "psychology_note": "Yağmurlu gün hayalleri, içe dönüş ve duygusal arınma ihtiyacını yansıtır. Kendi hayatını film gibi izlemek, aslında yaşadıklarına anlam katma çabasıdır.",
            "mood": "calm"
        }
    elif "davet" in lower or "lüks" in lower or "parti" in lower:
        return {
            "tags": ["lüks", "kalabalık", "gösteriş"],
            "category": "davet",
            "psychology_note": "Lüks davet ve kalabalık senaryoları, aidiyet ve kabul görme ihtiyacını yansıtır. Bu tür daydream'ler, sosyal kaygılarla başa çıkmanın bir yolu olabilir.",
            "mood": "energetic"
        }
    else:
        return {
            "tags": ["dreamy", "cinematic"],
            "category": "gece",
            "psychology_note": "Her senaryo, iç dünyamızın bir yansımasıdır. Müzik, bu içsel yolculukta sana eşlik eden en güçlü araçtır.",
            "mood": "dreamy"
        }

def search_spotify(category, limit=5):
    print(f"🎵 ŞARKILAR GETİRİLİYOR - Kategori: {category}")
    
    # Kategoriye göre şarkıları getir
    if category in SPOTIFY_SONGS:
        return SPOTIFY_SONGS[category][:limit]
    else:
        return SPOTIFY_SONGS["gece"][:limit]

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    scenario = data.get('scenario', '')
    language = data.get('language', 'tr')
    
    print(f"📨 İSTEK ALINDI: {scenario}")
    
    if not scenario:
        return jsonify({"error": "Senaryo yazılmamış"}), 400
    
    analysis = analyze_scenario(scenario, language)
    songs = search_spotify(analysis.get('category', 'gece'))
    
    return jsonify({
        "scenario": scenario,
        "tags": analysis.get('tags', []),
        "psychology_note": analysis.get('psychology_note', ''),
        "mood": analysis.get('mood', ''),
        "songs": songs
    })

if __name__ == '__main__':
    print("🚀 SceneTune AI Başlatılıyor...")
    print("📍 http://127.0.0.1:5000")
    app.run(debug=True, port=5000)