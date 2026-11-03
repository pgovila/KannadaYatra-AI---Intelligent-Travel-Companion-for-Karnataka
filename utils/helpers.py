"""
utils/helpers.py - KannadaYatra AI
Budget calculations, session-state management, Karnataka destination
database, and reusable UI asset helpers.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import streamlit as st

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1.  DESTINATION DATABASE - comprehensive Karnataka tourism data
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class Destination:
    """Single Karnataka tourism destination with rich metadata."""
    name: str
    region: str                       # e.g. "Mysore Region"
    lat: float
    lon: float
    categories: List[str]             # Heritage | Nature | Food | Adventure
    description: str
    best_season: str                  # e.g. "Oct-Feb"
    time_needed_hrs: float            # typical visit duration
    entry_fee_inr: int                # 0 if free
    highlights: List[str]
    nearby: List[str] = field(default_factory=list)
    secret_eatery: str = ""           # Authentic foodie spot locals swear by
    best_time_of_day: str = ""        # Golden hour / crowd avoidance
    transit_tip: str = ""             # Real-world bus/train connection info
    crowd_level: str = "Moderate"     # Low / Moderate / High


# fmt: off
KARNATAKA_DESTINATIONS: Dict[str, Destination] = {
    # ── Mysore Region ────────────────────────────────────────────
    "Mysore Palace": Destination(
        name="Mysore Palace", region="Mysore Region",
        lat=12.3051, lon=76.6551,
        categories=["Heritage"],
        description="The opulent seat of the Wadiyar dynasty, one of India's most visited monuments. "
                    "Its Indo-Saracenic architecture dazzles with 100,000 golden incandescent bulbs during Dasara.",
        best_season="Oct-Feb", time_needed_hrs=3, entry_fee_inr=70,
        highlights=["Durbar Hall", "Golden Howdah", "Dasara Illumination"],
        nearby=["Chamundi Hills", "Brindavan Gardens", "Srirangapatna"],
        secret_eatery="Guru Sweet Mart (Sayyaji Rao Rd) - Originator of Mysore Pak in 1935",
        best_time_of_day="5:00 PM for golden sunset, stay until 7:00 PM for evening facade lighting",
        transit_tip="Vande Bharat Express from Bangalore (1h 45m) or KSRTC Flybus direct from BLR Airport",
        crowd_level="High on weekends, peaceful before 11:00 AM on weekdays"
    ),
    "Chamundi Hills": Destination(
        name="Chamundi Hills", region="Mysore Region",
        lat=12.2724, lon=76.6704,
        categories=["Heritage", "Nature"],
        description="Sacred hillock rising 1,000 meters above Mysore with the iconic Chamundeshwari Temple and "
                    "the monolithic 16-foot Nandi Bull carved from a single black granite boulder.",
        best_season="Year-round", time_needed_hrs=2, entry_fee_inr=0,
        highlights=["Chamundeshwari Temple", "Monolithic Nandi Bull", "Mysore Panoramic View"],
        nearby=["Mysore Palace"],
        secret_eatery="Mylari Hotel (Nazarbad) - Ultra-soft Mylari Butter Masala Dosa",
        best_time_of_day="5:30 AM sunrise climb up the 1,008 stone steps",
        transit_tip="City bus Route 201 runs every 10 mins from Mysore City Bus Stand",
        crowd_level="Peak on Tuesdays & Fridays; serene early mornings"
    ),
    "Brindavan Gardens": Destination(
        name="Brindavan Gardens", region="Mysore Region",
        lat=12.4214, lon=76.5729,
        categories=["Nature"],
        description="Historic terraced gardens situated across the Krishna Raja Sagara (KRS) Dam, designed in Mughal "
                    "style with vibrant cascades, botanical walks, and an evening musical fountain show.",
        best_season="Year-round", time_needed_hrs=2.5, entry_fee_inr=30,
        highlights=["Musical Dancing Fountain", "Terraced Botanical Lawns", "KRS Reservoir"],
        nearby=["Mysore Palace", "Srirangapatna"],
        secret_eatery="Local Kaveri river fish fry stalls near the KRS dam gate",
        best_time_of_day="5:30 PM to catch both sunset over the dam and the 7:00 PM musical fountain",
        transit_tip="21 km from Mysore city center. KSRTC buses run frequently from city stand",
        crowd_level="High in the evening, low in afternoon"
    ),
    "Srirangapatna": Destination(
        name="Srirangapatna", region="Mysore Region",
        lat=12.4181, lon=76.6947,
        categories=["Heritage"],
        description="Island fortress town embraced by the sacred Kaveri River. The bastion of Tipu Sultan "
                    "with the colossal Sri Ranganathaswamy Temple, Daria Daulat Bagh, and Gumbaz mausoleum.",
        best_season="Oct-Mar", time_needed_hrs=3, entry_fee_inr=20,
        highlights=["Tipu's Water Gate & Fort", "Sri Ranganathaswamy Temple", "Daria Daulat Bagh"],
        nearby=["Mysore Palace", "Brindavan Gardens"],
        secret_eatery="Ranganatha Tiffin Room - Traditional banana leaf curd rice and filter coffee",
        best_time_of_day="Morning 8:30 AM before heat builds up across the fortress grounds",
        transit_tip="Situated directly on the Bangalore-Mysore Expressway; easy stopover hop",
        crowd_level="Moderate"
    ),

    # ── Hampi / North-Central ────────────────────────────────────
    "Hampi": Destination(
        name="Hampi", region="North Karnataka",
        lat=15.3350, lon=76.4600,
        categories=["Heritage"],
        description="UNESCO World Heritage Site - the legendary capital of the 14th-century Vijayanagara Empire. "
                    "A surreal landscape of giant granite boulders, 1,600+ monuments, and the iconic Stone Chariot.",
        best_season="Oct-Feb", time_needed_hrs=8, entry_fee_inr=40,
        highlights=["Stone Chariot at Vittala", "Virupaksha Temple", "Matanga Hill Sunrise", "Coracle Ride on Tungabhadra"],
        nearby=["Badami", "Aihole", "Pattadakal"],
        secret_eatery="Mango Tree Restaurant & local Jolada Rotti Khanavalis near Hampi Bazaar",
        best_time_of_day="6:00 AM on Matanga Hill for sunrise; 5:00 PM at Hemakuta Hill for sunset",
        transit_tip="Overnight Hampi Express train from Bangalore to Hospet (13 km from Hampi)",
        crowd_level="Moderate; sprawling 26 sq km ensures serene spaces even during peak season"
    ),
    "Badami": Destination(
        name="Badami", region="North Karnataka",
        lat=15.9199, lon=75.6822,
        categories=["Heritage"],
        description="Ancient capital of the Early Chalukyas, famous for four rock-cut cave temples chiseled into "
                    "towering red sandstone cliffs overlooking the emerald waters of Agastya Lake.",
        best_season="Oct-Mar", time_needed_hrs=4, entry_fee_inr=25,
        highlights=["Rock-cut Cave Temples", "Agastya Lake", "Bhutanatha Temple at Water's Edge"],
        nearby=["Aihole", "Pattadakal", "Hampi"],
        secret_eatery="Sri Banashankari Khanavali - Authentic North Karnataka Jowar Rotti Meals with Shengachutney",
        best_time_of_day="Late afternoon (3:30-5:30 PM) when the red sandstone glows fiery bronze in sunlight",
        transit_tip="Connected via Bagalkot railhead; KSRTC buses connect Badami, Pattadakal, and Aihole",
        crowd_level="Low to Moderate"
    ),
    "Aihole": Destination(
        name="Aihole", region="North Karnataka",
        lat=16.0178, lon=75.8813,
        categories=["Heritage"],
        description="Known as the 'Cradle of Indian Temple Architecture' with over 125 stone temples dating from "
                    "450 to 1200 CE, showcasing the earliest experimental stages of Dravidian and Nagara styles.",
        best_season="Oct-Mar", time_needed_hrs=3, entry_fee_inr=25,
        highlights=["Durga Temple with Apsidal Sanctorum", "Lad Khan Temple", "Meguti Jain Temple Hilltop"],
        nearby=["Badami", "Pattadakal"],
        secret_eatery="Village tea stalls serving piping hot mirchi bajjis and buttermilk",
        best_time_of_day="Early morning 8:00 AM when the sculptured stone pillars cast long dramatic shadows",
        transit_tip="Just 35 km from Badami; best covered as a unified 1-day circuit with Pattadakal",
        crowd_level="Low and very peaceful"
    ),
    "Pattadakal": Destination(
        name="Pattadakal", region="North Karnataka",
        lat=15.9480, lon=75.8170,
        categories=["Heritage"],
        description="UNESCO World Heritage Site on the banks of Malaprabha River. The ceremonial coronation grounds "
                    "of the Chalukyan dynasty, representing the zenith of harmonious temple architectural fusion.",
        best_season="Oct-Mar", time_needed_hrs=2.5, entry_fee_inr=30,
        highlights=["Virupaksha Temple", "Mallikarjuna Temple", "Sangameshwara Temple"],
        nearby=["Badami", "Aihole"],
        secret_eatery="Kamat Lingayat Khanavali along Badami-Pattadakal road",
        best_time_of_day="10:00 AM to 1:00 PM for photography of intricate Ramayana narrative friezes",
        transit_tip="Midway between Badami (22 km) and Aihole (14 km)",
        crowd_level="Low to Moderate"
    ),
    "Bijapur (Vijayapura)": Destination(
        name="Bijapur (Vijayapura)", region="North Karnataka",
        lat=16.8302, lon=75.7100,
        categories=["Heritage"],
        description="The historic Adil Shahi stronghold. Features the world-famous Gol Gumbaz with the second-largest "
                    "unsupported dome on earth, and Ibrahim Rouza - the acoustic and artistic inspiration for the Taj Mahal.",
        best_season="Oct-Feb", time_needed_hrs=5, entry_fee_inr=25,
        highlights=["Gol Gumbaz Whispering Gallery", "Ibrahim Rouza", "Malik-e-Maidan Monolithic Cannon"],
        nearby=["Badami"],
        secret_eatery="Hotel Tourist Vijayapura - Famous for aromatic Dum Biryani and North Karnataka Kadak Rotti",
        best_time_of_day="9:00 AM sharp at Gol Gumbaz to experience the 11-echo Whispering Gallery before crowds arrive",
        transit_tip="Gol Gumbaz Express train connects directly from Bangalore",
        crowd_level="Moderate"
    ),

    # ── Coastal Karnataka ────────────────────────────────────────
    "Gokarna": Destination(
        name="Gokarna", region="Coastal Karnataka",
        lat=14.5479, lon=74.3188,
        categories=["Nature", "Adventure"],
        description="Sacred coastal enclave where ancient Shaivite sanctity meets five pristine crescent beaches. "
                    "Renowned for the Cliffside Beach Trek connecting Kudle, Om Beach, Half Moon, and Paradise Beach.",
        best_season="Oct-Mar", time_needed_hrs=6, entry_fee_inr=0,
        highlights=["Om Beach & Beach Trek", "Mahabaleshwar Temple Atmalinga", "Sunset at Kudle Beach"],
        nearby=["Murdeshwar", "Karwar"],
        secret_eatery="Namaste Cafe on Om Beach (fresh sea bass & coconut curry) & Prema Restaurant for homemade Nutella pie",
        best_time_of_day="4:30 PM for the cliff trek between Kudle and Om Beach to catch the Arabian Sea sunset",
        transit_tip="Konkan Railway station (Gokarna Road); KSRTC sleeper buses from Bangalore & Mangalore",
        crowd_level="Moderate on weekdays, lively on weekends"
    ),
    "Murdeshwar": Destination(
        name="Murdeshwar", region="Coastal Karnataka",
        lat=14.0946, lon=74.4873,
        categories=["Heritage", "Adventure"],
        description="Coastal sanctuary home to the world's second-tallest Shiva statue (123 ft), surrounded by three "
                    "sides of the Arabian Sea, with a 20-story Rajagopuram with an elevator to the panoramic viewing deck.",
        best_season="Oct-Mar", time_needed_hrs=3, entry_fee_inr=0,
        highlights=["Colossal 123-ft Shiva Statue", "Raja Gopura Lift Panorama", "Scuba Diving at Netrani Island"],
        nearby=["Gokarna"],
        secret_eatery="Naveen Beach Restaurant situated on a pier into the sea - Neer Dosa & Spicy Prawn Masala",
        best_time_of_day="Sunrise at 6:30 AM or late afternoon when sea breeze sweeps the temple promontory",
        transit_tip="Direct stop on Konkan Railway; just 54 km south of Gokarna along NH-66",
        crowd_level="Moderate to High during temple festivals"
    ),
    "Mangalore": Destination(
        name="Mangalore", region="Coastal Karnataka",
        lat=12.9141, lon=74.8560,
        categories=["Food", "Heritage"],
        description="Karnataka's coastal metropolis and premier gastronomic capital. Famed for red-tiled heritage homes, "
                    "the 10th-century Kadri Manjunath Temple, and legendary Ghee Roast and Kori Rotti culinary traditions.",
        best_season="Oct-May", time_needed_hrs=5, entry_fee_inr=0,
        highlights=["Mangalorean Seafood Ghee Roast", "St. Aloysius Chapel Renaissance Frescoes", "Panambur Beach Sunset"],
        nearby=["Udupi"],
        secret_eatery="Hotel Narayana (Bunder Port) for authentic Lady Fish fry & Giri Manja's for Ghee Roast",
        best_time_of_day="Evenings for food exploration and Panambur Beach walks",
        transit_tip="International Airport (IXE) with direct flights, Vande Bharat train from Bangalore",
        crowd_level="Urban, active year-round"
    ),
    "Udupi": Destination(
        name="Udupi", region="Coastal Karnataka",
        lat=13.3409, lon=74.7421,
        categories=["Food", "Heritage"],
        description="The spiritual and culinary crown jewel of Karnataka. The birthplace of pure vegetarian Udupi cuisine, "
                    "centered around the 13th-century Sri Krishna Matha where the deity is worshipped through a 9-holed silver window.",
        best_season="Oct-May", time_needed_hrs=4, entry_fee_inr=0,
        highlights=["Sri Krishna Matha & Kanakana Kindi", "St. Mary's Hexagonal Basaltic Rock Islands", "Malpe Sea Walk"],
        nearby=["Mangalore", "Murdeshwar"],
        secret_eatery="Mitra Samaj (Car Street) - The legendary 70-year-old birthplace of crispy Mangalore Buns & Goli Baje",
        best_time_of_day="7:00 AM for peaceful Matha darshan, then afternoon boat to St. Mary's Island",
        transit_tip="Only 55 km north of Mangalore along smooth 4-lane highway NH-66",
        crowd_level="High on Ekadashi & festival days, moderate normally"
    ),
    "Karwar": Destination(
        name="Karwar", region="Coastal Karnataka",
        lat=14.8025, lon=74.1240,
        categories=["Nature", "Adventure"],
        description="Where the tranquil Kali River estuary merges into the Arabian Sea, famously praised by Rabindranath Tagore. "
                    "Gateway to secluded island getaways like Devbagh and historic Sadashivgad Fort.",
        best_season="Oct-Mar", time_needed_hrs=4, entry_fee_inr=0,
        highlights=["Devbagh Island Watersports", "Tagore Beach Walk", "Sadashivgad Fort Sunset Viewpoint"],
        nearby=["Gokarna"],
        secret_eatery="Amrut Restaurant - Authentic Karwar Crab Masala and Sol Kadi",
        best_time_of_day="5:00 PM on the Kali River bridge or Sadashivgad fort for dramatic estuary sunsets",
        transit_tip="Northernmost coastal Karnataka town; just 15 km south of the Goa border",
        crowd_level="Low and unhurried"
    ),

    # ── Western Ghats / Coffee Country ───────────────────────────
    "Coorg (Kodagu)": Destination(
        name="Coorg (Kodagu)", region="Western Ghats",
        lat=12.3375, lon=75.8069,
        categories=["Nature", "Food"],
        description="The 'Scotland of India' - rolling cloud-kissed hills, private coffee and black pepper estates, "
                    "tumbling waterfalls, and the proud martial traditions and distinctive pork cuisine of the Kodava community.",
        best_season="Sep-Mar", time_needed_hrs=12, entry_fee_inr=0,
        highlights=["Abbey Falls & Raja's Seat", "Coffee & Cardamom Plantation Walk", "Namdroling Golden Temple Bylakuppe", "Kodava Pandi Curry"],
        nearby=["Nagarhole (Kabini)", "Sakleshpur"],
        secret_eatery="Taste of Coorg (Madikeri) for authentic Kodava Pandi Curry with Kadambuttu rice dumplings",
        best_time_of_day="Sunrise at Mandalpatti Peak in a 4x4 Jeep; 5:30 PM sunset at Raja's Seat",
        transit_tip="4.5 hrs scenic drive from Bangalore; KSRTC non-stop Rajahamsa buses run day & night",
        crowd_level="High on long weekends; private plantation homestays offer complete seclusion"
    ),
    "Chikmagalur": Destination(
        name="Chikmagalur", region="Western Ghats",
        lat=13.3161, lon=75.7720,
        categories=["Nature", "Adventure"],
        description="The cradle of coffee in India where Baba Budan first planted seven beans in 1670. Crowned by "
                    "Mullayanagiri, Karnataka's highest peak (1,930 m), lush tea gardens, and babbling mountain streams.",
        best_season="Sep-Feb", time_needed_hrs=8, entry_fee_inr=0,
        highlights=["Mullayanagiri Peak Trek", "Baba Budangiri Shrine", "Hebbe Falls Jeep Ride", "Fresh Estate Coffee Cupping"],
        nearby=["Belur", "Halebidu", "Sakleshpur"],
        secret_eatery="Town Canteen (Chikmagalur town) - Crispy Benne Dosa served with mild coconut chutney since 1966",
        best_time_of_day="6:00 AM summit trek at Mullayanagiri above the sea of clouds",
        transit_tip="4.5 hours from Bangalore via Hassan NH-75; roads are in excellent condition",
        crowd_level="Moderate"
    ),
    "Sakleshpur": Destination(
        name="Sakleshpur", region="Western Ghats",
        lat=12.9440, lon=75.7847,
        categories=["Nature", "Adventure"],
        description="Charming misty hill station renowned for star-shaped 18th-century Manjarabad Fort, untouched spice "
                    "valleys, and the majestic Bisle Reserve Forest offering a viewpoint of three mountain ranges.",
        best_season="Sep-Feb", time_needed_hrs=6, entry_fee_inr=0,
        highlights=["Manjarabad Star Fort", "Bisle Ghat Beauty Viewpoint", "Green Route Railway Trek Views"],
        nearby=["Chikmagalur", "Belur"],
        secret_eatery="Surabhi Hotel on bypass - Malnad-style Akki Rotti with spicy chicken or raw jackfruit curry",
        best_time_of_day="7:00 AM at Bisle Viewpoint before thick valley mist rolls over the peaks",
        transit_tip="Direct train from Bangalore to Sakleshpur passes through lush Hassan plains",
        crowd_level="Low to Moderate"
    ),
    "Kudremukh": Destination(
        name="Kudremukh", region="Western Ghats",
        lat=13.2500, lon=75.2500,
        categories=["Nature", "Adventure"],
        description="A UNESCO-listed biodiversity hotspot shaped like a horse's face. Endless emerald shola grasslands, "
                    "crystal streams, and a protected national park home to lion-tailed macaques and leopards.",
        best_season="Oct-May", time_needed_hrs=8, entry_fee_inr=100,
        highlights=["Kudremukh Peak Trek (1,894 m)", "Rolling Shola Grasslands", "Hanuman Gundi Falls"],
        nearby=["Chikmagalur", "Udupi"],
        secret_eatery="Local homestays in Kalasa serving authentic Malnad jackfruit pappad & kashaya herbal brew",
        best_time_of_day="6:00 AM forest department entry gate - permits are strictly capped at 50 trekkers per day!",
        transit_tip="Trek bookings MUST be reserved online through Karnataka Eco-Tourism portal",
        crowd_level="Regulated and pristine"
    ),

    # ── Heritage Temple Towns ────────────────────────────────────
    "Belur": Destination(
        name="Belur", region="Hassan Region",
        lat=13.1631, lon=75.8615,
        categories=["Heritage"],
        description="The sublime 12th-century Chennakeshava Temple, chiseled from soft soapstone over 103 years. "
                    "Famed for 48 Darpana Sundari (bracket figures) captured in dynamic classical dance postures.",
        best_season="Year-round", time_needed_hrs=2.5, entry_fee_inr=25,
        highlights=["Chennakeshava Masterpiece", "Madanika Bracket Figures", "Gravity-Defying Lamp Pillar"],
        nearby=["Halebidu", "Chikmagalur", "Shravanabelagola"],
        secret_eatery="Vishnu Kripa - Traditional Hassan Ragi Mudde with hot Bassaru",
        best_time_of_day="Morning 8:30-11:00 AM for gentle sunlight illuminating the external relief carvings",
        transit_tip="Just 16 km from Halebidu; 38 km from Hassan railway junction",
        crowd_level="Moderate on weekends"
    ),
    "Halebidu": Destination(
        name="Halebidu", region="Hassan Region",
        lat=13.2133, lon=75.9933,
        categories=["Heritage"],
        description="The regal capital of the Hoysala Empire. The Hoysaleshwara Temple boasts an astonishing unbroken "
                    "frieze of over 12,000 intricately carved soapstone sculptures where no two animals or figures are identical.",
        best_season="Year-round", time_needed_hrs=2, entry_fee_inr=25,
        highlights=["Hoysaleshwara Twin Shrines", "12,000 Micro-Sculptures", "Monolithic Nandi Mantapa"],
        nearby=["Belur", "Shravanabelagola"],
        secret_eatery="Mayura Shantala (KSTDC restaurant located right in the temple garden grounds)",
        best_time_of_day="3:30-5:30 PM when the lower soapstone animal friezes catch direct golden evening rays",
        transit_tip="Combine seamlessly with Belur in a single morning-afternoon excursion",
        crowd_level="Moderate"
    ),
    "Shravanabelagola": Destination(
        name="Shravanabelagola", region="Hassan Region",
        lat=12.8585, lon=76.4866,
        categories=["Heritage"],
        description="One of the ancient world's grandest pilgrimage shrines. Perched atop Vindhyagiri Hill stands the "
                    "57-foot monolithic statue of Lord Gommateshwara (Bahubali), carved out of a single rock in 981 CE.",
        best_season="Year-round", time_needed_hrs=3, entry_fee_inr=0,
        highlights=["57-ft Bahubali Monolith", "650 Stone Steps of Vindhyagiri", "Chandragiri Jain Inscriptions"],
        nearby=["Belur", "Halebidu"],
        secret_eatery="Gomatheswara Pure Veg Bhojanalaya - Satvik Jain Karnataka thali",
        best_time_of_day="6:30 AM barefoot ascent up the granite steps before the rock absorbs solar heat",
        transit_tip="Located directly along the Bangalore-Hassan NH-75 highway (140 km from Bangalore)",
        crowd_level="Moderate; serene in early morning"
    ),

    # ── Wildlife / National Parks ────────────────────────────────
    "Bandipur National Park": Destination(
        name="Bandipur National Park", region="Mysore Region",
        lat=11.6688, lon=76.6337,
        categories=["Nature", "Adventure"],
        description="Premier Project Tiger reserve nestled in the Nilgiri Biosphere foothills. Dense dry deciduous "
                    "forests teeming with Bengal tigers, wild elephants, Indian leopards, and Asiatic wild dogs.",
        best_season="Oct-May", time_needed_hrs=6, entry_fee_inr=300,
        highlights=["Open-top Jeep Jungle Safari", "Tiger & Leopard Tracking", "Wild Elephant Herds"],
        nearby=["Mysore Palace", "Nagarhole (Kabini)"],
        secret_eatery="Jungle Lodges Bandipur Safari Lodge buffet featuring local country chicken and ragi rotis",
        best_time_of_day="Dawn safari (6:15 AM) or dusk safari (4:00 PM) for maximum predator sightings",
        transit_tip="80 km south of Mysore on the Ooty highway (NH-766); night traffic strictly banned 9 PM-6 AM",
        crowd_level="Regulated; online safari booking is mandatory to secure seats"
    ),
    "Nagarhole (Kabini)": Destination(
        name="Nagarhole (Kabini)", region="Mysore Region",
        lat=12.0569, lon=76.1510,
        categories=["Nature", "Adventure"],
        description="Celebrated worldwide for India's best leopard and black panther sightings. The Kabini river reservoir "
                    "draws the largest summer congregation of Asian elephants in the world along its lush banks.",
        best_season="Oct-May", time_needed_hrs=6, entry_fee_inr=300,
        highlights=["Kabini River Coracle/Boat Safari", "Black Panther & Tiger Sightings", "Huge Elephant Congregations"],
        nearby=["Coorg (Kodagu)", "Bandipur National Park"],
        secret_eatery="Kabini River Lodge colonial veranda dining over the water",
        best_time_of_day="3:30 PM boat safari along the river banks when elephants arrive for their evening bath",
        transit_tip="90 km southwest of Mysore; private taxi or resort vehicle recommended",
        crowd_level="Controlled and peaceful"
    ),
    "Dandeli": Destination(
        name="Dandeli", region="North Karnataka",
        lat=15.2633, lon=74.6239,
        categories=["Adventure", "Nature"],
        description="The white-water adventure capital of South India. The roaring Kali River provides Grade-3 rapids, "
                    "surrounded by dense teak forests, hornbill sanctuaries, and prehistoric volcanic Syntheri Rocks.",
        best_season="Oct-May", time_needed_hrs=8, entry_fee_inr=50,
        highlights=["Grade 3 White-Water Rafting", "Kali River Kayaking & Coracle Rides", "Syntheri Rocks Giant Monolith", "Hornbill Spotting"],
        nearby=["Karwar"],
        secret_eatery="River-camp riverside barbecue with spicy North Karnataka Dharwad-style masalas",
        best_time_of_day="9:00 AM for water release from Supa Dam for prime river rafting rapids",
        transit_tip="75 km from Hubli / Dharwad rail stations; buses connect via Alnavar",
        crowd_level="Lively during holiday seasons"
    ),

    # ── Bangalore Region ─────────────────────────────────────────
    "Bangalore": Destination(
        name="Bangalore", region="Bangalore Region",
        lat=12.9716, lon=77.5946,
        categories=["Food", "Heritage"],
        description="The Garden City turned global tech titan. A dynamic metropolis blending 16th-century Kempe Gowda "
                    "fortresses, Lalbagh botanical glasshouse, iconic darshinis, and over 65 artisanal craft microbreweries.",
        best_season="Year-round", time_needed_hrs=8, entry_fee_inr=0,
        highlights=["VV Puram Street Food Trail", "Lalbagh Botanical Gardens & Glass House", "Bangalore Palace Tudor Estate", "Craft Beer Hubs"],
        nearby=["Nandi Hills"],
        secret_eatery="Vidyarthi Bhavan (Gandhi Bazaar, est. 1943) & Bramhins Coffee Bar (Shankarapuram)",
        best_time_of_day="7:00 AM for Lalbagh morning walk, 7:00 PM for VV Puram Food Street feast",
        transit_tip="Namma Metro Purple & Green lines connect major city hubs seamlessly",
        crowd_level="Metropolitan bustle"
    ),
    "Nandi Hills": Destination(
        name="Nandi Hills", region="Bangalore Region",
        lat=13.3702, lon=77.6835,
        categories=["Nature", "Adventure"],
        description="Ancient hilltop fortress situated at 1,478 meters altitude. Famed for mesmerizing cloud-inversion sunrises, "
                    "Tipu Sultan's summer retreat, ancient yoga temples, and tandem paragliding launches.",
        best_season="Sep-Feb", time_needed_hrs=4, entry_fee_inr=20,
        highlights=["Cloud Inversion Sunrise View", "Tipu's Drop", "Tandem Paragliding", "Yoga Nandeeshwara Temple"],
        nearby=["Bangalore"],
        secret_eatery="Indian Paratha Company on Hyderabad highway or KSTDC Mayura restaurant hilltop",
        best_time_of_day="5:00 AM arrival to beat the barrier gate rush and catch the mystical sea of clouds at dawn",
        transit_tip="60 km from central Bangalore, only 35 km from Kempegowda International Airport",
        crowd_level="Very high on weekend mornings; serene on weekdays"
    ),

    # ── Waterfalls ───────────────────────────────────────────────
    "Jog Falls": Destination(
        name="Jog Falls", region="Coastal Karnataka",
        lat=14.2295, lon=74.8127,
        categories=["Nature"],
        description="India's second-highest untiered plunge waterfall (253 m). The Sharavathi River thunders over the chasm "
                    "in four dramatic cascades aptly named Raja, Rani, Rover, and Rocket.",
        best_season="Aug-Dec", time_needed_hrs=3, entry_fee_inr=0,
        highlights=["Raja Fall 253-meter Plunge", "1,400 Stone Steps to the Chasm Base", "Illuminated Evening Falls"],
        nearby=["Murdeshwar", "Gokarna"],
        secret_eatery="Hotel Mayura Gerusoppa (KSTDC) - Malnad style fish and piping hot rasam",
        best_time_of_day="10:00 AM when morning mist clears to reveal the full majesty of all 4 cascades",
        transit_tip="Talguppa is nearest railway station (14 km); KSRTC connects from Shimoga and Sagar",
        crowd_level="High during monsoon peak (Aug-Oct), peaceful in winter"
    ),

    # ── North Karnataka Food Hubs ────────────────────────────────
    "Dharwad": Destination(
        name="Dharwad", region="North Karnataka",
        lat=15.4589, lon=75.0078,
        categories=["Food", "Heritage"],
        description="The cultural soul of North Karnataka and classical music capital. Celebrated for its unique GI-tagged "
                    "Dharwad Pedha, rich literary tradition, and wholesome Jolada Rotti Khanavalis.",
        best_season="Year-round", time_needed_hrs=3, entry_fee_inr=0,
        highlights=["Line Bazaar Dharwad Pedha", "Karnatak University Heritage Campus", "Lingayat Khanavali Feast"],
        nearby=["Badami", "Dandeli"],
        secret_eatery="Babusingh Thakur Pedha (Line Bazaar) - The 175-year-old original creator of Dharwad Pedha",
        best_time_of_day="11:30 AM to catch freshly made hot batches of pedha right off the traditional wood-fired stoves",
        transit_tip="Twin-city Hubli-Dharwad has its own airport (HBX) and major railway junction",
        crowd_level="Moderate"
    ),
    "Davangere": Destination(
        name="Davangere", region="North Karnataka",
        lat=14.4644, lon=75.9218,
        categories=["Food"],
        description="The undisputed Benne (Butter) Dosa capital of Karnataka. A bustling textile and food hub situated along "
                    "the Tungabhadra basin, serving crisp dosas topped with fresh white home-churned butter.",
        best_season="Year-round", time_needed_hrs=2, entry_fee_inr=0,
        highlights=["Davangere Benne Masala Dosa", "Spicy Potato Palya & Coconut Chutney", "Kalleshwara Temple"],
        nearby=["Hampi"],
        secret_eatery="Ravi Benne Dosa Hotel (Church Rd) & Sri Guru Kottureshwara Butter Dosa Hotel",
        best_time_of_day="Evening 5:30 PM to watch master cooks prepare 30 butter dosas simultaneously on giant cast-iron tawas",
        transit_tip="Directly on National Highway 48 midway between Bangalore and Hubli; perfect food pitstop",
        crowd_level="High at dinner hour; rapid turnover"
    ),
}
# fmt: on


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CURATED POPULAR CIRCUITS (1-Click Itinerary Launchers)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CURATED_CIRCUITS: Dict[str, Dict[str, any]] = {
    "👑 Royal Wadiyar Heritage": {
        "title": "Royal Mysore & Hoysala Stone Lace Trail",
        "tagline": "Golden thrones, island forts & 900-year-old carved temples",
        "description": "Walk through Mysore's opulent halls, Tipu Sultan's island fortress in Srirangapatna, and the micro-carved soapstone marvels of Belur & Halebidu.",
        "interests": ["Heritage", "Food"],
        "budget": "Mid-range",
        "days": 3,
        "travelers": 2,
        "companions": "Couple",
        "badge": "Most Popular",
        "stops": ["Mysore Palace", "Chamundi Hills", "Srirangapatna", "Belur", "Halebidu"],
        "highlight_dish": "Original Mysore Pak & Mylari Butter Dosa",
        "image_url": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?auto=format&fit=crop&w=800&q=80",
    },
    "☕ Misty Ghats & Coffee Trails": {
        "title": "Western Ghats Cloud & Aroma Trail",
        "tagline": "Cloud inversions, shola grasslands & estate-fresh filter coffee",
        "description": "Trek the cloud-capped summit of Mullayanagiri, wake up to misty coffee plantations in Chikmagalur, and experience warrior heritage and pandi curry in Coorg.",
        "interests": ["Nature", "Food", "Adventure"],
        "budget": "Mid-range",
        "days": 4,
        "travelers": 2,
        "companions": "Friends Group",
        "badge": "Scenic Favorite",
        "stops": ["Chikmagalur", "Coorg (Kodagu)", "Sakleshpur", "Kudremukh"],
        "highlight_dish": "Kodava Pandi Curry & Estate Filter Coffee",
        "image_url": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=650&q=80",
    },
    "🌊 Coastal Sunset & Spiritual Sands": {
        "title": "Karavali Coast & Temple Odyssey",
        "tagline": "Crescent beach treks, ocean deities & coastal seafood feasts",
        "description": "Trek Gokarna's pristine sea cliffs, gaze upon Murdeshwar's colossal 123-ft Shiva statue, and feast on world-famous Udupi and Mangalorean delicacies.",
        "interests": ["Nature", "Food", "Adventure"],
        "budget": "Mid-range",
        "days": 4,
        "travelers": 2,
        "companions": "Friends Group",
        "badge": "Adventure & Food",
        "stops": ["Gokarna", "Murdeshwar", "Udupi", "Mangalore"],
        "highlight_dish": "Mangalorean Fish Ghee Roast & Udupi Neer Dosa",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=650&q=80",
    },
    "🏛️ UNESCO Stone Empires": {
        "title": "Vijayanagara & Chalukyan Odyssey",
        "tagline": "Boulder kingdoms, 6th-century caves & whispering domes",
        "description": "Explore Hampi's surreal boulder terrain and stone chariot, marvel at Badami's rock-cut cliff temples, and whisper inside the world's second-largest dome at Bijapur.",
        "interests": ["Heritage"],
        "budget": "Budget",
        "days": 4,
        "travelers": 2,
        "companions": "Friends Group",
        "badge": "UNESCO Circuit",
        "stops": ["Hampi", "Badami", "Pattadakal", "Aihole", "Bijapur (Vijayapura)"],
        "highlight_dish": "Jolada Rotti Meals with Shengachutney & Dharwad Pedha",
        "image_url": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=650&q=80",
    },
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2.  BUDGET COST ENGINE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Daily cost estimates per person (INR) by budget tier
BUDGET_PROFILES: Dict[str, Dict[str, Tuple[int, int]]] = {
    "Budget": {
        "accommodation":  (500,  1200),
        "food":           (300,   600),
        "transport":      (200,   500),
        "activities":     (100,   400),
        "miscellaneous":  (100,   300),
    },
    "Mid-range": {
        "accommodation":  (2000,  4500),
        "food":           (600,  1200),
        "transport":      (500,  1200),
        "activities":     (300,   800),
        "miscellaneous":  (200,   500),
    },
    "Luxury": {
        "accommodation":  (6000, 15000),
        "food":           (1500,  3500),
        "transport":      (1500,  4000),
        "activities":     (800,  2000),
        "miscellaneous":  (500,  1500),
    },
}


def compute_daily_budget(tier: str, num_travelers: int = 1) -> pd.DataFrame:
    """
    Returns a DataFrame with expected daily costs for the given budget tier.
    Columns: category, min_cost, max_cost, avg_cost (per person × travelers).
    """
    profile = BUDGET_PROFILES.get(tier, BUDGET_PROFILES["Mid-range"])
    rows = []
    for cat, (lo, hi) in profile.items():
        rows.append({
            "category":   cat.title(),
            "min_cost":   lo * num_travelers,
            "max_cost":   hi * num_travelers,
            "avg_cost":   int(((lo + hi) / 2) * num_travelers),
        })
    return pd.DataFrame(rows)


def compute_trip_budget(
    tier: str,
    days: int,
    num_travelers: int = 1,
) -> Dict[str, any]:
    """
    Aggregate budget breakdown for the entire trip.
    Returns dict with 'daily' DataFrame, 'total_min', 'total_max', 'total_avg'.
    """
    daily = compute_daily_budget(tier, num_travelers)
    total_min = daily["min_cost"].sum() * days
    total_max = daily["max_cost"].sum() * days
    total_avg = daily["avg_cost"].sum() * days
    return {
        "daily":     daily,
        "total_min": int(total_min),
        "total_max": int(total_max),
        "total_avg": int(total_avg),
        "days":      days,
        "tier":      tier,
        "travelers": num_travelers,
    }


def budget_saving_tips(tier: str) -> List[str]:
    """Context-aware budget tips based on the chosen tier."""
    tips = {
        "Budget": [
            "🚌 Use KSRTC state buses - reliable and incredibly affordable across Karnataka.",
            "🏠 Stay in KSTDC government guesthouses or dharamshalas near temples.",
            "🍽️ Eat at local *darshinis* (stand-and-eat joints) for meals under ₹80.",
            "🎟️ Many heritage sites offer combined tickets - ask at the counter!",
            "🚂 Book trains via IRCTC at least 30 days ahead for lowest fares.",
        ],
        "Mid-range": [
            "🏨 Heritage homestays in Coorg & Chikmagalur offer better value than hotels.",
            "🚗 Rent a self-drive car via Zoomcar for flexible multi-city travel.",
            "🍛 Mix high-end restaurants with local eateries to balance budget and experience.",
            "📱 Use Rapido/Ola Auto for short hops instead of taxis.",
            "🎫 Pre-book safari slots online - walk-in prices can be 40% higher.",
        ],
        "Luxury": [
            "🏰 Book Jungle Lodges & Resorts (govt.) for premium wildlife stays at fair prices.",
            "✈️ Fly to Hubli/Mangalore to save highway driving time to North/Coastal Karnataka.",
            "🍷 Premium Bangalore craft brewery tours offer excellent value tasting experiences.",
            "🚁 Helicopter joyrides at Jakkur offer stunning aerial views of Bangalore.",
            "🎭 Private guided heritage walks in Hampi provide unmatched depth over audio guides.",
        ],
    }
    return tips.get(tier, tips["Mid-range"])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3.  DESTINATION FILTER & SEARCH UTILITIES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def filter_destinations(
    interests: List[str],
    max_results: int = 15,
) -> List[Destination]:
    """
    Return destinations matching at least one of the supplied interest
    categories, ranked by number of category overlaps (most relevant first).
    """
    scored: List[Tuple[int, Destination]] = []
    for dest in KARNATAKA_DESTINATIONS.values():
        overlap = len(set(dest.categories) & set(interests))
        if overlap > 0:
            scored.append((overlap, dest))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:max_results]]


def get_destinations_by_region(region: str) -> List[Destination]:
    """Return all destinations in a given region."""
    return [d for d in KARNATAKA_DESTINATIONS.values() if d.region == region]


def get_all_regions() -> List[str]:
    """Return sorted list of unique regions."""
    return sorted({d.region for d in KARNATAKA_DESTINATIONS.values()})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4.  STREAMLIT SESSION-STATE HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def init_session_state() -> None:
    """Initialise all session-state keys with safe defaults."""
    defaults = {
        "itinerary":          None,       # generated itinerary dict
        "selected_dest":      None,       # currently focused destination name
        "budget_data":        None,       # budget breakdown dict
        "trip_prefs":         {},         # user preference snapshot
        "generation_done":    False,      # flag: itinerary generated
        "tutorial_completed": False,      # gatekeeper: show onboarding tutorial before app starts
        "main_nav_bar":       "explore",  # canonical top website navigation selector
        "app_lang":           "English",  # active application UI language
        "tourist_lang":       "English",  # tourist mother tongue for translation & guidance
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def reset_session_state() -> None:
    """Clear generated content (keeps preferences and tutorial status)."""
    st.session_state["itinerary"]       = None
    st.session_state["budget_data"]     = None
    st.session_state["generation_done"] = False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5.  DESTINATION IMAGES & PHOTOGRAPHY DATABASE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DESTINATION_IMAGES: Dict[str, str] = {
    "Mysore Palace": "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?auto=format&fit=crop&w=800&q=80",
    "Chamundi Hills": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Brindavan Gardens": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?auto=format&fit=crop&w=800&q=80",
    "Srirangapatna": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Hampi": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Badami": "https://images.unsplash.com/photo-1628155930542-3c7a64e2c833?auto=format&fit=crop&w=800&q=80",
    "Aihole": "https://images.unsplash.com/photo-1628155930542-3c7a64e2c833?auto=format&fit=crop&w=800&q=80",
    "Pattadakal": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Bijapur (Vijayapura)": "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80",
    "Coorg (Kodagu)": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80",
    "Chikmagalur": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80",
    "Sakleshpur": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "Kudremukh": "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=800&q=80",
    "Gokarna": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
    "Murdeshwar": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Udupi": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=800&q=80",
    "Mangalore": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=800&q=80",
    "Karwar": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
    "Belur": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Halebidu": "https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=800&q=80",
    "Shravanabelagola": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80",
    "Bandipur National Park": "https://images.unsplash.com/photo-1575550959106-5a7defe28b56?auto=format&fit=crop&w=800&q=80",
    "Nagarhole (Kabini)": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?auto=format&fit=crop&w=800&q=80",
    "Dandeli": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80",
    "Bangalore": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80",
    "Nandi Hills": "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80",
    "Jog Falls": "https://images.unsplash.com/photo-1546182990-dffeafbe841d?auto=format&fit=crop&w=800&q=80",
    "Dharwad": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80",
    "Davangere": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?auto=format&fit=crop&w=800&q=80",
}


def get_destination_image(name: str) -> str:
    """Return high-resolution photo URL for a Karnataka destination with smart keyword matching."""
    if not name:
        return DESTINATION_IMAGES["Mysore Palace"]

    # 1. Exact match
    if name in DESTINATION_IMAGES:
        return DESTINATION_IMAGES[name]

    # 2. Substring & keyword match across known destinations
    name_lower = name.lower()
    for dest_key, img_url in DESTINATION_IMAGES.items():
        clean_key = dest_key.split("(")[0].strip().lower()
        if clean_key in name_lower or name_lower in clean_key:
            return img_url

    # 3. Category & regional keyword fallbacks
    if any(w in name_lower for w in ["temple", "heritage", "palace", "fort", "monument", "stone", "ruin"]):
        return DESTINATION_IMAGES["Hampi"]
    if any(w in name_lower for w in ["falls", "waterfall", "river", "lake", "dam"]):
        return DESTINATION_IMAGES["Jog Falls"]
    if any(w in name_lower for w in ["beach", "sea", "coast", "cliff", "ocean"]):
        return DESTINATION_IMAGES["Gokarna"]
    if any(w in name_lower for w in ["hill", "peak", "ghat", "coffee", "estate", "trek"]):
        return DESTINATION_IMAGES["Chikmagalur"]
    if any(w in name_lower for w in ["safari", "tiger", "jungle", "wildlife", "forest"]):
        return DESTINATION_IMAGES["Bandipur National Park"]
    if any(w in name_lower for w in ["food", "dosa", "hotel", "cafe", "market", "eatery", "darshini"]):
        return DESTINATION_IMAGES["Davangere"]

    # 4. Reliable default
    return DESTINATION_IMAGES.get(
        "Mysore Palace",
        "https://images.unsplash.com/photo-1609766857041-ed402ea8069a?auto=format&fit=crop&w=800&q=80"
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GANDABERUNDA ROYAL HERITAGE EMBLEM & SEAL (OFFICIAL KARNATAKA EMBLEM)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GANDABERUNDA_SEAL_SVG = """<svg width="34" height="34" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align:middle; filter:drop-shadow(0 2px 5px rgba(0,0,0,0.35)); flex-shrink:0;">
  <!-- Royal Rim -->
  <circle cx="60" cy="60" r="57" fill="#88131B" stroke="#F59E0B" stroke-width="4"/>
  <circle cx="60" cy="60" r="51" fill="none" stroke="#FEF3C7" stroke-width="1.5" stroke-dasharray="3 3"/>
  <circle cx="60" cy="60" r="47" fill="#700B13"/>
  <!-- Gandaberunda Double-Headed Mythological Bird -->
  <path d="M60 40 C56 28 44 26 39 33 C32 42 39 56 50 58 C37 58 25 48 16 60 C27 65 41 64 51 61 C43 69 29 76 18 78 C31 82 45 76 54 69 C53 78 46 88 38 97 C53 94 60 81 60 74 C60 81 67 94 82 97 C74 88 67 78 66 69 C75 76 89 82 102 78 C91 76 77 69 69 61 C79 64 93 65 104 60 C95 48 83 58 70 58 C81 56 88 42 81 33 C76 26 64 28 60 40 Z" fill="#FBBF24"/>
  <!-- Royal Crowns & Golden Beaks -->
  <polygon points="41,20 46,28 37,28" fill="#FDE68A"/>
  <polygon points="79,20 74,28 83,28" fill="#FDE68A"/>
  <polygon points="60,16 56,26 64,26" fill="#FDE68A"/>
  <circle cx="60" cy="52" r="5" fill="#DC2626" stroke="#FEF3C7" stroke-width="1.5"/>
</svg>"""

GANDABERUNDA_HERITAGE_BADGE_HTML = f"""<div style="background:linear-gradient(135deg, rgba(136,19,27,0.85) 0%, rgba(185,28,28,0.85) 100%); border:1.5px solid #F59E0B; border-radius:24px; padding:0.35rem 0.9rem; font-size:0.78rem; font-weight:800; color:#FFFFFF !important; display:inline-flex; align-items:center; gap:8px; box-shadow:0 3px 10px rgba(0,0,0,0.25);">
{GANDABERUNDA_SEAL_SVG}
<div style="text-align:left; line-height:1.2;">
  <span style="color:#FEF3C7; font-size:0.68rem; text-transform:uppercase; letter-spacing:0.5px; display:block;">ಕರ್ನಾಟಕ ರಾಜ ಮುದ್ರೆ</span>
  <span style="color:#FFFFFF; font-weight:800; font-size:0.82rem;">Gandaberunda Royal Seal</span>
</div>
</div>"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6.  UI STYLING & ASSET HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600;1,700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Noto+Sans+Kannada:wght@400;600;700&display=swap');

    /* ── Hide the default Streamlit sidebar for clean top-nav website look ── */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* ── Karnataka Heritage Gradient Canvas with Warm Ambient Aura ───────── */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stToolbar"] {
        background: 
            radial-gradient(circle at 8% 8%, rgba(254, 243, 199, 0.75) 0%, transparent 40%),
            radial-gradient(circle at 92% 14%, rgba(254, 226, 226, 0.6) 0%, transparent 38%),
            radial-gradient(circle at 50% 92%, rgba(254, 243, 199, 0.5) 0%, transparent 45%),
            #FAF8F5 !important;
        color: #111827 !important;
        font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }

    /* ── High-Def Karnataka Cultural Watermark (Gandaberunda + Hampi Chariot + Hoysala Lotus) ── */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        pointer-events: none;
        z-index: 0;
        opacity: 0.08;
        background-image: url("data:image/svg+xml,%3Csvg width='320' height='320' viewBox='0 0 320 320' xmlns='http://www.w3.org/2000/svg'%3E%3C!-- Mysore Crimson Gandaberunda & Palace Arches --%3E%3Cg fill='%2388131B' fill-opacity='1'%3E%3Cpath d='M160 170 C150 155 130 150 120 160 C110 170 115 190 130 195 C110 195 95 180 85 200 C100 205 120 205 135 202 C125 215 105 225 90 230 C110 235 130 225 145 215 C145 230 135 245 125 260 C145 255 155 235 160 225 C165 235 175 255 195 260 C185 245 175 230 175 215 C190 225 210 235 230 230 C215 225 195 215 185 202 C200 205 220 205 235 200 C225 180 210 195 190 195 C205 190 210 170 200 160 C190 150 170 155 160 170 Z M142 155 C140 145 147 135 152 138 C147 142 145 148 142 155 Z M178 155 C180 145 173 135 168 138 C173 142 175 148 178 155 Z'/%3E%3Cpath d='M70 145 C70 125 90 115 90 115 C90 115 110 125 110 145 Z'/%3E%3Cpath d='M210 145 C210 125 230 115 230 115 C230 115 250 125 250 145 Z'/%3E%3C/g%3E%3C!-- Golden Amber Hampi Stone Chariot --%3E%3Cg fill='%23D97706' fill-opacity='1'%3E%3Cpath d='M230 35 L255 35 L260 55 L275 55 L275 75 L210 75 L210 55 L225 55 Z M217 75 A11 11 0 1 0 239 75 Z M248 75 A11 11 0 1 0 270 75 Z M235 20 L250 20 L247 35 L238 35 Z'/%3E%3C/g%3E%3C!-- Sandalwood Gold Hoysala 8-pointed Star Lotus --%3E%3Cg fill='%23B45309' fill-opacity='1'%3E%3Cpath d='M80 30 L88 48 L108 48 L92 60 L98 80 L80 68 L62 80 L68 60 L52 48 L72 48 Z'/%3E%3Ccircle cx='80' cy='55' r='5'/%3E%3Ccircle cx='30' cy='30' r='9'/%3E%3Ccircle cx='290' cy='30' r='9'/%3E%3Ccircle cx='30' cy='290' r='9'/%3E%3Ccircle cx='290' cy='290' r='9'/%3E%3C/g%3E%3C/svg%3E");
        background-repeat: repeat;
        background-size: 260px 260px;
    }

    /* ── Deep, Crisp Text Contrast Rules (Overrides OS/Browser Dark Mode) ── */
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stMarkdownContainer"] li,
    .stApp p, .stApp li,
    .stMarkdown,
    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stRadio"] label,
    [data-testid="stRadio"] div,
    [data-testid="stSelectbox"] label,
    [data-testid="stMultiSelect"] label,
    [data-testid="stSlider"] label,
    [data-testid="stNumberInput"] label {
        color: #111827 !important;
        font-weight: 500;
    }

    /* Exclude Buttons from dark text rules! */
    .stButton button p,
    .stButton button span,
    .stButton button div,
    button p, button span, button div,
    .day-header, .day-header *,
    .hero-banner *,
    .step-number, .step-number * {
        color: #FFFFFF !important;
    }

    /* Headings in Deep Royal Crimson (except inside Hero Banner) */
    [data-testid="stMarkdownContainer"] h1:not(.hero-banner h1),
    [data-testid="stMarkdownContainer"] h2:not(.hero-banner h2),
    [data-testid="stMarkdownContainer"] h3:not(.hero-banner h3),
    [data-testid="stMarkdownContainer"] h4:not(.hero-banner h4),
    .stApp h1, .stApp h2, .stApp h3, .stApp h4 {
        color: #88131B !important;
        font-weight: 800 !important;
        letter-spacing: -0.3px;
    }

    /* Hero Banner High-Contrast Pure White Overrides */
    .hero-banner,
    .hero-banner *,
    .hero-banner h1,
    .hero-banner h2,
    .hero-banner h3,
    .hero-banner p,
    .hero-banner span,
    .hero-banner div,
    [data-testid="stMarkdownContainer"] .hero-banner *,
    [data-testid="stMarkdownContainer"] .hero-banner h1,
    [data-testid="stMarkdownContainer"] .hero-banner h2,
    [data-testid="stMarkdownContainer"] .hero-banner p,
    [data-testid="stMarkdownContainer"] .hero-banner span,
    [data-testid="stMarkdownContainer"] .hero-banner div {
        color: #FFFFFF !important;
    }
    .hero-banner .subtitle,
    [data-testid="stMarkdownContainer"] .hero-banner .subtitle {
        color: #FEF3C7 !important;
    }
    .hero-banner pre, .hero-banner code,
    [data-testid="stMarkdownContainer"] .hero-banner pre,
    [data-testid="stMarkdownContainer"] .hero-banner code {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
        color: #FFFFFF !important;
        font-family: inherit !important;
        display: contents !important;
    }

    /* Subtitles and Captions */
    [data-testid="stCaptionContainer"] p, .stCaption, caption {
        color: #4B5563 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* Streamlit Tabs Navigation Bar */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 0.6rem 1rem !important;
    }
    button[data-baseweb="tab"] div,
    button[data-baseweb="tab"] p,
    button[data-baseweb="tab"] span {
        color: #374151 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] div,
    button[data-baseweb="tab"][aria-selected="true"] p,
    button[data-baseweb="tab"][aria-selected="true"] span {
        color: #88131B !important;
        font-weight: 800 !important;
    }

    /* Modern Website Segmented Control Top Navbar */
    [data-testid="stSegmentedControl"] {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: flex-start !important;
        background: #FFFFFF !important;
        padding: 6px 10px !important;
        border-radius: 16px !important;
        border: 1.5px solid #F3F4F6 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06) !important;
        gap: 6px !important;
        margin-bottom: 1.4rem !important;
    }
    [data-testid="stSegmentedControl"] button {
        border-radius: 12px !important;
        border: 1px solid #E5E7EB !important;
        padding: 0.55rem 1.15rem !important;
        background: #F9FAFB !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
    }
    [data-testid="stSegmentedControl"] button:hover {
        background: #FEF3C7 !important;
        border-color: #FDE68A !important;
        transform: translateY(-1px) !important;
    }
    .stApp [data-testid="stSegmentedControl"] button p,
    .stApp [data-testid="stSegmentedControl"] button span,
    .stApp [data-testid="stSegmentedControl"] button div {
        color: #374151 !important;
        font-weight: 700 !important;
        font-size: 0.92rem !important;
    }
    /* Active Pill with Royal Crimson & Amber Highlight */
    [data-testid="stSegmentedControl"] button[aria-checked="true"],
    [data-testid="stSegmentedControl"] button[data-checked="true"] {
        background: linear-gradient(135deg, #88131B 0%, #B91C1C 100%) !important;
        border: 1px solid #7F1D1D !important;
        box-shadow: 0 4px 14px rgba(136, 19, 27, 0.3) !important;
    }
    .stApp [data-testid="stSegmentedControl"] button[aria-checked="true"] p,
    .stApp [data-testid="stSegmentedControl"] button[aria-checked="true"] span,
    .stApp [data-testid="stSegmentedControl"] button[aria-checked="true"] div,
    .stApp [data-testid="stSegmentedControl"] button[data-checked="true"] p,
    .stApp [data-testid="stSegmentedControl"] button[data-checked="true"] span,
    .stApp [data-testid="stSegmentedControl"] button[data-checked="true"] div {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* Streamlit Inputs, Dropdowns, Selectboxes */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        border: 1.5px solid #D1D5DB !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] * {
        color: #111827 !important;
    }
    /* Multi-select filter chips */
    [data-baseweb="tag"] {
        background-color: #FEF3C7 !important;
        color: #92400E !important;
        border: 1px solid #FDE68A !important;
        border-radius: 20px !important;
    }
    [data-baseweb="tag"] * {
        color: #92400E !important;
        font-weight: 700 !important;
    }

    /* Metric elements */
    [data-testid="stMetricValue"] {
        color: #88131B !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #374151 !important;
        font-weight: 700 !important;
    }

    /* Expander elements */
    [data-testid="stExpander"] {
        background: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 12px !important;
    }
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary p {
        color: #111827 !important;
        font-weight: 700 !important;
    }

    /* ── Main Container ────────────────────────────── */
    .main .block-container {
        padding-top: 1.2rem;
        padding-bottom: 3.5rem;
        max-width: 1240px;
        position: relative;
        z-index: 1;
    }

    /* ── Top Website Navigation Header ──────────────── */
    .top-navbar {
        background: #ffffff;
        border: 1.5px solid #E5E7EB;
        border-radius: 16px;
        padding: 0.9rem 1.6rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.04);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.8rem;
    }
    .top-navbar .brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .top-navbar .brand-title {
        font-size: 1.45rem;
        font-weight: 800;
        color: #88131B !important;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .top-navbar .brand-subtitle {
        font-size: 0.82rem;
        color: #4B5563 !important;
        font-weight: 600;
        margin-top: 2px;
    }

    /* ── Onboarding / Tutorial Gateway Card ────────── */
    .gateway-card {
        background: #ffffff;
        border: 2px solid #FDE68A;
        border-radius: 20px;
        padding: 2.2rem 2.6rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 35px rgba(245, 158, 11, 0.12);
    }
    .gateway-card h2 {
        color: #88131B !important;
        font-size: 2rem;
        font-weight: 800;
        margin: 0 0 0.5rem 0;
    }
    .gateway-card p {
        color: #374151 !important;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    /* ── Hero Banner ───────────────────────────────── */
    
    /* ── Karnataka Tourism Official Portal Styles (High Contrast) ── */
    .karnataka-hero-portal {
        position: relative;
        overflow: hidden;
        border-radius: 24px;
        background-color: #080C16;
        background-image: 
            linear-gradient(180deg, rgba(8, 12, 22, 0.90) 0%, rgba(8, 12, 22, 0.78) 45%, rgba(8, 12, 22, 0.95) 100%),
            url('https://web-cms.karnatakatourism.org/wp-content/uploads/2025/07/mysore-palace-illuminated-1.jpg'),
            url('https://images.unsplash.com/photo-1609766857041-ed402ea8069a?auto=format&fit=crop&w=1600&q=80');
        background-size: cover;
        background-position: center 32%;
        padding: 3.2rem 2.4rem 2.2rem 2.4rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 18px 50px rgba(0,0,0,0.35);
        border: 1.5px solid rgba(255,255,255,0.22);
        text-align: center;
        color: #FFFFFF !important;
    }
    /* Force high-contrast pure white/gold on everything inside hero */
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal,
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal *,
    .stApp [data-testid="stMarkdownContainer"] .karnataka-hero-portal *,
    .stApp .karnataka-hero-portal * {
        color: #FFFFFF !important;
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.9);
    }
    .hero-top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.8rem;
        margin-bottom: 1.6rem;
    }
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .gov-badge-pill,
    .karnataka-hero-portal .gov-badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(12px);
        border: 1.5px solid rgba(254, 243, 199, 0.6) !important;
        border-radius: 30px;
        padding: 0.4rem 1.2rem;
        color: #FEF3C7 !important;
        font-weight: 800;
        font-size: 0.82rem;
        letter-spacing: 1px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.4);
    }
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .gov-badge-pill * {
        color: #FEF3C7 !important;
    }
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .gandaberunda-seal-pill,
    .karnataka-hero-portal .gandaberunda-seal-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, rgba(136,19,27,0.95), rgba(217,119,6,0.95)) !important;
        border: 1.5px solid #F59E0B !important;
        border-radius: 30px;
        padding: 0.4rem 1.2rem;
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 0.82rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.45);
    }
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .karnataka-kicker,
    .karnataka-hero-portal .karnataka-kicker {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.95rem;
        font-weight: 800;
        letter-spacing: 7px;
        color: #FBBF24 !important;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.95) !important;
    }
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .karnataka-hero-title,
    .karnataka-hero-portal .karnataka-hero-title {
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 3.6rem;
        font-weight: 800;
        color: #FFFFFF !important;
        line-height: 1.15;
        margin: 0 auto 0.5rem auto;
        text-shadow: 0 4px 26px rgba(0,0,0,0.95) !important;
        font-style: italic;
    }
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .karnataka-hero-sub,
    .karnataka-hero-portal .karnataka-hero-sub {
        font-size: 1.35rem;
        font-weight: 700;
        color: #FEF3C7 !important;
        margin-bottom: 1.1rem;
        text-shadow: 0 2px 12px rgba(0,0,0,0.85) !important;
    }
    .karnataka-hero-desc-box {
        background: rgba(10, 14, 26, 0.65);
        backdrop-filter: blur(10px);
        border: 1.5px solid rgba(255, 255, 255, 0.22);
        border-radius: 16px;
        padding: 1.1rem 1.8rem;
        max-width: 880px;
        margin: 0 auto 1.6rem auto;
        box-shadow: 0 6px 24px rgba(0,0,0,0.45);
    }
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .karnataka-hero-desc,
    .karnataka-hero-portal .karnataka-hero-desc {
        font-size: 1.08rem;
        color: #FFFFFF !important;
        line-height: 1.65;
        margin: 0;
        font-weight: 500;
        text-shadow: 0 2px 8px rgba(0,0,0,0.9) !important;
    }
    .karnataka-cta-wrapper {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-bottom: 1.4rem;
        flex-wrap: wrap;
    }
    .karnataka-cta-pill {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 1.05rem;
        padding: 0.85rem 2.2rem;
        border-radius: 40px;
        box-shadow: 0 6px 25px rgba(16,185,129,0.5);
        border: 1.5px solid rgba(255,255,255,0.45);
        text-decoration: none;
        cursor: pointer;
        transition: all 0.25s ease;
    }
    .karnataka-pills-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 1.2rem;
    }
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .k-pill,
    .karnataka-hero-portal .k-pill {
        background: rgba(15, 23, 42, 0.85) !important;
        backdrop-filter: blur(10px);
        color: #FFFFFF !important;
        font-weight: 700;
        font-size: 0.88rem;
        padding: 0.5rem 1.2rem;
        border-radius: 30px;
        border: 1.5px solid rgba(255,255,255,0.4) !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.45);
    }
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .k-pill *,
    .karnataka-hero-portal .k-pill * {
        color: #FFFFFF !important;
    }
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .k-pill.trending,
    .karnataka-hero-portal .k-pill.trending {
        background: linear-gradient(135deg, #D97706, #B45309) !important;
        border: 1.5px solid #FDE68A !important;
        color: #FFFFFF !important;
        font-weight: 800;
    }
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .k-pill.trending * {
        color: #FFFFFF !important;
    }
    .karnataka-hero-footer-bar {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin-top: 2rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(255,255,255,0.22);
        font-size: 0.84rem;
        color: #FEF3C7 !important;
        flex-wrap: wrap;
        gap: 12px;
    }
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .karnataka-hero-footer-bar,
    [data-testid="stMarkdownContainer"] .karnataka-hero-portal .karnataka-hero-footer-bar * {
        color: #FEF3C7 !important;
    }

    .hero-banner {
        background: linear-gradient(135deg, #7A0C16 0%, #A61B24 45%, #D97706 80%, #F59E0B 100%);
        padding: 2.4rem 2.8rem;
        border-radius: 20px;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 30px rgba(136, 19, 27, 0.22);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::after {
        content: '';
        position: absolute;
        top: -40%;
        right: -10%;
        width: 340px;
        height: 340px;
        background: radial-gradient(circle, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0) 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-banner h1 {
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0 0 0.4rem 0;
        color: #ffffff !important;
        text-shadow: 0 2px 6px rgba(0,0,0,0.25);
    }
    .hero-banner .subtitle {
        font-size: 1.25rem;
        font-weight: 700;
        color: #FEF3C7 !important;
        margin-bottom: 0.6rem;
    }
    .hero-banner p {
        color: #FFFFFF !important;
    }
    .hero-banner .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-top: 1.1rem;
    }
    .hero-banner .pill {
        background: rgba(0, 0, 0, 0.22);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 0.35rem 0.9rem;
        border-radius: 30px;
        font-size: 0.85rem;
        font-weight: 700;
        color: #ffffff !important;
    }

    /* ── Trip Builder Card ─────────────────────────── */
    .builder-card {
        background: #ffffff;
        border: 1.5px solid #E5E7EB;
        border-radius: 18px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);
    }
    .builder-card h3 {
        color: #88131B !important;
        font-size: 1.3rem;
        font-weight: 800;
        margin: 0 0 0.4rem 0;
    }

    /* ── Circuit Showcase Cards with Photos ────────── */
    .circuit-card {
        background: #ffffff;
        border: 1.5px solid #E5E7EB;
        border-radius: 16px;
        padding: 1.4rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.04);
        transition: all 0.25s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        overflow: hidden;
    }
    .circuit-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(136, 19, 27, 0.14);
        border-color: #D97706;
    }
    .circuit-card .photo-header {
        height: 135px;
        border-radius: 12px;
        margin: -1.4rem -1.4rem 1rem -1.4rem;
        background-size: cover;
        background-position: center;
        position: relative;
    }
    .circuit-card .badge {
        display: inline-block;
        background: #FEF3C7;
        color: #88131B !important;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    .circuit-card h3 {
        color: #111827 !important;
        font-size: 1.2rem;
        font-weight: 800;
        margin: 0 0 0.3rem 0;
    }
    .circuit-card .tagline {
        color: #88131B !important;
        font-size: 0.88rem;
        font-weight: 700;
        margin-bottom: 0.6rem;
    }
    .circuit-card p {
        color: #374151 !important;
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 0.8rem;
    }
    .circuit-card .meta {
        font-size: 0.82rem;
        color: #4B5563 !important;
        margin-top: auto;
        padding-top: 0.6rem;
        border-top: 1px dashed #E5E7EB;
    }

    /* ── Modern Cards ──────────────────────────────── */
    .dest-card {
        background: #ffffff;
        border: 1.5px solid #E5E7EB;
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .dest-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 22px rgba(136, 19, 27, 0.12);
        border-color: #F59E0B;
    }
    .dest-card h4 {
        margin: 0 0 0.35rem;
        color: #88131B !important;
        font-weight: 800;
    }
    .dest-card p {
        color: #374151 !important;
    }

    /* ── Kannada Phrase Cards with Audio ───────────── */
    .phrase-card {
        background: #ffffff;
        border: 1.5px solid #FED7AA;
        border-left: 6px solid #D97706;
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 2px 8px rgba(217, 119, 6, 0.08);
        transition: transform 0.15s ease;
    }
    .phrase-card:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 14px rgba(217, 119, 6, 0.16);
    }
    .phrase-card .kannada {
        font-family: 'Noto Sans Kannada', sans-serif;
        font-size: 1.55rem;
        font-weight: 800;
        color: #111827 !important;
        line-height: 1.4;
    }
    .phrase-card .phonetic {
        color: #88131B !important;
        font-weight: 700;
        font-size: 1rem;
        margin-top: 3px;
    }
    .audio-btn {
        background: linear-gradient(90deg, #D97706, #B45309);
        color: #ffffff !important;
        border: none;
        border-radius: 20px;
        padding: 0.35rem 0.95rem;
        font-size: 0.82rem;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        gap: 5px;
        font-weight: 700;
        box-shadow: 0 2px 6px rgba(180, 83, 9, 0.25);
        transition: transform 0.15s ease;
    }
    .audio-btn:hover {
        transform: scale(1.05);
        background: #88131B;
    }

    /* ── Timeline ──────────────────────────────────── */
    .day-header {
        background: linear-gradient(90deg, #7A0C16 0%, #A61B24 50%, #D97706 100%);
        padding: 0.9rem 1.4rem;
        border-radius: 12px;
        font-size: 1.22rem;
        font-weight: 800;
        margin: 1.6rem 0 0.8rem;
        box-shadow: 0 4px 14px rgba(136, 19, 27, 0.18);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .day-header, .day-header * {
        color: #ffffff !important;
    }
    .timeline-item {
        background: #ffffff;
        border: 1.5px solid #E5E7EB;
        border-left: 4px solid #D97706;
        border-radius: 10px;
        padding: 1rem 1.3rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .timeline-item .time-badge {
        background: #FEF3C7;
        color: #88131B !important;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 800;
        margin-right: 0.5rem;
    }

    /* ── Metric Cards ──────────────────────────────── */
    .metric-card {
        background: #ffffff;
        border: 1.5px solid #E5E7EB;
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }
    .metric-card .value {
        font-size: 2.1rem;
        font-weight: 800;
        color: #88131B !important;
        line-height: 1.1;
    }
    .metric-card .label {
        font-size: 0.88rem;
        font-weight: 700;
        color: #4B5563 !important;
        margin-top: 0.35rem;
    }

    /* ── Booking Action Bar ────────────────────────── */
    .booking-cta-bar {
        background: linear-gradient(135deg, #1F2937 0%, #374151 100%);
        border-radius: 16px;
        padding: 1.4rem 1.8rem;
        margin: 1.8rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    .booking-cta-bar .title {
        font-size: 1.18rem;
        font-weight: 800;
        color: #F59E0B !important;
    }
    .booking-cta-bar .desc {
        font-size: 0.9rem;
        color: #F3F4F6 !important;
        max-width: 550px;
    }
    .booking-btn {
        background: linear-gradient(90deg, #F59E0B, #D97706);
        color: #111827 !important;
        font-weight: 800;
        padding: 0.65rem 1.35rem;
        border-radius: 30px;
        text-decoration: none;
        display: inline-block;
        transition: transform 0.15s ease;
    }
    .booking-btn:hover {
        transform: scale(1.05);
    }

    /* ── Tutorial Step Cards ───────────────────────── */
    .tutorial-step-card {
        background: #ffffff;
        border: 1.5px solid #E5E7EB;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.1rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.03);
        display: flex;
        gap: 1.2rem;
        align-items: flex-start;
    }
    .step-number {
        background: linear-gradient(135deg, #88131B, #D97706);
        color: #ffffff !important;
        font-size: 1.3rem;
        font-weight: 800;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 3px 8px rgba(136, 19, 27, 0.25);
    }
    .step-content h4 {
        margin: 0 0 0.35rem 0;
        color: #88131B !important;
        font-size: 1.18rem;
        font-weight: 800;
    }
    .step-content p {
        margin: 0 0 0.5rem 0;
        color: #374151 !important;
        font-size: 0.95rem;
        line-height: 1.55;
    }
    .step-tip {
        background: #FEF3C7;
        color: #92400E !important;
        padding: 0.3rem 0.75rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
    }

    /* ── Cultural Info Blocks ──────────────────────── */
    .culture-block {
        background: #ffffff;
        border: 1.5px solid #E5E7EB;
        border-left: 5px solid #0F766E;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
        color: #1F2937 !important;
        font-size: 0.98rem;
        line-height: 1.65;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }

    /* ── ALL BUTTONS & VIEW TUTORIAL BUTTON - ALWAYS BRIGHT WHITE TEXT ── */
    .stButton > button,
    button[kind="secondary"],
    button[kind="primary"],
    [data-testid="baseButton-secondary"],
    [data-testid="baseButton-primary"],
    [data-testid="stBaseButton-secondary"],
    [data-testid="stBaseButton-primary"] {
        background: linear-gradient(90deg, #88131B 0%, #B81D24 50%, #D97706 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: 800 !important;
        border-radius: 12px !important;
        padding: 0.65rem 1.2rem !important;
        box-shadow: 0 4px 14px rgba(136, 19, 27, 0.28) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    .stButton > button:hover,
    button[kind="secondary"]:hover,
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(136, 19, 27, 0.38) !important;
    }

    /* Force WHITE text inside all button children */
    .stButton > button *,
    .stButton > button p,
    .stButton > button span,
    .stButton > button div,
    button[kind="secondary"] *,
    button[kind="secondary"] p,
    button[kind="secondary"] span,
    button[kind="secondary"] div,
    [data-testid="baseButton-secondary"] *,
    [data-testid="baseButton-secondary"] p,
    [data-testid="baseButton-secondary"] span,
    [data-testid="baseButton-secondary"] div,
    [data-testid="stBaseButton-secondary"] *,
    [data-testid="stBaseButton-secondary"] p,
    [data-testid="stBaseButton-secondary"] span,
    [data-testid="stBaseButton-secondary"] div {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3) !important;
        white-space: nowrap !important;
    }
</style>
"""


def inject_custom_css() -> None:
    """Inject the project's custom CSS into the Streamlit page."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_hero_banner() -> None:
    """Render the official Karnataka Tourism-styled dynamic cinematic hero banner."""
    html_content = """<div class="karnataka-hero-portal">
<div class="hero-top-bar">
    <div class="gov-badge-pill" style="color:#FEF3C7 !important;">
        <span style="font-size:1.05rem;">🏛️</span>
        <span style="color:#FEF3C7 !important; font-weight:800;">ಕರ್ನಾಟಕ ಸರ್ಕಾರ • KANNADA DIGITAL INNOVATION HACKATHON 2026</span>
    </div>
    <div class="gandaberunda-seal-pill" style="color:#FFFFFF !important;">
        <span style="font-size:1.1rem;">👑</span>
        <span style="color:#FFFFFF !important; font-weight:800;">Gandaberunda Royal Seal Verified</span>
    </div>
</div>

<div class="karnataka-kicker" style="color:#FBBF24 !important;">K A R N A T A K A</div>
<div class="karnataka-hero-title" style="color:#FFFFFF !important;">One State, Many Worlds.</div>
<div class="karnataka-hero-sub" style="color:#FEF3C7 !important;">KannadaYatra AI • ಕರ್ನಾಟಕ ಪ್ರವಾಸ ಸಹಾಯಕ</div>

<div class="karnataka-hero-desc-box">
    <p class="karnataka-hero-desc" style="color:#FFFFFF !important;">
        Your intelligent, hyper-personalized AI travel companion for Karnataka. 
        Experience Karnataka like a local, not just a tourist, with living cultural deep-dives, 
        phonetically-taught 5-language survival phrases, real-world KSRTC transit feasibility, and secret culinary trails.
    </p>
</div>

<div class="karnataka-cta-wrapper">
    <div class="karnataka-cta-pill" style="color:#FFFFFF !important;">
        <span style="color:#FFFFFF !important;">✨ Explore Itineraries Around You</span>
        <span style="color:#FFFFFF !important; font-size:1.2rem;">➔</span>
    </div>
</div>

<div class="karnataka-pills-row">
    <span class="k-pill trending" style="color:#FFFFFF !important; background:linear-gradient(135deg, #D97706, #B45309) !important; border:1.5px solid #FDE68A !important;">
        <span style="color:#FFFFFF !important;">🔥 What's trending?</span>
    </span>
    <span class="k-pill" style="color:#FFFFFF !important; background:rgba(15,23,42,0.85) !important; border:1.5px solid rgba(255,255,255,0.45) !important;">
        <span style="color:#FFFFFF !important;">👑 Royal Wadiyar Heritage</span>
    </span>
    <span class="k-pill" style="color:#FFFFFF !important; background:rgba(15,23,42,0.85) !important; border:1.5px solid rgba(255,255,255,0.45) !important;">
        <span style="color:#FFFFFF !important;">☕ Misty Ghats & Coffee</span>
    </span>
    <span class="k-pill" style="color:#FFFFFF !important; background:rgba(15,23,42,0.85) !important; border:1.5px solid rgba(255,255,255,0.45) !important;">
        <span style="color:#FFFFFF !important;">🌊 Karavali Coast & Sands</span>
    </span>
    <span class="k-pill" style="color:#FFFFFF !important; background:rgba(15,23,42,0.85) !important; border:1.5px solid rgba(255,255,255,0.45) !important;">
        <span style="color:#FFFFFF !important;">🏛️ UNESCO Stone Empires</span>
    </span>
</div>

<div class="karnataka-hero-footer-bar" style="color:#FEF3C7 !important;">
    <div style="color:#FEF3C7 !important;"><span style="color:#FEF3C7 !important;">🔈 <b style="color:#FFFFFF !important;">Audio Synthesizer:</b> Natural spoken Kannada voice active</span></div>
    <div style="color:#FEF3C7 !important;"><span style="color:#FEF3C7 !important;">📍 <b style="color:#FFFFFF !important;">Zero Map Paywall:</b> Watermark-free OpenStreetMap</span></div>
    <div style="color:#FEF3C7 !important;"><span style="color:#FEF3C7 !important;">⚡ <b style="color:#FFFFFF !important;">Dual-Engine AI:</b> Gemini 2.5 Flash + 6ms Offline Fallback</span></div>
</div>
</div>"""
    st.markdown(html_content, unsafe_allow_html=True)


def format_inr(amount: int) -> str:
    """Format an integer as Indian Rupee string with commas (lakhs style)."""
    s = str(amount)
    if len(s) <= 3:
        return f"₹{s}"
    last3 = s[-3:]
    rest  = s[:-3]
    # Add commas every 2 digits for lakh/crore grouping
    parts = []
    while len(rest) > 2:
        parts.insert(0, rest[-2:])
        rest = rest[:-2]
    if rest:
        parts.insert(0, rest)
    return "₹" + ",".join(parts) + "," + last3

