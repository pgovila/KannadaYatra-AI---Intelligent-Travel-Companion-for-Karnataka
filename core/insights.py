"""
core/insights.py - KannadaYatra AI
Cultural context engine: Kannada survival-phrase generator, regional
cuisine database, festival calendar, and heritage history lookup.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1.  KANNADA SURVIVAL PHRASE KIT - phonetically spelled for tourists
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class KannadaPhrase:
    """A single survival phrase with Kannada script, phonetics, English, Hindi, Tamil, and Telugu."""
    english: str
    kannada: str
    phonetic: str
    context_hint: str = ""          # when/where to use it
    hindi: str = ""                 # हिन्दी
    tamil: str = ""                 # தமிழ்
    telugu: str = ""                # తెలుగు


# ── Core Greeting & Courtesy Phrases ─────────────────────────────────
GREETINGS: List[KannadaPhrase] = [
    KannadaPhrase(
        "Hello / Greetings", "ನಮಸ್ಕಾರ", "Namaskāra",
        "Universal greeting - works everywhere",
        hindi="नमस्ते / नमस्कार", tamil="வணக்கம்", telugu="నమస్కారం",
    ),
    KannadaPhrase(
        "How are you?", "ಹೇಗಿದ್ದೀರಾ?", "Hēgiddīrā?",
        "Polite - use with elders & strangers",
        hindi="आप कैसे हैं?", tamil="எப்படி இருக்கிறீர்கள்?", telugu="మీరు ఎలా ఉన్నారు?",
    ),
    KannadaPhrase(
        "I am fine", "ನಾನು ಚೆನ್ನಾಗಿದ್ದೇನೆ", "Nānu chennāgiddēne",
        "Friendly response",
        hindi="मैं ठीक हूँ", tamil="நான் நலமாக இருக்கிறேன்", telugu="నేను బాగున్నాను",
    ),
    KannadaPhrase(
        "Thank you", "ಧನ್ಯವಾದಗಳು", "Dhanyavādagaḷu",
        "Express gratitude",
        hindi="धन्यवाद / शुक्रिया", tamil="நன்றி", telugu="ధన్యవాదాలు",
    ),
    KannadaPhrase(
        "Please", "ದಯವಿಟ್ಟು", "Dayaviṭṭu",
        "Prefix to any request",
        hindi="कृपया", tamil="தயவுசெய்து", telugu="దయచేసి",
    ),
    KannadaPhrase(
        "Excuse me / Sorry", "ಕ್ಷಮಿಸಿ", "Kṣhamisi",
        "Apologising or getting attention",
        hindi="माफ़ कीजिए", tamil="மன்னிக்கவும்", telugu="క్షమించండి",
    ),
    KannadaPhrase(
        "Yes", "ಹೌದು", "Haudu",
        "Affirmation",
        hindi="हाँ / जी हाँ", tamil="ஆம் / சரி", telugu="అవును",
    ),
    KannadaPhrase(
        "No", "ಇಲ್ಲ", "Illa",
        "Polite refusal",
        hindi="नहीं", tamil="இல்லை", telugu="లేదు / కాదు",
    ),
    KannadaPhrase(
        "I don't understand", "ನನಗೆ ಅರ್ಥವಾಗುತ್ತಿಲ್ಲ", "Nanage arthavāguttilla",
        "When someone speaks too fast",
        hindi="मुझे समझ नहीं आया", tamil="எனக்கு புரியவில்லை", telugu="నాకు అర్థం కాలేదు",
    ),
    KannadaPhrase(
        "I don't speak Kannada", "ನನಗೆ ಕನ್ನಡ ಬರುವುದಿಲ್ಲ", "Nanage Kannaḍa baruvudilla",
        "Helpful for tourists",
        hindi="मुझे कन्नड़ नहीं आती", tamil="எனக்கு கன்னடம் பேச வராது", telugu="నాకు కన్నడ రాదు",
    ),
    KannadaPhrase(
        "Do you speak English?", "ನೀವು ಇಂಗ್ಲಿಷ್ ಮಾತಾಡುತ್ತೀರಾ?", "Nīvu English mātāḍuttīrā?",
        "Ask before explaining",
        hindi="क्या आप अंग्रेज़ी बोलते हैं?", tamil="நீங்கள் ஆங்கிலம் பேசுவீர்களா?", telugu="మీరు ఇంగ్లీష్ మాట్లాడతారా?",
    ),
]

# ── Directions & Navigation ──────────────────────────────────────────
DIRECTIONS: List[KannadaPhrase] = [
    KannadaPhrase(
        "Where is ___?", "___ ಎಲ್ಲಿದೆ?", "___ Ellide?",
        "Point or name the place",
        hindi="___ कहाँ है?", tamil="___ எங்கே இருக்கிறது?", telugu="___ ఎక్కడ ఉంది?",
    ),
    KannadaPhrase(
        "How do I get to ___?", "___ ಗೆ ಹೇಗೆ ಹೋಗಬೇಕು?", "___ ge hēge hōgabēku?",
        "Ask route instructions",
        hindi="___ कैसे जा सकते हैं?", tamil="___ க்கு எப்படி செல்வது?", telugu="___ కి ఎలా వెళ్ళాలి?",
    ),
    KannadaPhrase(
        "Turn left", "ಎಡಕ್ಕೆ ತಿರುಗಿ", "Eḍakke tirugi",
        "Direction",
        hindi="बाएं मुड़िए", tamil="இடதுபுறம் திரும்புங்கள்", telugu="ఎడమ వైపు తిరగండి",
    ),
    KannadaPhrase(
        "Turn right", "ಬಲಕ್ಕೆ ತಿರುಗಿ", "Balakke tirugi",
        "Direction",
        hindi="दाएं मुड़िए", tamil="வலதுபுறம் திரும்புங்கள்", telugu="కుడి వైపు తిరగండి",
    ),
    KannadaPhrase(
        "Go straight", "ನೇರವಾಗಿ ಹೋಗಿ", "Nēravāgi hōgi",
        "Direction",
        hindi="सीधे जाइए", tamil="நேராக செல்லுங்கள்", telugu="నేరుగా వెళ్ళండి",
    ),
    KannadaPhrase(
        "Is it far from here?", "ಇಲ್ಲಿಂದ ದೂರ ಇದೆಯಾ?", "Illinda dūra ideyā?",
        "Check walking distance",
        hindi="क्या यह यहाँ से दूर है?", tamil="இங்கிருந்து தூரமா?", telugu="ఇక్కడ నుండి దూరమా?",
    ),
    KannadaPhrase(
        "Bus stop", "ಬಸ್ ನಿಲ್ದಾಣ", "Bus nildāṇa",
        "Transit spot",
        hindi="बस स्टैंड / बस स्टॉप", tamil="பேருந்து நிலையம்", telugu="బస్సు స్టాప్",
    ),
    KannadaPhrase(
        "Railway station", "ರೈಲ್ವೇ ನಿಲ್ದಾಣ", "Railway nildāṇa",
        "Transit spot",
        hindi="रेलवे स्टेशन", tamil="ரயில் நிலையம்", telugu="రైల్వే స్టేషన్",
    ),
    KannadaPhrase(
        "Please call an auto-rickshaw", "ಆಟೋ ಕರೆಯಿರಿ ದಯವಿಟ್ಟು", "Auto kareyiri dayaviṭṭu",
        "Request assistance",
        hindi="कृपया ऑटो बुला दीजिए", tamil="தயவுசெய்து ஆட்டோ கூப்பிடுங்கள்", telugu="దయచేసి ఆటో పిలవండి",
    ),
    KannadaPhrase(
        "Use the meter, please", "ಮೀಟರ್ ಹಾಕಿ, ದಯವಿಟ್ಟು", "Meter hāki, dayaviṭṭu",
        "For auto rides in Bangalore & Mysore",
        hindi="कृपया मीटर चालू कीजिए", tamil="தயவுசெய்து மீட்டர் போடுங்க", telugu="దయచేసి మీటర్ వేయండి",
    ),
]

# ── Food & Dining ────────────────────────────────────────────────────
FOOD_PHRASES: List[KannadaPhrase] = [
    KannadaPhrase(
        "I am hungry", "ನನಗೆ ಹಸಿವಾಗಿದೆ", "Nanage hasivāgide",
        "Express hunger",
        hindi="मुझे भूख लगी है", tamil="எனக்கு பசிக்கிறது", telugu="నాకు ఆకలిగా ఉంది",
    ),
    KannadaPhrase(
        "Menu please", "ಮೆನು ಕೊಡಿ", "Menu koḍi",
        "At any restaurant or hotel",
        hindi="मेन्यू दीजिए", tamil="மெனு கொடுங்கள்", telugu="మెనూ ఇవ్వండి",
    ),
    KannadaPhrase(
        "What is the specialty here?", "ಇಲ್ಲಿಯ ವಿಶೇಷ ಏನು?", "Illiya vishēṣha ēnu?",
        "Great conversation starter at darshinis",
        hindi="यहाँ का खास क्या है?", tamil="இங்கு என்ன ஸ்பெஷல்?", telugu="ఇక్కడ స్పెషల్ ఏమిటి?",
    ),
    KannadaPhrase(
        "This is very tasty!", "ಇದು ತುಂಬಾ ರುಚಿಯಾಗಿದೆ!", "Idu tumbā ruchiyāgide!",
        "Compliment the cook or host",
        hindi="यह बहुत स्वादिष्ट है!", tamil="இது மிகவும் சுவையாக உள்ளது!", telugu="ఇది చాలా రుచిగా ఉంది!",
    ),
    KannadaPhrase(
        "Water, please", "ನೀರು ಕೊಡಿ", "Nīru koḍi",
        "Essential dining request",
        hindi="पानी दीजिए", tamil="தண்ணீர் கொடுங்கள்", telugu="నీళ్ళు ఇవ్వండి",
    ),
    KannadaPhrase(
        "One more plate", "ಇನ್ನೊಂದು ಪ್ಲೇಟ್", "Innondu plate",
        "Reorder snacks or meals",
        hindi="एक प्लेट और दीजिए", tamil="இன்னொரு பிளேட் கொடுங்கள்", telugu="ఇంకో ప్లేట్ ఇవ్వండి",
    ),
    KannadaPhrase(
        "Bill / Check, please", "ಬಿಲ್ ಕೊಡಿ", "Bill koḍi",
        "End of meal",
        hindi="बिल दीजिए", tamil="பில் கொடுங்கள்", telugu="బిల్లు ఇవ్వండి",
    ),
    KannadaPhrase(
        "I am vegetarian", "ನಾನು ಶಾಖಾಹಾರಿ", "Nānu shākhāhāri",
        "Very widely understood",
        hindi="मैं शाकाहारी हूँ", tamil="நான் சைவம்", telugu="నేను శాఖాహారిని",
    ),
    KannadaPhrase(
        "No spice, please", "ಖಾರ ಬೇಡ, ದಯವಿಟ್ಟು", "Khāra bēḍa, dayaviṭṭu",
        "Adjust spice level",
        hindi="तीखा मत डालिए / कम तीखा", tamil="காரம் வேண்டாம் / குறைக்கவும்", telugu="కారం వద్దు / తక్కువ వేయండి",
    ),
    KannadaPhrase(
        "I want filter coffee", "ಫಿಲ್ಟರ್ ಕಾಫಿ ಬೇಕು", "Filter coffee bēku",
        "Karnataka's iconic staple!",
        hindi="मुझे फ़िल्टर कॉफ़ी चाहिए", tamil="எனக்கு பில்டர் காபி வேண்டும்", telugu="నాకు ఫిల్టర్ కాఫీ కావాలి",
    ),
]

# ── Shopping & Bargaining ────────────────────────────────────────────
SHOPPING_PHRASES: List[KannadaPhrase] = [
    KannadaPhrase(
        "How much does this cost?", "ಇದರ ಬೆಲೆ ಎಷ್ಟು?", "Idara bele eṣhṭu?",
        "Point at the souvenir or silk item",
        hindi="इसकी कीमत कितनी है?", tamil="இதன் விலை என்ன?", telugu="దీని ధర ఎంత?",
    ),
    KannadaPhrase(
        "Too expensive!", "ತುಂಬಾ ದುಬಾರಿ!", "Tumbā dubāri!",
        "Start of friendly bargaining",
        hindi="बहुत महंगा है!", tamil="மிகவும் விலை அதிகம்!", telugu="చాలా ఖరీదు!",
    ),
    KannadaPhrase(
        "Reduce the price a little", "ಸ್ವಲ್ಪ ಕಡಿಮೆ ಮಾಡಿ", "Svalpa kaḍime māḍi",
        "Polite negotiation phrase",
        hindi="थोड़ा कम कीजिए", tamil="கொஞ்சம் குறைத்துக் கொடுங்கள்", telugu="కొంచెం తగ్గించండి",
    ),
    KannadaPhrase(
        "I will take this", "ನಾನು ಇದನ್ನು ತೆಗೆದುಕೊಳ್ಳುತ್ತೇನೆ", "Nānu idannu tegedukoḷḷuttēne",
        "Finalise purchase",
        hindi="मैं यह लूँगा / लूँगी", tamil="நான் இதை எடுத்துக்கொள்கிறேன்", telugu="నేను ఇది తీసుకుంటాను",
    ),
    KannadaPhrase(
        "Do you accept UPI / card?", "UPI / ಕಾರ್ಡ್ ಆಗುತ್ತಾ?", "UPI / card āguttā?",
        "Common across street vendors & stalls",
        hindi="क्या UPI / कार्ड चलेगा?", tamil="UPI / கார்டு ஏற்குமா?", telugu="UPI / కార్డు తీసుకుంటారా?",
    ),
    KannadaPhrase(
        "Can I see that?", "ಅದನ್ನ ತೋರಿಸಿ", "Adanna tōrisi",
        "Inspect item closely",
        hindi="वह दिखाइए", tamil="அதை காட்டுங்கள்", telugu="అది చూపించండి",
    ),
    KannadaPhrase(
        "I am just looking", "ನಾನು ನೋಡುತ್ತಿದ್ದೇನೆ", "Nānu nōḍuttiddēne",
        "No-pressure browsing",
        hindi="मैं बस देख रहा हूँ", tamil="நான் சும்மா பார்க்கிறேன்", telugu="నేను చూస్తున్నానంతే",
    ),
    KannadaPhrase(
        "Where is the market?", "ಮಾರುಕಟ್ಟೆ ಎಲ್ಲಿದೆ?", "Mārukaṭṭe ellide?",
        "Find local bazaar or spice market",
        hindi="बाज़ार कहाँ है?", tamil="சந்தை எங்கே இருக்கிறது?", telugu="మార్కెట్ ఎక్కడ ఉంది?",
    ),
]

# ── Emergency & Help ─────────────────────────────────────────────────
EMERGENCY_PHRASES: List[KannadaPhrase] = [
    KannadaPhrase(
        "Help!", "ಸಹಾಯ ಮಾಡಿ!", "Sahāya māḍi!",
        "Urgent situations",
        hindi="मदद कीजिए!", tamil="உதவி செய்யுங்கள்!", telugu="సహాయం చేయండి!",
    ),
    KannadaPhrase(
        "I need a doctor", "ನನಗೆ ಡಾಕ್ಟರ್ ಬೇಕು", "Nanage doctor bēku",
        "Medical need",
        hindi="मुझे डॉक्टर की ज़रूरत है", tamil="எனக்கு மருத்துவர் தேவை", telugu="నాకు డాక్టర్ కావాలి",
    ),
    KannadaPhrase(
        "Please call the police", "ಪೊಲೀಸರನ್ನು ಕರೆಯಿರಿ", "Polīsarannu kareyiri",
        "Safety request",
        hindi="कृपया पुलिस को बुलाइए", tamil="தயவுசெய்து காவல்துறையை அழைக்கவும்", telugu="దయచేసి పోలీసులను పిలవండి",
    ),
    KannadaPhrase(
        "Where is the hospital?", "ಆಸ್ಪತ್ರೆ ಎಲ್ಲಿದೆ?", "Āspatre ellide?",
        "Medical facility",
        hindi="अस्पताल कहाँ है?", tamil="மருத்துவமனை எங்கே இருக்கிறது?", telugu="ఆసుపత్రి ఎక్కడ ఉంది?",
    ),
    KannadaPhrase(
        "I am lost", "ನಾನು ದಾರಿ ತಪ್ಪಿದ್ದೇನೆ", "Nānu dāri tappiddēne",
        "Need directional aid",
        hindi="मैं रास्ता भटक गया हूँ", tamil="நான் வழியைத் தொலைத்துவிட்டேன்", telugu="నేను దారి తప్పాను",
    ),
    KannadaPhrase(
        "My phone number is ___", "ನನ್ನ ಫೋನ್ ನಂಬರ್ ___", "Nanna phone number ___",
        "Sharing emergency contact",
        hindi="मेरा फ़ोन नंबर ___ है", tamil="எனது தொலைபேசி எண் ___", telugu="నా ఫోన్ నంబర్ ___",
    ),
]

# ── Transit-Specific ─────────────────────────────────────────────────
TRANSIT_PHRASES: List[KannadaPhrase] = [
    KannadaPhrase(
        "One ticket to ___", "___ ಗೆ ಒಂದು ಟಿಕೆಟ್", "___ ge ondu ticket",
        "Bus conductor or railway counter",
        hindi="___ के लिए एक टिकट दीजिए", tamil="___ க்கு ஒரு டிக்கெட்", telugu="___ కి ఒక టికెట్ ఇవ్వండి",
    ),
    KannadaPhrase(
        "What time does the bus leave?", "ಬಸ್ ಎಷ್ಟು ಗಂಟೆಗೆ ಹೊರಡುತ್ತೆ?", "Bus eṣhṭu gaṇṭege horaḍutte?",
        "Schedule inquiry at KSRTC depots",
        hindi="बस कितने बजे निकलेगी?", tamil="பேருந்து எத்தனை மணிக்கு புறப்படும்?", telugu="బస్సు ఎన్ని గంటలకు బయలుదేరుతుంది?",
    ),
    KannadaPhrase(
        "Stop here, please", "ಇಲ್ಲಿ ನಿಲ್ಲಿಸಿ, ದಯವಿಟ್ಟು", "Illi nillisi, dayaviṭṭu",
        "Alight from auto, taxi, or bus",
        hindi="यहाँ रोक दीजिए, कृपया", tamil="இங்கே நிறுத்துங்கள், தயவுசெய்து", telugu="ఇక్కడ ఆపండి, దయచేసి",
    ),
    KannadaPhrase(
        "How long will it take?", "ಎಷ್ಟು ಸಮಯ ಆಗುತ್ತೆ?", "Eṣhṭu samaya āgutte?",
        "Travel time estimate",
        hindi="कितना समय लगेगा?", tamil="எவ்வளவு நேரம் ஆகும்?", telugu="ఎంత సమయం పడుతుంది?",
    ),
    KannadaPhrase(
        "Is this the right bus for ___?", "ಇದು ___ ಗೆ ಹೋಗುವ ಬಸ್ಸಾ?", "Idu ___ ge hōguva bassā?",
        "Confirm route with conductor",
        hindi="क्या यह ___ जाने वाली बस है?", tamil="இது ___ செல்லும் பேருந்தா?", telugu="ఇది ___ వెళ్లే బస్సా?",
    ),
    KannadaPhrase(
        "Window seat, please", "ಕಿಟಕಿ ಸೀಟ್ ಕೊಡಿ", "Kiṭaki seat koḍi",
        "Long-distance KSRTC Rajahamsa/Airavat",
        hindi="खिड़की वाली सीट दीजिए", tamil="ஜன்னல் ஓர இருக்கை கொடுங்கள்", telugu="కిటికీ పక్క సీటు ఇవ్వండి",
    ),
]

# ── Phrase registry by category name ─────────────────────────────────
PHRASE_CATEGORIES: Dict[str, List[KannadaPhrase]] = {
    "🙏 Greetings & Courtesy":   GREETINGS,
    "🧭 Directions & Navigation": DIRECTIONS,
    "🍛 Food & Dining":           FOOD_PHRASES,
    "🛍️ Shopping & Bargaining":   SHOPPING_PHRASES,
    "🚌 Transit":                 TRANSIT_PHRASES,
    "🚨 Emergency & Help":        EMERGENCY_PHRASES,
}


def get_context_phrases(destination_name: str) -> Dict[str, List[KannadaPhrase]]:
    """
    Given a destination name, return the most contextually relevant
    phrase categories. All destinations get Greetings + Directions;
    food destinations also get Food phrases, etc.
    """
    from utils.helpers import KARNATAKA_DESTINATIONS

    dest = KARNATAKA_DESTINATIONS.get(destination_name)
    # Always include basics
    result: Dict[str, List[KannadaPhrase]] = {
        "🙏 Greetings & Courtesy":   GREETINGS,
        "🧭 Directions & Navigation": DIRECTIONS,
    }

    if dest:
        cats = set(dest.categories)
        if "Food" in cats:
            result["🍛 Food & Dining"] = FOOD_PHRASES
        if "Heritage" in cats or "Adventure" in cats:
            result["🛍️ Shopping & Bargaining"] = SHOPPING_PHRASES
        if "Nature" in cats or "Adventure" in cats:
            result["🚌 Transit"] = TRANSIT_PHRASES
    else:
        # Unknown destination → give everything
        result.update(PHRASE_CATEGORIES)

    # Always include emergency
    result["🚨 Emergency & Help"] = EMERGENCY_PHRASES
    return result


def search_travel_phrases(query: str) -> List[KannadaPhrase]:
    """Search for relevant phrases across English, Kannada, Hindi, Tamil, and Telugu keywords and common romanized terms."""
    if not query or not query.strip():
        return []
    q = query.strip().lower()

    # Map colloquial romanized terms across languages
    synonym_map = {
        "pani": "water", "paani": "water", "thanni": "water", "thanneer": "water", "neellu": "water", "neeru": "water",
        "kaapi": "coffee", "kapi": "coffee", "chai": "coffee", "tea": "coffee",
        "dosa": "plate", "dose": "plate", "tiffin": "food", "nashta": "food", "khana": "hungry", "oota": "hungry", "saapadu": "hungry", "bhojanam": "hungry",
        "auto": "auto-rickshaw", "meter": "meter", "rickshaw": "auto-rickshaw", "cab": "auto-rickshaw", "taxi": "auto-rickshaw",
        "kitna": "cost", "evvalavu": "cost", "enta": "cost", "price": "cost", "rate": "cost", "bele": "cost", "discount": "reduce",
        "namaste": "hello", "vanakkam": "hello", "namaskaram": "hello", "namaskara": "hello",
        "shukriya": "thank", "nandri": "thank", "dhanyavadalu": "thank", "thanks": "thank",
        "madad": "help", "udhavi": "help", "sahayam": "help", "sahaaya": "help",
        "baayein": "left", "idathu": "left", "edama": "left", "edakku": "left",
        "daayein": "right", "valathu": "right", "kudi": "right", "balakku": "right",
        "seedha": "straight", "neraga": "straight",
        "doctor": "doctor", "hospital": "hospital", "police": "police", "bus": "bus", "train": "railway",
    }
    expanded_queries = {q}
    if q in synonym_map:
        expanded_queries.add(synonym_map[q])

    matches = []
    seen = set()
    for cat_phrases in PHRASE_CATEGORIES.values():
        for p in cat_phrases:
            if p.english in seen:
                continue
            haystack = f"{p.english} {p.kannada} {p.phonetic} {p.hindi} {p.tamil} {p.telugu} {p.context_hint}".lower()
            if any(term in haystack for term in expanded_queries):
                matches.append(p)
                seen.add(p.english)
    return matches


# ── Interactive Situational Dialogues (Multilingual Roleplays) ───────

@dataclass
class ConversationTurn:
    speaker: str         # "Tourist" | "Local"
    kannada: str         # Spoken Kannada text
    phonetic: str        # Pronunciation guide
    english: str         # English translation
    hindi: str           # Hindi translation
    tamil: str           # Tamil translation
    telugu: str          # Telugu translation
    tip: str = ""        # Cultural context note


@dataclass
class TravelScenario:
    title: str
    icon: str
    location: str
    description: str
    turns: List[ConversationTurn]


TRAVEL_SCENARIOS: List[TravelScenario] = [
    TravelScenario(
        title="Haggling with an Auto-Rickshaw Driver",
        icon="🛺",
        location="Bengaluru (MG Road / Majestic) & Mysuru",
        description="Learn how to hail an auto, insist politely on the meter, or negotiate a fair fixed rate without conflict.",
        turns=[
            ConversationTurn(
                speaker="Tourist",
                kannada="ನಮಸ್ಕಾರ ಬಾಸ್, ಎಂ.ಜಿ. ರೋಡ್ ಗೆ ಹೋಗುತ್ತೀರಾ?",
                phonetic="Namaskāra boss, MG Road ge hōguttīrā?",
                english="Hello boss, will you go to MG Road?",
                hindi="नमस्ते भाई साहब, क्या आप एमजी रोड चलेंगे?",
                tamil="வணக்கம் பாஸ், எம்.ஜி. ரோட்டிற்கு போவீர்களா?",
                telugu="నమస్కారం బాస్, ఎం.జీ. రోడ్డుకి వెళ్తారా?",
                tip="Calling the driver 'Boss' or 'Sir' immediately sets a friendly, respectful tone.",
            ),
            ConversationTurn(
                speaker="Local Driver",
                kannada="ಹೌದು ಸಾರ್, ಬನ್ನಿ ಕೂತ್ಕೊಳ್ಳಿ. ₹100 ಆಗುತ್ತೆ.",
                phonetic="Haudu sir, banni kūtkoḷḷi. ₹100 āgutte.",
                english="Yes sir, come please sit. It will be ₹100.",
                hindi="हाँ सर, आइए बैठिए। ₹100 लगेगा।",
                tamil="ஆம் சார், வாருங்கள் உட்காருங்கள். ₹100 ஆகும்.",
                telugu="అవును సార్, రండి కూర్చోండి. ₹100 అవుతుంది.",
            ),
            ConversationTurn(
                speaker="Tourist",
                kannada="ದಯವಿಟ್ಟು ಮೀಟರ್ ಹಾಕಿ, ಮೀಟರ್ ಪ್ರಕಾರನೇ ಕೊಡ್ತೀನಿ.",
                phonetic="Dayaviṭṭu meter hāki, meter prakāranē koḍtīni.",
                english="Please turn on the meter, I will pay strictly by the meter.",
                hindi="कृपया मीटर चालू कीजिए, मैं मीटर के हिसाब से ही दूंगा।",
                tamil="தயவுசெய்து மீட்டர் போடுங்கள், மீட்டர் படியே தருகிறேன்.",
                telugu="దయచేసి మీటర్ వేయండి, మీటర్ ప్రకారమే ఇస్తాను.",
                tip="Polite insistence on the meter ('Dayaviṭṭu meter hāki') works in most central city areas.",
            ),
            ConversationTurn(
                speaker="Local Driver",
                kannada="ಸರಿ ಸಾರ್, ಮೀಟರ್ ಹಾಕಿದ್ದೀನಿ. ಬನ್ನಿ.",
                phonetic="Sari sir, meter hākiddīni. Banni.",
                english="Okay sir, I have turned on the meter. Please hop in.",
                hindi="ठीक है सर, मीटर चालू कर दिया है। बैठिए।",
                tamil="சரி சார், மீட்டர் போட்டுவிட்டேன். ஏறுங்கள்.",
                telugu="సరే సార్, మీటర్ వేశాను. ఎక్కండి.",
            ),
        ],
    ),
    TravelScenario(
        title="Ordering at a Traditional Darshini or Sagar Cafe",
        icon="☕",
        location="Udupi / Bengaluru / Davangere Darshinis",
        description="Experience Karnataka's unique self-service Darshini culture: buy a token, ask for crispy roast, and sip steaming filter coffee.",
        turns=[
            ConversationTurn(
                speaker="Tourist",
                kannada="ಒಂದು ಮಸಾಲೆ ದೋಸೆ ಮತ್ತು ಒಂದು ಫಿಲ್ಟರ್ ಕಾಫಿ ಕೊಡಿ.",
                phonetic="Ondu Masale Dose mattu ondu filter coffee koḍi.",
                english="Please give one Masala Dosa and one filter coffee.",
                hindi="एक मसाला डोसा और एक फ़िल्टर कॉफ़ी दीजिए।",
                tamil="ஒரு மசாலா தோசை மற்றும் ஒரு பில்டர் காபி கொடுங்கள்.",
                telugu="ఒక మసాలా దోశ మరియు ఒక ఫిల్టర్ కాఫీ ఇవ్వండి.",
                tip="At darshinis, collect your paper token from the cash counter first, then hand it to the kitchen counter.",
            ),
            ConversationTurn(
                speaker="Local Server",
                kannada="ದೋಸೆಗೆ ಸಾಂಬಾರ್ ಬೇಕಾ? ಇಲ್ಲಿ ಚಟ್ನಿ ಮಾತ್ರ ಕೊಡ್ತೀವಿ.",
                phonetic="Dōsege sāmbār bēkā? Illi chutney mātra koḍtīvi.",
                english="Do you need sambar? We traditionally serve only chutney here.",
                hindi="क्या डोसे के साथ सांभर चाहिए? यहाँ हम केवल चटनी देते हैं।",
                tamil="தோசைக்கு சாம்பார் வேண்டுமா? இங்கு சட்னி மட்டுமே வழங்குவோம்.",
                telugu="దోశతో పాటు సాంబార్ కావాలా? ఇక్కడ చట్నీ మాత్రమే ఇస్తాము.",
            ),
            ConversationTurn(
                speaker="Tourist",
                kannada="ಪರವಾಗಿಲ್ಲ, ಚಟ್ನಿ ಸಾಕು. ದೋಸೆ ಕ್ರಿಸ್ಪ್ ಆಗಿರಲಿ, ಖಾರ ಕಡಿಮೆ ಮಾಡಿ.",
                phonetic="Paravāgilla, chutney sāku. Dōse crisp āgirali, khāra kaḍime māḍi.",
                english="No problem, chutney is enough. Please make the dosa crispy with less spice.",
                hindi="कोई बात नहीं, चटनी काफी है। डोसा कुरकुरा रखिए और तीखा कम।",
                tamil="பரவாயில்லை, சட்னியே போதும். தோசை மொறுமொறுப்பாகவும் காரம் குறைவாகவும் இருக்கட்டும்.",
                telugu="పర్వాలేదు, చట్నీ చాలు. దోశ క్రిస్పీగా చేసి కారం తక్కువ వేయండి.",
            ),
            ConversationTurn(
                speaker="Local Server",
                kannada="ಖಂಡಿತ ಸಾರ್, ಎರಡು ನಿಮಿಷದಲ್ಲಿ ರೆಡಿ ಆಗುತ್ತೆ!",
                phonetic="Khaṇḍita sir, eraḍu nimiṣhadalli ready āgutte!",
                english="Certainly sir, it will be piping hot and ready in two minutes!",
                hindi="बिल्कुल सर, दो मिनट में तैयार हो जाएगा!",
                tamil="நிச்சயமாக சார், இரண்டு நிமிடங்களில் தயாராகிவிடும்!",
                telugu="తప్పకుండా సార్, రెండు నిమిషాల్లో రెడీ అవుతుంది!",
            ),
        ],
    ),
    TravelScenario(
        title="Shopping for Mysore Silk, Sandalwood & Spices",
        icon="🛍️",
        location="Devaraja Market (Mysuru) & Commercial Street",
        description="Bargain gracefully for GI-tagged Mysore Silk, pure sandalwood carvings, and Coorg spices.",
        turns=[
            ConversationTurn(
                speaker="Tourist",
                kannada="ಈ ಶ್ರೀಗಂಧದ ಕೆತ್ತನೆ ಮತ್ತು ರೇಷ್ಮೆ ಸೀರೆ ಬೆಲೆ ಎಷ್ಟು?",
                phonetic="Ī shrīgandhada kettane mattu rēṣhme sīre bele eṣhṭu?",
                english="How much does this sandalwood carving and silk saree cost?",
                hindi="इस चंदन की नक्काशी और रेशम साड़ी की कीमत कितनी है?",
                tamil="இந்த சந்தன சிற்பம் மற்றும் பட்டு சேலையின் விலை என்ன?",
                telugu="ఈ గంధపు చెక్కడము మరియు పట్టు చీర ధర ఎంత?",
                tip="Look for the official Silk Mark and Government Sandalwood Oil seal to guarantee authenticity.",
            ),
            ConversationTurn(
                speaker="Local Merchant",
                kannada="ಇದು ಗವರ್ನಮೆಂಟ್ ಸಿಲ್ಕ್ ಸಾರ್, ₹3,800. ಕ್ವಾಲಿಟಿ ಬೆಸ್ಟ್ ಇದೆ.",
                phonetic="Idu government silk sir, ₹3,800. Quality best ide.",
                english="This is genuine certified silk sir, ₹3,800. The quality is top-notch.",
                hindi="यह प्रमाणित रेशम है सर, ₹3,800। इसकी गुणवत्ता सर्वोत्तम है।",
                tamil="இது அரசு சான்றளிக்கப்பட்ட பட்டு சார், ₹3,800. தரம் மிகச் சிறந்தது.",
                telugu="ఇది ప్రభుత్వ గుర్తింపు పొందిన పట్టు సార్, ₹3,800. నాణ్యత చాలా బాగుంటుంది.",
            ),
            ConversationTurn(
                speaker="Tourist",
                kannada="ಸ್ವಲ್ಪ ಕಡಿಮೆ ಮಾಡಿ ಬಾಸ್, ಎರಡು ತಗೋತೀನಿ. UPI ಆಗುತ್ತಾ?",
                phonetic="Svalpa kaḍime māḍi boss, eraḍu tagōtīni. UPI āguttā?",
                english="Please reduce the price a little, I will take two. Do you accept UPI (Google Pay / PhonePe)?",
                hindi="थोड़ा कम कीजिए भाई साहब, मैं दो लूँगा। क्या UPI चलेगा?",
                tamil="கொஞ்சம் விலை குறைத்துக் கொடுங்கள், இரண்டு எடுக்கிறேன். UPI ஏற்குமா?",
                telugu="కొంచెం తగ్గించండి బాస్, రెండు తీసుకుంటాను. UPI తీసుకుంటారా?",
            ),
            ConversationTurn(
                speaker="Local Merchant",
                kannada="ಸರಿ, ₹3,500 ಕೊಡಿ. ಗೂಗಲ್ ಪೇ ಕ್ಯೂಆರ್ ಕೋಡ್ ಇಲ್ಲಿದೆ, ಸ್ಕ್ಯಾನ್ ಮಾಡಿ.",
                phonetic="Sari, ₹3,500 koḍi. Google Pay QR code illide, scan māḍi.",
                english="Alright, pay ₹3,500 each. The QR code is right here, you can scan and pay.",
                hindi="ठीक है, ₹3,500 दे दीजिए। QR कोड यहाँ है, स्कैन कर लीजिए।",
                tamil="சரி, ₹3,500 கொடுங்கள். QR கோட் இதோ உள்ளது, ஸ்கேன் செய்யுங்கள்.",
                telugu="సరే, ₹3,500 ఇవ్వండి. QR కోడ్ ఇక్కడే ఉంది, స్కాన్ చేయండి.",
            ),
        ],
    ),
    TravelScenario(
        title="Navigating KSRTC Bus Stand & Terminal Platforms",
        icon="🚌",
        location="Majestic (KBS) Bengaluru & Hassan Bus Stand",
        description="Find the right platform, ask the conductor for your destination, and request a window seat on state buses.",
        turns=[
            ConversationTurn(
                speaker="Tourist",
                kannada="ಕ್ಷಮಿಸಿ, ಹಂಪಿ / ಮೈಸೂರು ಗೆ ಹೋಗುವ ಬಸ್ ಯಾವ ಪ್ಲಾಟ್‌ಫಾರ್ಮ್ ನಲ್ಲಿ ಬರುತ್ತೆ?",
                phonetic="Kṣhamisi, Hampi / Mysuru ge hōguva bus yāva platform nalli barutte?",
                english="Excuse me, which platform does the bus to Hampi / Mysuru depart from?",
                hindi="माफ़ कीजिए, हम्पी / मैसूर जाने वाली बस किस प्लेटफ़ॉर्म पर आएगी?",
                tamil="மன்னிக்கவும், ஹம்பி / மைசூர் செல்லும் பேருந்து எந்த பிளாட்பாரத்தில் வரும்?",
                telugu="క్షమించండి, హంపి / మైసూర్ వెళ్లే బస్సు ఏ ప్లాట్‌ఫారమ్‌పై వస్తుంది?",
            ),
            ConversationTurn(
                speaker="Local Conductor",
                kannada="ಪ್ಲಾಟ್‌ಫಾರ್ಮ್ ನಂಬರ್ 12 ಕ್ಕೆ ಹೋಗಿ, ಏರಾವತ್ ಬಸ್ ಇನ್ನು ಹತ್ತು ನಿಮಿಷದಲ್ಲಿ ಹೊರಡುತ್ತೆ.",
                phonetic="Platform number 12 kke hōgi, Airavat bus innu hattu nimiṣhadalli horaḍutte.",
                english="Head to platform 12, the Airavat AC bus leaves in ten minutes.",
                hindi="प्लेटफ़ॉर्म नंबर 12 पर जाइए, ऐरावत एसी बस दस मिनट में निकलेगी।",
                tamil="பிளாட்பாரம் 12-க்கு செல்லுங்கள், ஐராவத் பேருந்து இன்னும் பத்து நிமிடத்தில் புறப்படும்.",
                telugu="ప్లాట్‌ఫారమ్ నంబర్ 12 కి వెళ్ళండి, ఐరావత్ బస్సు పది నిమిషాల్లో బయలుదేరుతుంది.",
            ),
            ConversationTurn(
                speaker="Tourist",
                kannada="ತುಂಬಾ ಧನ್ಯವಾದಗಳು! ಕಿಟಕಿ ಸೀಟ್ ಸಿಗುತ್ತಾ?",
                phonetic="Tumbā dhanyavādagaḷu! Kiṭaki seat siguttā?",
                english="Thank you very much! Is a window seat available?",
                hindi="बहुत-बहुत धन्यवाद! क्या खिड़की वाली सीट मिल सकती है?",
                tamil="மிக்க நன்றி! ஜன்னல் ஓர இருக்கை கிடைக்குமா?",
                telugu="చాలా ధన్యవాదాలు! కిటికీ పక్క సీటు దొరుకుతుందా?",
            ),
        ],
    ),
]


# ── UI Localization Strings for the 5 Supported Languages ───────────

UI_LOCALIZATION = {
    "English": {
        "brand_subtitle": "Intelligent Travel Companion for Karnataka",
        "badge_hackathon": "🏆 Hackathon 2026 Edition",
        "badge_ai": "🟢 Dual-Engine AI Active",
        "view_tutorial": "📖 View Tutorial",
        "language_label": "🌐 Language",
        "quick_launch": "⚡ Quick-Launch",
        "enter_app": "🚀 Enter KannadaYatra AI & Start Exploring",
        "plan_this_trip": "👑 Plan This Trip",
        "generate_itinerary": "🚀 Generate My Itinerary",
        "download_pass": "📥 Download Travel Pass (.txt)",
        "optimal_timing": "⏰ Optimal Timing",
        "local_secret": "🍛 Local Food Secret",
        "transit_tip": "🚌 Transit Tip",
        "days": "Days",
        "budget": "Budget",
        "travelers": "Travelers",
        "listen": "🔊 Listen",
        "show_local": "📱 Show to Driver / Local (Full Screen)",
        "search_phrases_placeholder": "🔍 Search words in English, Hindi, Tamil, Telugu, or Kannada (e.g. 'coffee', 'auto', 'water', 'paani', 'neellu')...",
        "mother_tongue_prompt": "Select Your Native Language (for translation & phonetic guidance):",
        "explore_tab": "🏠 Explore & Circuits",
        "builder_tab": "⚙️ Custom Trip Planner",
        "itinerary_tab": "📍 Itinerary & Route Map",
        "survival_tab": "🗣️ Multilingual Survival Kit",
        "budget_tab": "💰 Budget Optimizer",
        "culture_tab": "🎭 Cultural Explorer",
        "guide_tab": "🧭 User Guide & Tutorial",
    },
    "Kannada": {
        "brand_subtitle": "ಕರ್ನಾಟಕ ಪ್ರವಾಸ ಸಹಾಯಕ • ಕನ್ನಡ ಡಿಜಿಟಲ್ ನಾವೀನ್ಯತೆ",
        "badge_hackathon": "🏆 ಹ್ಯಾಕಥಾನ್ 2026 ಆವೃತ್ತಿ",
        "badge_ai": "🟢 ಡ್ಯುಯಲ್-ಎಂಜಿನ್ AI ಸಕ್ರಿಯ",
        "view_tutorial": "📖 ಮಾರ್ಗದರ್ಶಿ ವೀಕ್ಷಿಸಿ",
        "language_label": "🌐 ಭಾಷೆ",
        "quick_launch": "⚡ ತ್ವರಿತ ಆರಂಭ",
        "enter_app": "🚀 ಅನ್ವೇಷಣೆ ಆರಂಭಿಸಿ",
        "plan_this_trip": "👑 ಈ ಪ್ರವಾಸವನ್ನು ಯೋಜಿಸಿ",
        "generate_itinerary": "🚀 ಪ್ರವಾಸ ವಿವರವನ್ನು ರಚಿಸಿ",
        "download_pass": "📥 ಪ್ರವಾಸ ಪಾಸ್ ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ (.txt)",
        "optimal_timing": "⏰ ಸೂಕ್ತ ಸಮಯ",
        "local_secret": "🍛 ಸ್ಥಳೀಯ ಆಹಾರ ರಹಸ್ಯ",
        "transit_tip": "🚌 ಸಾರಿಗೆ ಸಲಹೆ",
        "days": "ದಿನಗಳು",
        "budget": "ಬಜೆಟ್",
        "travelers": "ಪ್ರವಾಸಿಗರು",
        "listen": "🔊 ಆಲಿಸಿ",
        "show_local": "📱 ಚಾಲಕ / ಅಂಗಡಿಯವರಿಗೆ ತೋರಿಸಿ",
        "search_phrases_placeholder": "🔍 ಇಂಗ್ಲಿಷ್, ಹಿಂದಿ, ತಮಿಳು, ತೆಲುಗು ಅಥವಾ ಕನ್ನಡದಲ್ಲಿ ಹುಡುಕಿ...",
        "mother_tongue_prompt": "ನಿಮ್ಮ ಮಾತೃಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ:",
        "explore_tab": "🏠 ಅನ್ವೇಷಣೆ ಮತ್ತು ಪ್ರವಾಸಗಳು",
        "builder_tab": "⚙️ ಕಸ್ಟಮ್ ಪ್ರವಾಸ ಯೋಜನೆ",
        "itinerary_tab": "📍 ಪ್ರವಾಸ ವಿವರ & ನಕ್ಷೆ",
        "survival_tab": "🗣️ ಬಹುಭಾಷಾ ಸಂವಹನ ಕಿಟ್",
        "budget_tab": "💰 ಬಜೆಟ್ ಆಪ್ಟಿಮೈಜರ್",
        "culture_tab": "🎭 ಸಾಂಸ್ಕೃತಿಕ ಅನ್ವೇಷಣೆ",
        "guide_tab": "🧭 ಬಳಕೆದಾರ ಮಾರ್ಗದರ್ಶಿ",
    },
    "Hindi": {
        "brand_subtitle": "कर्नाटक का बुद्धिमान और सांस्कृतिक यात्रा साथी",
        "badge_hackathon": "🏆 हैकाथॉन 2026 संस्करण",
        "badge_ai": "🟢 डुअल-इंजन AI सक्रिय",
        "view_tutorial": "📖 ट्यूटोरियल देखें",
        "language_label": "🌐 भाषा",
        "quick_launch": "⚡ त्वरित शुरुआत",
        "enter_app": "🚀 कन्नड़यात्रा AI में प्रवेश करें",
        "plan_this_trip": "👑 यह यात्रा प्लान करें",
        "generate_itinerary": "🚀 मेरा यात्रा कार्यक्रम बनाएं",
        "download_pass": "📥 यात्रा पास डाउनलोड करें (.txt)",
        "optimal_timing": "⏰ सबसे अच्छा समय",
        "local_secret": "🍛 स्थानीय स्वादिष्ट भोजन",
        "transit_tip": "🚌 यात्रा व बस टिप",
        "days": "दिन",
        "budget": "बजट",
        "travelers": "यात्री",
        "listen": "🔊 सुनें",
        "show_local": "📱 ड्राइवर / दुकानदार को दिखाएं",
        "search_phrases_placeholder": "🔍 अंग्रेजी, हिंदी, तमिल, तेलुगु या कन्नड़ में खोजें (जैसे 'कॉफी', 'ऑटो', 'पानी')...",
        "mother_tongue_prompt": "अपनी मातृभाषा चुनें (अनुवाद और उच्चारण के लिए):",
        "explore_tab": "🏠 पर्यटन एवं सर्किट",
        "builder_tab": "⚙️ यात्रा योजनाकार",
        "itinerary_tab": "📍 यात्रा कार्यक्रम एवं मानचित्र",
        "survival_tab": "🗣️ बहुभाषी संवाद किट",
        "budget_tab": "💰 बजट कैलकुलेटर",
        "culture_tab": "🎭 सांस्कृतिक अन्वेषण",
        "guide_tab": "🧭 उपयोगकर्ता मार्गदर्शिका",
    },
    "Tamil": {
        "brand_subtitle": "கர்நாடகாவின் அறிவார்ந்த மற்றும் கலாச்சார பயண வழிகாட்டி",
        "badge_hackathon": "🏆 ஹேக்கத்தான் 2026 பதிப்பு",
        "badge_ai": "🟢 இரட்டை-இயந்திர AI இயங்குகிறது",
        "view_tutorial": "📖 வழிகாட்டியைப் பார்க்கவும்",
        "language_label": "🌐 மொழி",
        "quick_launch": "⚡ விரைவு தொடக்கம்",
        "enter_app": "🚀 பயணத்தை தொடங்குங்கள்",
        "plan_this_trip": "👑 இந்த பயணத்தைத் திட்டமிடுங்கள்",
        "generate_itinerary": "🚀 பயண அட்டவணையை உருவாக்குங்கள்",
        "download_pass": "📥 பயண பாஸை பதிவிறக்கவும் (.txt)",
        "optimal_timing": "⏰ உகந்த நேரம்",
        "local_secret": "🍛 உள்ளூர் உணவு ரகசியம்",
        "transit_tip": "🚌 போக்குவரத்து குறிப்பு",
        "days": "நாட்கள்",
        "budget": "பட்ஜெட்",
        "travelers": "பயணிகள்",
        "listen": "🔊 கேட்கவும்",
        "show_local": "📱 டிரைவர் / கடைக்காரரிடம் காட்டவும்",
        "search_phrases_placeholder": "🔍 ஆங்கிலம், இந்தி, தமிழ், தெலுங்கு அல்லது கன்னடத்தில் தேடுங்கள்...",
        "mother_tongue_prompt": "உங்கள் தாய்மொழியைத் தேர்ந்தெடுக்கவும்:",
        "explore_tab": "🏠 சுற்றுலா & சுற்றுகள்",
        "builder_tab": "⚙️ பயணத் திட்டமிடுபவர்",
        "itinerary_tab": "📍 பயண வரைபடம் & திட்டம்",
        "survival_tab": "🗣️ பன்மொழி உரையாடல் கிட்",
        "budget_tab": "💰 பட்ஜெட் வழிகாட்டி",
        "culture_tab": "🎭 கலாச்சார ஆய்வு",
        "guide_tab": "🧭 பயனர் வழிகாட்டி",
    },
    "Telugu": {
        "brand_subtitle": "కర్ణాటక కోసం తెలివైన సాంస్కృతిక ప్రయాణ సహచరుడు",
        "badge_hackathon": "🏆 హ్యాకథాన్ 2026 ఎడిషన్",
        "badge_ai": "🟢 డ్యూయల్-ఇంజిన్ AI యాక్టివ్",
        "view_tutorial": "📖 ట్యుటోరియల్ చూడండి",
        "language_label": "🌐 భాష",
        "quick_launch": "⚡ త్వరిత ప్రారంభం",
        "enter_app": "🚀 ప్రయాణాన్ని ప్రారంభించండి",
        "plan_this_trip": "👑 ఈ ట్రిప్‌ను ప్లాన్ చేయండి",
        "generate_itinerary": "🚀 ప్రయాణ షెడ్యూల్‌ను రూపొందించండి",
        "download_pass": "📥 ప్రయాణ పాస్‌ను డౌన్‌లోడ్ చేయండి (.txt)",
        "optimal_timing": "⏰ అనుకూలమైన సమయం",
        "local_secret": "🍛 స్థానిక ఆహార రహస్యం",
        "transit_tip": "🚌 ప్రయాణ చిట్కా",
        "days": "రోజులు",
        "budget": "బడ్జెట్",
        "travelers": "ప్రయాణికులు",
        "listen": "🔊 వినండి",
        "show_local": "📱 డ్రైవర్ / దుకాణదారునికి చూపించండి",
        "search_phrases_placeholder": "🔍 ఇంగ్లీష్, హిందీ, తమిళం, తెలుగు లేదా కన్నడలో శోధించండి...",
        "mother_tongue_prompt": "మీ మాతృభాషను ఎంచుకోండి:",
        "explore_tab": "🏠 అన్వేషణ & సర్క్యూట్లు",
        "builder_tab": "⚙️ ప్రయాణ ప్రణాళిక",
        "itinerary_tab": "📍 ప్రయాణ పటం & షెడ్యూల్",
        "survival_tab": "🗣️ బహుభాషా సంభాషణ కిట్",
        "budget_tab": "💰 బడ్జెట్ ఆప్టిమైజర్",
        "culture_tab": "🎭 సాంస్కృతిక విశేషాలు",
        "guide_tab": "🧭 గైడ్ & ట్యుటోరియల్",
    },
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2.  REGIONAL CULINARY SPECIALTIES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class RegionalCuisine:
    """Culinary identity of a Karnataka sub-region."""
    region: str
    signature_dishes: List[str]
    must_try: str                     # single top recommendation
    food_culture_note: str


REGIONAL_CUISINES: Dict[str, RegionalCuisine] = {
    "Mysore Region": RegionalCuisine(
        region="Mysore Region",
        signature_dishes=["Mysore Masala Dosa", "Mysore Pak", "Mysore Bonda",
                          "Chiroti", "Nanjangud Banana Chips"],
        must_try="Mysore Pak from the original Guru Sweet Mart",
        food_culture_note="Mysore's food culture is rooted in the Wadiyar royal kitchen traditions. "
                          "The city's *Mysore Pak* was accidentally invented by the royal chef."
    ),
    "North Karnataka": RegionalCuisine(
        region="North Karnataka",
        signature_dishes=["Jolada Rotti (Jowar Flatbread)", "Ennegai (Stuffed Brinjal)",
                          "Badanekai Yennegai", "Dharwad Pedha", "Davangere Benne Dosa",
                          "Holige (Puran Poli)", "Mirchi Bajji"],
        must_try="Davangere Benne Dosa - dripping with butter, served with spicy chutney",
        food_culture_note="North Karnataka cuisine is heartier and spicier, built around *jowar* "
                          "(sorghum) rotis. Dharwad's milk pedha is a nationally recognised sweet."
    ),
    "Coastal Karnataka": RegionalCuisine(
        region="Coastal Karnataka",
        signature_dishes=["Mangalorean Fish Gassi", "Neer Dosa", "Kori Rotti",
                          "Kane Fry (Lady Fish)", "Udupi Sambar", "Goli Baje",
                          "Pundi (Steamed Rice Dumplings)"],
        must_try="Neer Dosa with Chicken Sukka at a Mangalorean home-style restaurant",
        food_culture_note="Coastal cuisine blends coconut, kokum, and fresh seafood. Udupi is the "
                          "birthplace of India's vegetarian restaurant tradition."
    ),
    "Western Ghats": RegionalCuisine(
        region="Western Ghats",
        signature_dishes=["Pandi Curry (Kodava Pork)", "Kadambuttu (Rice Balls)",
                          "Bamboo Shoot Curry", "Akki Rotti", "Estate-fresh Filter Coffee"],
        must_try="Pandi Curry with Kadambuttu - the signature Kodava feast",
        food_culture_note="Kodava (Coorg) cuisine is unique to its warrior culture - "
                          "rich, meat-heavy, and infused with local spices grown in the estates."
    ),
    "Bangalore Region": RegionalCuisine(
        region="Bangalore Region",
        signature_dishes=["Bisi Bele Bath", "Ragi Mudde (Finger Millet Balls)",
                          "Masala Puri", "Mangalore Buns", "Craft Beer"],
        must_try="VV Puram Food Street for a dosa-to-dessert walking tour",
        food_culture_note="Bangalore is Karnataka's melting pot - from traditional *darshini* "
                          "eateries to India's craft beer capital with 60+ microbreweries."
    ),
    "Hassan Region": RegionalCuisine(
        region="Hassan Region",
        signature_dishes=["Ragi Mudde", "Saaru (Rasam)", "Kosambari",
                          "Obbattu (Holige)", "Balehannu Payasa (Banana Kheer)"],
        must_try="Ragi Mudde with spicy Saaru - the heartland comfort meal",
        food_culture_note="Hassan's cuisine reflects Old Mysuru's agricultural roots - "
                          "ragi (finger millet) is the staple grain, served at every meal."
    ),
}


def get_cuisine_for_region(region: str) -> Optional[RegionalCuisine]:
    """Look up culinary info for a region."""
    return REGIONAL_CUISINES.get(region)


def get_cuisine_for_destination(dest_name: str) -> Optional[RegionalCuisine]:
    """Get cuisine based on destination's region."""
    from utils.helpers import KARNATAKA_DESTINATIONS
    dest = KARNATAKA_DESTINATIONS.get(dest_name)
    if dest:
        return REGIONAL_CUISINES.get(dest.region)
    return None


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3.  FESTIVAL CALENDAR - major Karnataka festivals by month
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class Festival:
    """Karnataka festival with cultural context."""
    name: str
    months: List[str]            # e.g. ["October", "November"]
    region: str                  # where it's biggest
    description: str
    traveler_tip: str


KARNATAKA_FESTIVALS: List[Festival] = [
    Festival(
        "Mysore Dasara", ["September", "October"],
        "Mysore Region",
        "Karnataka's grandest festival - 10 days of Navaratri culminating in a spectacular "
        "royal procession (Jamboo Savari) with the golden howdah atop a caparisoned elephant.",
        "Book Mysore hotels 2-3 months ahead. The Palace illumination with 100,000 bulbs is unmissable."
    ),
    Festival(
        "Hampi Utsav (Vijaya Utsav)", ["November"],
        "North Karnataka",
        "A 3-day festival recreating the glory of the Vijayanagara Empire with dance, music, "
        "puppet shows, fireworks, and grand processions among the ruins.",
        "Stay in Hospet (14 km away) for better hotel options. Arrive early for the best views."
    ),
    Festival(
        "Ugadi (Kannada New Year)", ["March", "April"],
        "All Karnataka",
        "The Kannada New Year marked by the ritual tasting of *Bevu-Bella* (neem and jaggery) "
        "symbolising life's mix of bitter and sweet. Homes are decorated with mango leaf torans.",
        "Visit any local home or temple for an authentic experience. Special festive meals are served."
    ),
    Festival(
        "Makar Sankranti / Suggi", ["January"],
        "All Karnataka",
        "The harvest festival celebrated with *Ellu-Bella* (sesame-jaggery mix) exchanges, "
        "kite flying, and bonfires. In rural areas, cattle are decorated and worshipped.",
        "Head to rural Karnataka or Bangalore's parks to witness traditional kite-flying."
    ),
    Festival(
        "Karaga Festival", ["March", "April"],
        "Bangalore Region",
        "Bangalore's oldest festival (predating the city itself) honoring Draupadi. "
        "A priest carries a flower-decked *karaga* pot on his head through the old city all night.",
        "The midnight procession through Bangalore's oldest streets is a unique experience."
    ),
    Festival(
        "Pattadakal Dance Festival", ["January", "February"],
        "North Karnataka",
        "Classical dance performances set against the backdrop of UNESCO heritage temples. "
        "Features Bharatanatyam, Kathak, Odissi, and Kuchipudi by nationally renowned artists.",
        "Combine with visits to Badami and Aihole - all three are within 30 km of each other."
    ),
    Festival(
        "Kodagu (Coorg) Huthri", ["November", "December"],
        "Western Ghats",
        "The Kodava harvest festival celebrating the first rice harvest. Families gather in "
        "ancestral homes (*ainmane*) for traditional feasts, folk dances, and ritual ceremonies.",
        "If invited to a Kodava home, don't refuse - the hospitality and feast are legendary."
    ),
    Festival(
        "Kambala (Buffalo Race)", ["November", "December", "January", "February"],
        "Coastal Karnataka",
        "Traditional buffalo race in muddy, waterlogged paddy fields - a spectacular and "
        "adrenaline-pumping rural sporting tradition of the Tulu Nadu region.",
        "Events happen in villages near Mangalore/Udupi. Check local dates as they vary."
    ),
    Festival(
        "Mahamastakabhisheka", ["Once every 12 years"],
        "Hassan Region",
        "The grand anointing of the Gommateshwara statue at Shravanabelagola with milk, "
        "saffron, and sandalwood paste. Next occurrence: 2030.",
        "This 12-yearly event draws millions. Plan way ahead if timing aligns."
    ),
    Festival(
        "Banashankari Fair", ["January", "February"],
        "North Karnataka",
        "A vibrant temple fair at Banashankari near Badami with folk performances, "
        "local handicrafts, bullock-cart races, and traditional North Karnataka food stalls.",
        "Combine with the Chalukyan temple circuit - Badami, Aihole, Pattadakal."
    ),
]


def get_festivals_for_region(region: str) -> List[Festival]:
    """Return festivals most relevant to a region (including pan-Karnataka ones)."""
    return [
        f for f in KARNATAKA_FESTIVALS
        if f.region == region or f.region == "All Karnataka"
    ]


def get_festivals_by_month(month: str) -> List[Festival]:
    """Return festivals happening in a given month."""
    return [f for f in KARNATAKA_FESTIVALS if month in f.months]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4.  HERITAGE HISTORY SNAPSHOTS - tied to destinations
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HERITAGE_HISTORIES: Dict[str, str] = {
    "Mysore Palace":
        "Built between 1897-1912 after the old wooden palace burned down, the Amba Vilas Palace "
        "was designed by British architect Henry Irwin in the Indo-Saracenic style. It was the seat "
        "of the Wadiyar dynasty who ruled the Kingdom of Mysore for nearly 600 years. The palace "
        "houses the legendary Golden Throne and the Golden Howdah used during the Dasara procession.",

    "Hampi":
        "Hampi was the capital of the Vijayanagara Empire (1336-1646), once one of the largest and "
        "richest cities in the world with a population exceeding 500,000. The empire's wealth came "
        "from the spice and cotton trade. After the Battle of Talikota (1565), the city was sacked "
        "and left in ruins. Today, its 1,600+ monuments across 26 sq km stand as a UNESCO World Heritage Site.",

    "Badami":
        "Badami (ancient Vatapi) was the capital of the Early Chalukya dynasty (6th-8th century). "
        "The four rock-cut cave temples - three Hindu and one Jain - are carved into soft red "
        "sandstone and represent some of the earliest examples of Dravidian architecture. The Chalukyas "
        "pioneered temple-building traditions that influenced architecture across South India.",

    "Pattadakal":
        "A UNESCO World Heritage Site, Pattadakal served as the coronation ground of Chalukyan kings. "
        "Its group of 10 temples (7th-8th century) showcases a unique blend of Northern (Nagara) and "
        "Southern (Dravidian) architectural styles, representing the climax of Chalukyan artistic achievement.",

    "Bijapur (Vijayapura)":
        "Bijapur was the capital of the Adil Shahi dynasty (1489-1686), one of the five Deccan "
        "Sultanates. The Gol Gumbaz, built in 1656, houses the world's second-largest dome (44m "
        "diameter) and a 'whispering gallery' where a whisper can be heard across 37 meters. "
        "Ibrahim Rouza, the inspiration for the Taj Mahal, stands as a masterpiece of Deccan architecture.",

    "Belur":
        "The Chennakeshava Temple at Belur was commissioned by Hoysala King Vishnuvardhana in 1117 AD "
        "to celebrate his victory and conversion from Jainism to Vaishnavism. It took 103 years to "
        "complete. The temple's exterior has 48 intricately carved bracket figures (madanika) depicting "
        "celestial dancers, each unique and detailed down to their jewelry and hairstyles.",

    "Halebidu":
        "Halebidu ('Old Capital') was the regal capital of the Hoysala Empire. The Hoysaleshwara "
        "Temple (1121 AD) is the largest monument dedicated to Shiva by the Hoysalas. Its exterior "
        "walls carry an unbroken frieze of over 12,000 sculpted figures - elephants, lions, horsemen, "
        "scrollwork, and scenes from the Ramayana and Mahabharata - with no two figures alike.",

    "Shravanabelagola":
        "Home to the 57-foot Gommateshwara (Bahubali) monolith, carved in 981 AD by the Ganga "
        "dynasty minister Chamundaraya. It is the world's tallest free-standing monolithic statue. "
        "The site has been a major Jain pilgrimage centre for over 2,000 years, with inscriptions "
        "dating back to the 3rd century BCE - the earliest Kannada epigraph.",

    "Srirangapatna":
        "The island fortress of Srirangapatna on the Kaveri River was the de facto capital of Mysore "
        "under Hyder Ali and his son Tipu Sultan (the 'Tiger of Mysore'). Tipu's innovative rocket "
        "artillery inspired the British Congreve rockets. He fell in the Fourth Anglo-Mysore War (1799) "
        "defending this very fort against British forces.",

    "Coorg (Kodagu)":
        "The Kodavas of Coorg are a unique warrior community with their own language, customs, and "
        "martial traditions - they are the only community in India permitted to carry firearms without "
        "a license. Coffee was introduced here by Baba Budan in the 17th century, making Coorg one of "
        "India's first coffee-growing regions. The region's *ainmane* (ancestral homes) and distinct "
        "culture remain fiercely preserved.",

    "Gokarna":
        "Gokarna is one of the seven sacred pilgrimage sites (Muktisthala) in Karnataka. According "
        "to legend, the Atmalinga emerged here from the ear of a cow (Go = cow, Karna = ear). "
        "The Mahabaleshwar Temple is believed to house the original Atmalinga brought by Ravana. "
        "The town balances its ancient spiritual heritage with its modern reputation as a beach paradise.",

    "Mangalore":
        "Known as Mangaluru, this port city has been a maritime trading hub for over 1,400 years, "
        "connecting the Malabar Coast to Arabian and Southeast Asian trade routes. The city's "
        "distinctive Mangalorean tile-roofed architecture, its unique blend of Tulu, Konkani, and "
        "Beary cultures, and its legendary seafood cuisine make it one of Karnataka's most cosmopolitan cities.",
}


def get_heritage_history(dest_name: str) -> Optional[str]:
    """Return heritage history narrative for a destination, if available."""
    return HERITAGE_HISTORIES.get(dest_name)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5.  CULTURAL CONTEXT AGGREGATOR - one-call function
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class CulturalContext:
    """Aggregated cultural information for a single destination."""
    destination_name: str
    history: Optional[str]
    cuisine: Optional[RegionalCuisine]
    festivals: List[Festival]
    survival_phrases: Dict[str, List[KannadaPhrase]]


def get_full_cultural_context(dest_name: str) -> CulturalContext:
    """
    One-stop function that gathers all cultural intelligence for a
    given destination: history, cuisine, festivals, and language kit.
    """
    from utils.helpers import KARNATAKA_DESTINATIONS

    dest = KARNATAKA_DESTINATIONS.get(dest_name)
    region = dest.region if dest else "All Karnataka"

    return CulturalContext(
        destination_name=dest_name,
        history=get_heritage_history(dest_name),
        cuisine=get_cuisine_for_destination(dest_name),
        festivals=get_festivals_for_region(region),
        survival_phrases=get_context_phrases(dest_name),
    )

