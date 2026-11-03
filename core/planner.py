"""
core/planner.py - KannadaYatra AI
AI-powered itinerary generation using Google Gemini, with robust
fallback to curated local data when the API is unavailable.
"""

from __future__ import annotations

import json
import os
import random
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

try:
    # pyrefly: ignore[missing-import]
    from dotenv import load_dotenv
except ImportError:
    # python-dotenv not installed - env vars must be set externally
    def load_dotenv():
        pass

from utils.helpers import (
    KARNATAKA_DESTINATIONS,
    Destination,
    filter_destinations,
    compute_trip_budget,
)
from core.insights import (
    get_context_phrases,
    get_cuisine_for_destination,
    get_festivals_for_region,
    get_heritage_history,
)

# Load environment variables from .env (if present)
load_dotenv()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1.  DATA MODELS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@dataclass
class TimeSlot:
    """A single activity block within a day."""
    time: str               # e.g. "09:00 AM"
    activity: str           # Short title
    destination: str        # Destination name from DB (or custom)
    description: str        # 1-2 sentence detail
    duration_hrs: float
    travel_tip: str = ""


@dataclass
class DayPlan:
    """Full plan for one day of the trip."""
    day_number: int
    title: str              # e.g. "Royal Mysore"
    slots: List[TimeSlot]
    overnight_stay: str     # city/area name
    day_highlights: List[str] = field(default_factory=list)


@dataclass
class Itinerary:
    """Complete trip itinerary."""
    trip_title: str
    days: List[DayPlan]
    interests: List[str]
    budget_tier: str
    num_travelers: int
    overview: str = ""
    pro_tips: List[str] = field(default_factory=list)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2.  GEMINI API INTEGRATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_gemini_api_key() -> str:
    """
    Resolve Gemini API key across multiple sources:
    1. Streamlit session_state (user entered in UI)
    2. Streamlit Cloud Secrets (st.secrets["GEMINI_API_KEY"] or st.secrets["GOOGLE_API_KEY"])
    3. Environment variables (os.environ["GEMINI_API_KEY"] or os.environ["GOOGLE_API_KEY"])
    """
    # 1. Streamlit session_state
    try:
        import streamlit as st
        key = st.session_state.get("gemini_api_key", "").strip()
        if key and key != "your_gemini_api_key_here":
            return key
    except Exception:
        pass

    # 2. Streamlit Cloud Secrets
    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            for sec_name in ["GEMINI_API_KEY", "GOOGLE_API_KEY", "gemini_api_key", "google_api_key"]:
                if sec_name in st.secrets and st.secrets[sec_name]:
                    val = str(st.secrets[sec_name]).strip()
                    if val and val != "your_gemini_api_key_here":
                        return val
    except Exception:
        pass

    # 3. Environment variables
    for env_name in ["GEMINI_API_KEY", "GOOGLE_API_KEY"]:
        val = os.getenv(env_name, "").strip()
        if val and val != "your_gemini_api_key_here":
            return val

    return ""


def _get_gemini_model(model_name: Optional[str] = None):
    """
    Initialise and return a Gemini GenerativeModel.
    Supports custom model names via GEMINI_MODEL env var or fallback hierarchy.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)

        # Priority: explicit param -> GEMINI_MODEL in env -> modern defaults
        target_model = model_name or os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
        if not target_model:
            target_model = "gemini-2.5-flash"

        model = genai.GenerativeModel(target_model)
        return model
    except Exception as e:
        print(f"[KannadaYatra AI] Gemini model init warning: {e}")
        return None


def _build_itinerary_prompt(
    interests: List[str],
    budget_tier: str,
    days: int,
    travelers: int,
    companions: str,
    language: str = "English",
) -> str:
    """Construct a detailed prompt for AI itinerary generation."""
    available = filter_destinations(interests, max_results=20)
    dest_names = [d.name for d in available]

    lang_instruction = ""
    if language != "English":
        lang_instruction = f"\nIMPORTANT: Write the trip_title, overview, each day title, activity descriptions, and travel tips in {language} language."

    return f"""You are KannadaYatra AI - an expert Karnataka travel planner.

Generate a {days}-day Karnataka travel itinerary with the following constraints:
- Interests: {', '.join(interests)}
- Budget Level: {budget_tier}
- Number of Travelers: {travelers}
- Travel Companions: {companions}
- User Language: {language}{lang_instruction}

Available Karnataka destinations to choose from (pick the best fit):
{', '.join(dest_names)}

RESPOND IN VALID JSON ONLY. Use this exact structure:
{{
  "trip_title": "A catchy title for the trip",
  "overview": "2-3 sentence trip overview",
  "days": [
    {{
      "day_number": 1,
      "title": "Day theme title",
      "overnight_stay": "City name",
      "day_highlights": ["highlight 1", "highlight 2"],
      "slots": [
        {{
          "time": "09:00 AM",
          "activity": "Activity title",
          "destination": "Exact destination name from the list",
          "description": "1-2 sentence description of the activity",
          "duration_hrs": 2.5,
          "travel_tip": "Useful tip for this activity"
        }}
      ]
    }}
  ],
  "pro_tips": ["tip 1", "tip 2", "tip 3"]
}}

Requirements:
1. Each day should have 3-5 activity slots from morning to evening.
2. Activities should be logically sequenced (nearby locations together).
3. Include travel time between destinations.
4. Match activities to the {budget_tier} budget level.
5. Include local food recommendations for each day.
6. Make the itinerary practical and realistic, not rushed.
7. For {companions} travelers, ensure activities are suitable.

Return ONLY the JSON, no markdown formatting or explanation."""


def _parse_gemini_response(text: str) -> Optional[Dict]:
    """Extract and parse JSON from the Gemini response text."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    json_match = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group())
        except json.JSONDecodeError:
            pass

    return None


def _is_api_reachable(timeout: float = 3.0) -> bool:
    """Probe to ensure Google Gemini endpoint is reachable. Permissive fallback for containers."""
    import socket
    try:
        sock = socket.create_connection(("generativelanguage.googleapis.com", 443), timeout=timeout)
        sock.close()
        return True
    except Exception:
        # In cloud containers, socket probes can fail while HTTP succeeds; proceed to SDK
        return True


def generate_ai_itinerary(
    interests: List[str],
    budget_tier: str,
    days: int,
    travelers: int,
    companions: str,
    language: str = "English",
) -> Optional[Itinerary]:
    """
    Attempt to generate an itinerary via Google Gemini with safety timeout.
    Returns an Itinerary dataclass or None on failure (falling back to curated immediately).
    """
    api_key = get_gemini_api_key()
    if not api_key:
        return None

    configured_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    model_name = configured_model or "gemini-2.5-flash"
    prompt = _build_itinerary_prompt(interests, budget_tier, days, travelers, companions, language=language)

    try:
        import socket
        orig_timeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(7.0)

        model = _get_gemini_model(model_name)
        if model is None:
            return None

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 4096,
            },
        )
        parsed = _parse_gemini_response(response.text)
        if parsed is not None:
            return _dict_to_itinerary(parsed, interests, budget_tier, travelers)

    except Exception as e:
        print(f"[KannadaYatra AI] AI generation fallback triggered: {e}")
        return None
    finally:
        try:
            socket.setdefaulttimeout(orig_timeout)
        except Exception:
            pass

    return None


def _dict_to_itinerary(
    data: Dict,
    interests: List[str],
    budget_tier: str,
    travelers: int,
) -> Itinerary:
    """Convert a parsed JSON dict into an Itinerary dataclass."""
    day_plans = []
    for d in data.get("days", []):
        slots = []
        for s in d.get("slots", []):
            slots.append(TimeSlot(
                time=s.get("time", ""),
                activity=s.get("activity", ""),
                destination=s.get("destination", ""),
                description=s.get("description", ""),
                duration_hrs=float(s.get("duration_hrs", 1)),
                travel_tip=s.get("travel_tip", ""),
            ))
        day_plans.append(DayPlan(
            day_number=d.get("day_number", 0),
            title=d.get("title", ""),
            slots=slots,
            overnight_stay=d.get("overnight_stay", ""),
            day_highlights=d.get("day_highlights", []),
        ))

    return Itinerary(
        trip_title=data.get("trip_title", "Your Karnataka Adventure"),
        days=day_plans,
        interests=interests,
        budget_tier=budget_tier,
        num_travelers=travelers,
        overview=data.get("overview", ""),
        pro_tips=data.get("pro_tips", []),
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3.  CURATED FALLBACK ENGINE - works offline without any API
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Pre-built itinerary templates for common scenarios
_CURATED_ROUTES: Dict[str, List[List[str]]] = {
    # Routes by primary interest - each inner list is one day's destinations
    "Heritage": [
        ["Bangalore", "Srirangapatna"],
        ["Mysore Palace", "Chamundi Hills"],
        ["Belur", "Halebidu"],
        ["Shravanabelagola"],
        ["Hampi"],
        ["Badami", "Aihole", "Pattadakal"],
        ["Bijapur (Vijayapura)"],
    ],
    "Nature": [
        ["Bangalore", "Nandi Hills"],
        ["Coorg (Kodagu)"],
        ["Chikmagalur"],
        ["Kudremukh"],
        ["Jog Falls"],
        ["Dandeli"],
        ["Bandipur National Park"],
    ],
    "Food": [
        ["Bangalore"],
        ["Mysore Palace"],      # Mysore Pak, Mysore Masala Dosa
        ["Udupi"],
        ["Mangalore"],
        ["Coorg (Kodagu)"],
        ["Davangere"],
        ["Dharwad"],
    ],
    "Adventure": [
        ["Bangalore", "Nandi Hills"],
        ["Sakleshpur"],
        ["Chikmagalur"],
        ["Dandeli"],
        ["Gokarna"],
        ["Murdeshwar"],
        ["Nagarhole (Kabini)"],
    ],
}

# Time templates for a typical tourism day
_TIME_TEMPLATES = [
    ("07:00 AM", "Breakfast & hotel checkout / start", 1.0),
    ("08:30 AM", "Morning sightseeing", 2.5),
    ("11:00 AM", "Mid-morning exploration", 2.0),
    ("01:00 PM", "Lunch at a local eatery", 1.0),
    ("02:30 PM", "Afternoon activity", 2.5),
    ("05:00 PM", "Evening leisure / sunset point", 1.5),
    ("07:00 PM", "Dinner & overnight stay", 1.5),
]

# Food recommendations per budget tier
_FOOD_RECS = {
    "Budget": {
        "breakfast": "Local darshini or tea stall",
        "lunch": "Thali meals at a working-class eatery (₹60-100)",
        "dinner": "Street food or small family restaurant",
    },
    "Mid-range": {
        "breakfast": "Hotel breakfast or popular local café",
        "lunch": "Well-known regional restaurant (₹200-400)",
        "dinner": "Specialty restaurant with local cuisine",
    },
    "Luxury": {
        "breakfast": "Resort/heritage hotel breakfast spread",
        "lunch": "Fine dining or curated food experience (₹800+)",
        "dinner": "Premium restaurant with tasting menu",
    },
}


def _build_day_slots(
    destinations: List[str],
    day_num: int,
    budget_tier: str,
) -> List[TimeSlot]:
    """Build realistic time-slotted activities for a day's destinations."""
    slots: List[TimeSlot] = []
    dest_objects = [KARNATAKA_DESTINATIONS.get(d) for d in destinations]
    dest_objects = [d for d in dest_objects if d is not None]

    food_rec = _FOOD_RECS.get(budget_tier, _FOOD_RECS["Mid-range"])

    if not dest_objects:
        return slots

    # Breakfast slot
    first = dest_objects[0]
    slots.append(TimeSlot(
        time="07:00 AM",
        activity=f"Breakfast - {food_rec['breakfast']}",
        destination=first.name,
        description=f"Start the day in {first.region}. {food_rec['breakfast']}.",
        duration_hrs=1.0,
        travel_tip="Start early to beat the crowd at popular sites.",
    ))

    # Assign exploration slots
    template_idx = 1  # skip breakfast
    for dest in dest_objects:
        if template_idx >= len(_TIME_TEMPLATES) - 1:
            break

        time_str, _, dur = _TIME_TEMPLATES[template_idx]
        slots.append(TimeSlot(
            time=time_str,
            activity=f"Explore {dest.name}",
            destination=dest.name,
            description=dest.description[:150] + "..." if len(dest.description) > 150 else dest.description,
            duration_hrs=min(dest.time_needed_hrs, dur + 0.5),
            travel_tip=f"Best season: {dest.best_season}. "
                       f"{'Entry: ₹' + str(dest.entry_fee_inr) if dest.entry_fee_inr > 0 else 'Free entry'}.",
        ))
        template_idx += 1

        # Add a highlight activity if there's a standout highlight
        if dest.highlights and template_idx < len(_TIME_TEMPLATES) - 1:
            time_str2, _, dur2 = _TIME_TEMPLATES[template_idx]
            highlight = dest.highlights[0]
            slots.append(TimeSlot(
                time=time_str2,
                activity=f"Must-See: {highlight}",
                destination=dest.name,
                description=f"Don't miss the {highlight} at {dest.name}. "
                            f"Other highlights: {', '.join(dest.highlights[1:3])}.",
                duration_hrs=dur2,
                travel_tip=", ".join(dest.highlights[1:]) if len(dest.highlights) > 1 else "",
            ))
            template_idx += 1

    # Lunch
    if template_idx <= 3:
        template_idx = 3  # force lunch at 1 PM
    if template_idx < len(_TIME_TEMPLATES):
        time_str, _, dur = _TIME_TEMPLATES[min(template_idx, 3)]
        cuisine = get_cuisine_for_destination(dest_objects[0].name)
        cuisine_note = f" Try: {cuisine.must_try}" if cuisine else ""
        slots.append(TimeSlot(
            time="01:00 PM",
            activity=f"Lunch - {food_rec['lunch']}",
            destination=dest_objects[0].name,
            description=f"Savour local cuisine.{cuisine_note}",
            duration_hrs=1.0,
            travel_tip="Ask locals for their favourite eatery - hidden gems abound!",
        ))

    # Dinner
    slots.append(TimeSlot(
        time="07:00 PM",
        activity=f"Dinner - {food_rec['dinner']}",
        destination=dest_objects[-1].name,
        description=f"Wind down with a satisfying dinner. {food_rec['dinner']}.",
        duration_hrs=1.5,
        travel_tip="Don't miss the local sweets - every region has its own specialty.",
    ))

    # Sort by time
    slots.sort(key=lambda s: s.time)
    return slots


def generate_curated_itinerary(
    interests: List[str],
    budget_tier: str,
    days: int,
    travelers: int,
    companions: str,
) -> Itinerary:
    """
    Generate a high-quality itinerary from curated route templates.
    Always succeeds - this is the offline fallback.
    """
    # Merge routes from all selected interests
    all_day_routes: List[List[str]] = []
    seen = set()
    for interest in interests:
        for route_day in _CURATED_ROUTES.get(interest, _CURATED_ROUTES["Heritage"]):
            key = tuple(sorted(route_day))
            if key not in seen:
                seen.add(key)
                all_day_routes.append(route_day)

    # Trim or extend to match requested days
    if len(all_day_routes) > days:
        all_day_routes = all_day_routes[:days]
    elif len(all_day_routes) < days:
        # Repeat/extend with remaining destinations
        extra_dests = filter_destinations(interests, max_results=30)
        used_names = {name for route in all_day_routes for name in route}
        extras = [d.name for d in extra_dests if d.name not in used_names]
        while len(all_day_routes) < days and extras:
            all_day_routes.append([extras.pop(0)])
        # If still not enough, repeat last day
        while len(all_day_routes) < days:
            all_day_routes.append(all_day_routes[-1])

    # Build day plans
    day_plans: List[DayPlan] = []
    for i, route_dests in enumerate(all_day_routes, start=1):
        slots = _build_day_slots(route_dests, i, budget_tier)

        # Day title
        if len(route_dests) == 1:
            title = f"Discover {route_dests[0]}"
        else:
            title = f"{route_dests[0]} & {route_dests[-1]}"

        # Highlights
        highlights = []
        for dest_name in route_dests:
            dest = KARNATAKA_DESTINATIONS.get(dest_name)
            if dest:
                highlights.extend(dest.highlights[:2])

        day_plans.append(DayPlan(
            day_number=i,
            title=title,
            slots=slots,
            overnight_stay=route_dests[-1].split("(")[0].strip(),  # city name
            day_highlights=highlights[:4],
        ))

    # Pro tips
    pro_tips = [
        f"💰 For {budget_tier} travel, daily budget is roughly "
        f"₹{compute_trip_budget(budget_tier, 1, travelers)['total_avg'] // days:,}/day for {travelers} traveler(s).",
        "📱 Download offline Google Maps for Karnataka - network can be spotty in the Ghats.",
        "🚌 KSRTC Airavat Club Class buses are the best value for intercity travel.",
        "☀️ Carry sunscreen and water bottles - Karnataka's heritage sites involve lots of walking.",
        "📸 Photography fees vary by site - always check before clicking at heritage monuments.",
    ]

    # Trip title
    interest_str = " & ".join(interests[:2])
    title = f"Karnataka {interest_str} Explorer - {days}-Day {budget_tier} Journey"

    overview = (
        f"A curated {days}-day {budget_tier.lower()} itinerary through Karnataka focusing on "
        f"{', '.join(interests).lower()}. This route takes {travelers} traveler(s) through "
        f"the best of what the state has to offer, from ancient heritage to living traditions."
    )

    return Itinerary(
        trip_title=title,
        days=day_plans,
        interests=interests,
        budget_tier=budget_tier,
        num_travelers=travelers,
        overview=overview,
        pro_tips=pro_tips,
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4.  MAIN ENTRY POINT - tries AI, falls back to curated
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def generate_itinerary(
    interests: List[str],
    budget_tier: str,
    days: int,
    travelers: int,
    companions: str = "Friends",
    fast_launch: bool = False,
    language: str = "English",
) -> Tuple[Itinerary, bool]:
    """
    Generate a trip itinerary. If fast_launch is True (e.g. for 1-click circuits
    or instant previews), generates immediately from curated routes (< 5ms).
    Otherwise attempts Gemini AI with a safety timeout before falling back.

    Returns:
        (Itinerary, ai_used: bool)
    """
    if fast_launch:
        curated = generate_curated_itinerary(interests, budget_tier, days, travelers, companions)
        return curated, False

    # Attempt AI generation if key is present
    try:
        if get_gemini_api_key():
            ai_result = generate_ai_itinerary(interests, budget_tier, days, travelers, companions, language=language)
            if ai_result is not None and len(ai_result.days) > 0:
                return ai_result, True
    except Exception as e:
        print(f"[KannadaYatra AI] Safe fallback on AI exception: {e}")

    # Fallback to curated engine
    curated = generate_curated_itinerary(interests, budget_tier, days, travelers, companions)
    return curated, False

