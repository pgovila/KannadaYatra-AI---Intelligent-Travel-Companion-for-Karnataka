"""
app.py - KannadaYatra AI (Release v2.2 - Pure White Hero Text & Officials Removed)

Main Streamlit application with a website-style top navigation bar,
light warm sandstone theme, 1-click curated circuits, audio phrase pronunciation,
and an interactive user tutorial guide.
"""

from __future__ import annotations

import importlib
import utils.helpers
importlib.reload(utils.helpers)

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

from utils.helpers import (
    KARNATAKA_DESTINATIONS,
    Destination,
    CURATED_CIRCUITS,
    DESTINATION_IMAGES,
    get_destination_image,
    inject_custom_css,
    render_hero_banner,
    init_session_state,
    reset_session_state,
    filter_destinations,
    compute_trip_budget,
    budget_saving_tips,
    format_inr,
    get_all_regions,
    get_destinations_by_region,
    GANDABERUNDA_SEAL_SVG,
    GANDABERUNDA_HERITAGE_BADGE_HTML,
)
from core.planner import generate_itinerary, Itinerary, DayPlan, TimeSlot, get_gemini_api_key
from core.insights import (
    PHRASE_CATEGORIES,
    KannadaPhrase,
    get_context_phrases,
    get_full_cultural_context,
    get_cuisine_for_destination,
    get_festivals_for_region,
    get_heritage_history,
    KARNATAKA_FESTIVALS,
    REGIONAL_CUISINES,
    search_travel_phrases,
    TRAVEL_SCENARIOS,
    UI_LOCALIZATION,
    localize_itinerary,
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. PAGE CONFIG & STYLING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.set_page_config(
    page_title="KannadaYatra AI - Karnataka Travel Companion",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_custom_css()
init_session_state()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ONBOARDING GATEWAY (TUTORIAL BEFORE APP STARTS)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def render_onboarding_tutorial():
    render_hero_banner()

    st.markdown(
        f"""<div class="gateway-card" style="display:flex; align-items:center; justify-content:space-between; gap:1.5rem; flex-wrap:wrap;">
<div style="flex:1; min-width:280px;">
<h2 style="margin-top:0;">📖 Quick-Start Tutorial & Onboarding</h2>
<p style="margin-bottom:0;">
Before entering the application, here is a quick 1-minute walkthrough on how KannadaYatra AI 
empowers you to experience Karnataka like a local, not just a tourist.
</p>
</div>
<div style="background:#FFFBEB; border:1.5px solid #FDE68A; border-radius:16px; padding:0.6rem 1.1rem; display:flex; align-items:center; gap:12px; box-shadow:0 2px 8px rgba(0,0,0,0.04);">
{GANDABERUNDA_SEAL_SVG}
<div>
<div style="font-size:0.72rem; font-weight:800; color:#88131B; text-transform:uppercase; letter-spacing:0.5px;">ಕರ್ನಾಟಕ ರಾಜ್ಯ ಲಾಂಛನ</div>
<div style="font-weight:800; font-size:0.88rem; color:#111827;">Official Heritage Seal Verified</div>
</div>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # 4-Step Walkthrough Cards
    st.markdown(
        """<div class="tutorial-step-card">
<div class="step-number">1</div>
<div class="step-content">
<h4>Choose Your Route (1-Click Presets or Custom Planner)</h4>
<p>
• <b>1-Click Presets:</b> Launch iconic routes (Royal Wadiyar, Misty Ghats, Karavali Coast, or UNESCO Stone Empires) in a single tap.<br>
• <b>Custom Planner:</b> Tailor your duration (1-14 days), budget (Budget, Mid-range, Luxury), group size, and companion style.
</p>
<span class="step-tip">💡 Curated engine works 100% offline - no API key required!</span>
</div>
</div>

<div class="tutorial-step-card">
<div class="step-number">2</div>
<div class="step-content">
<h4>Interactive Route Map & Chronological Timeline</h4>
<p>
• View your travel path rendered on a high-resolution, watermark-free OpenStreetMap.<br>
• Benefit from <b>⏰ Optimal Timing</b> alerts to beat crowds at monuments and sunset points.<br>
• Discover <b>🍛 Local Food Secrets</b> (hidden eateries like Guru Sweet Mart in Mysore or Town Canteen in Chikmagalur).
</p>
<span class="step-tip">💡 Download an offline Travel Pass (.txt) for your phone anytime!</span>
</div>
</div>

<div class="tutorial-step-card">
<div class="step-number">3</div>
<div class="step-content">
<h4>Real-World Kannada Survival Kit with Native Audio</h4>
<p>
• Access 60+ context-specific phrases for ordering food, bargaining with auto drivers, and asking directions.<br>
• Click the <b>🔊 Listen</b> button on any phrase to hear natural audio pronunciation directly through your speakers!
</p>
<span class="step-tip">💡 Speaking basic Kannada like 'Namaskāra' creates genuine smiles across Karnataka.</span>
</div>
</div>

<div class="tutorial-step-card">
<div class="step-number">4</div>
<div class="step-content">
<h4>Smart Budget Optimizer & Direct Government Bookings</h4>
<p>
• Real-time financial breakdowns across accommodation, food, transit, and activities with interactive Plotly charts.<br>
• Direct links to verified portals: KSTDC Heritage Tours, KSRTC Airavat Buses, and Eco-Tourism Safari permits.
</p>
<span class="step-tip">💡 Save 30-40% by booking official state transport directly.</span>
</div>
</div>""",
        unsafe_allow_html=True,
    )

    # ── Visual Gallery of Karnataka's 4 Iconic Belts ──
    st.markdown("### 📸 Explore Karnataka's 4 Distinct Travel Belts:")
    gcol1, gcol2, gcol3, gcol4 = st.columns(4)
    with gcol1:
        st.markdown(
            f"""<div style="background:#fff; border-radius:12px; overflow:hidden; border:1px solid #E5E7EB; box-shadow:0 3px 10px rgba(0,0,0,0.05); text-align:center;">
<img src="{CURATED_CIRCUITS['👑 Royal Wadiyar Heritage']['image_url']}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1609766857041-ed402ea8069a?auto=format&fit=crop&w=650&q=80';" style="width:100%; height:120px; object-fit:cover; background:#88131B;" />
<div style="padding:0.6rem; font-weight:800; font-size:0.88rem; color:#88131B;">👑 Mysore & Hoysala</div>
<div style="font-size:0.75rem; color:#6B7280; padding-bottom:0.5rem;">Palaces · Temples · Silk</div>
</div>""",
            unsafe_allow_html=True,
        )
    with gcol2:
        st.markdown(
            f"""<div style="background:#fff; border-radius:12px; overflow:hidden; border:1px solid #E5E7EB; box-shadow:0 3px 10px rgba(0,0,0,0.05); text-align:center;">
<img src="{CURATED_CIRCUITS['☕ Misty Ghats & Coffee Trails']['image_url']}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=650&q=80';" style="width:100%; height:120px; object-fit:cover; background:#0F766E;" />
<div style="padding:0.6rem; font-weight:800; font-size:0.88rem; color:#88131B;">☕ Western Ghats</div>
<div style="font-size:0.75rem; color:#6B7280; padding-bottom:0.5rem;">Coorg · Coffee · Treks</div>
</div>""",
            unsafe_allow_html=True,
        )
    with gcol3:
        st.markdown(
            f"""<div style="background:#fff; border-radius:12px; overflow:hidden; border:1px solid #E5E7EB; box-shadow:0 3px 10px rgba(0,0,0,0.05); text-align:center;">
<img src="{CURATED_CIRCUITS['🌊 Coastal Sunset & Spiritual Sands']['image_url']}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=650&q=80';" style="width:100%; height:120px; object-fit:cover; background:#1E3A8A;" />
<div style="padding:0.6rem; font-weight:800; font-size:0.88rem; color:#88131B;">🌊 Karavali Coast</div>
<div style="font-size:0.75rem; color:#6B7280; padding-bottom:0.5rem;">Gokarna · Murdeshwar · Food</div>
</div>""",
            unsafe_allow_html=True,
        )
    with gcol4:
        st.markdown(
            f"""<div style="background:#fff; border-radius:12px; overflow:hidden; border:1px solid #E5E7EB; box-shadow:0 3px 10px rgba(0,0,0,0.05); text-align:center;">
<img src="{CURATED_CIRCUITS['🏛️ UNESCO Stone Empires']['image_url']}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1590050752117-238cb0fb12b1?auto=format&fit=crop&w=650&q=80';" style="width:100%; height:120px; object-fit:cover; background:#D97706;" />
<div style="padding:0.6rem; font-weight:800; font-size:0.88rem; color:#88131B;">🏛️ Stone Empires</div>
<div style="font-size:0.75rem; color:#6B7280; padding-bottom:0.5rem;">Hampi · Badami · Caves</div>
</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 🎯 Quick-Select Your Starting Karnataka Vibe:")

    t_col1, t_col2 = st.columns([3, 1.8])
    with t_col2:
        cur_lang = st.session_state.get("app_lang", "English")
        lang_idx = ["English", "Kannada", "Hindi", "Tamil", "Telugu"].index(cur_lang) if cur_lang in ["English", "Kannada", "Hindi", "Tamil", "Telugu"] else 0
        chosen_lang = st.selectbox(
            "🌐 Choose Language / ಭಾಷೆ / भाषा",
            options=["English", "Kannada", "Hindi", "Tamil", "Telugu"],
            format_func=lambda l: {
                "English": "🇬🇧 English",
                "Kannada": "🇮🇳 ಕನ್ನಡ (Kannada)",
                "Hindi": "🇮🇳 हिन्दी (Hindi)",
                "Tamil": "🇮🇳 தமிழ் (Tamil)",
                "Telugu": "🇮🇳 తెలుగు (Telugu)",
            }.get(l, l),
            index=lang_idx,
            key="tutorial_lang_picker",
        )
        if chosen_lang != cur_lang:
            st.session_state["app_lang"] = chosen_lang
            st.session_state["tourist_lang"] = chosen_lang
            st.rerun()

    circuit_keys = list(CURATED_CIRCUITS.keys())
    selected_vibe = st.radio(
        "Choose an iconic circuit to start with (or enter with a blank slate):",
        options=["Enter blank custom planner"] + circuit_keys,
        index=1,
    )

    col_btn1, col_btn2 = st.columns([2, 3])
    with col_btn1:
        if st.button("🚀 Enter KannadaYatra AI & Start Exploring", key="enter_app_btn", type="primary", use_container_width=True):
            st.session_state["tutorial_completed"] = True
            st.session_state["main_nav_bar"] = "explore"
            st.rerun()

    with col_btn2:
        if selected_vibe != "Enter blank custom planner":
            c_info = CURATED_CIRCUITS[selected_vibe]
            if st.button(f"⚡ Quick-Launch '{selected_vibe}' Immediately", key="quick_launch_gateway_btn", use_container_width=True):
                with st.spinner(f"Preparing {c_info['title']}…"):
                    itinerary, used_ai = generate_itinerary(
                        interests=c_info["interests"],
                        budget_tier=c_info["budget"],
                        days=c_info["days"],
                        travelers=c_info["travelers"],
                        companions=c_info["companions"],
                        fast_launch=True,
                    )
                    budget_data = compute_trip_budget(c_info["budget"], c_info["days"], c_info["travelers"])
                    st.session_state["itinerary"] = itinerary
                    st.session_state["budget_data"] = budget_data
                    st.session_state["generation_done"] = True
                    st.session_state["used_ai"] = used_ai
                    st.session_state["trip_prefs"] = {
                        "interests": c_info["interests"],
                        "budget_tier": c_info["budget"],
                        "days": c_info["days"],
                        "travelers": c_info["travelers"],
                        "companions": c_info["companions"],
                    }
                    st.session_state["tutorial_completed"] = True
                    st.session_state["main_nav_bar"] = "itinerary"
                    st.session_state["main_nav_bar_radio"] = "itinerary"
                    st.rerun()


# Intercept if onboarding tutorial not completed yet
if not st.session_state.get("tutorial_completed", False):
    render_onboarding_tutorial()
    st.stop()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. TOP WEBSITE HEADER BAR (MAIN APPLICATION)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cur_app_lang = st.session_state.get("app_lang", "English")
ui_str = UI_LOCALIZATION.get(cur_app_lang, UI_LOCALIZATION["English"])

head_c1, head_c_sos, head_c_key, head_c2, head_c3 = st.columns([2.6, 0.7, 0.9, 1.2, 0.9])
with head_c1:
    st.markdown(
        f"""
        <div class="top-navbar" style="margin-bottom:0; padding:0.6rem 1.2rem;">
            <div class="brand" style="display:flex; align-items:center; gap:12px;">
                <div style="background:#FFFFFF; border:1px solid #E5E7EB; border-radius:10px; padding:3px 8px; box-shadow:0 2px 6px rgba(0,0,0,0.06); display:flex; align-items:center;">
                    <img src="https://karnatakatourism.org/_next/static/media/logo.2s-4nubynwmtz.svg" onerror="this.onerror=null; this.src='https://web-cms.karnatakatourism.org/wp-content/uploads/2025/11/kannada-Rajyotsava.png';" style="height:32px; width:auto;" alt="Karnataka Tourism" />
                </div>
                <div>
                    <div style="font-size:0.68rem; font-weight:800; color:#88131B; text-transform:uppercase; letter-spacing:0.5px;">ಕರ್ನಾಟಕ ಸರ್ಕಾರ • ಪ್ರವಾಸೋದ್ಯಮ ಇಲಾಖೆ</div>
                    <div class="brand-title" style="font-size:1.35rem; line-height:1.15;">KannadaYatra AI</div>
                    <div class="brand-subtitle" style="font-size:0.75rem; margin-top:1px;">{ui_str['brand_subtitle']}</div>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                <span style="background:#FEF3C7; color:#88131B; font-weight:800; font-size:0.72rem; padding:0.25rem 0.7rem; border-radius:20px; border:1px solid #FDE68A;">
                    {ui_str['badge_hackathon']}
                </span>
                <span style="background:#DCFCE7; color:#166534; font-weight:800; font-size:0.72rem; padding:0.25rem 0.7rem; border-radius:20px; border:1px solid #BBF7D0;">
                    {ui_str['badge_ai']}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with head_c_sos:
    st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
    with st.popover("🚨 SOS", help="Emergency Helplines (24x7)"):
        sos_t = ui_str.get("sos_title", "Emergency Tourist Helplines")
        pol_l = ui_str.get("police_helpline", "Police Emergency")
        tour_l = ui_str.get("tourist_helpline", "Karnataka Tourist Helpline")
        wom_l = ui_str.get("women_helpline", "Women Safety Helpline")
        med_l = ui_str.get("medical_helpline", "Medical / Ambulance")
        ksrtc_l = ui_str.get("ksrtc_care", "KSRTC 24x7 Passenger Care")
        kstdc_l = ui_str.get("kstdc_booking", "KSTDC Central Booking")

        st.markdown(
            f"""
            <div style="background:#FFFFFF; padding:6px; border-radius:10px; font-family:'Plus Jakarta Sans', sans-serif; min-width:260px;">
                <div style="font-size:1.02rem; font-weight:800; color:#DC2626; margin-bottom:10px; border-bottom:2px solid #FEE2E2; padding-bottom:6px;">
                    🚨 {sos_t}
                </div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; padding:7px 10px; background:#FEF2F2; border-radius:8px; border-left:4px solid #DC2626;">
                        <span style="font-weight:700; color:#1F2937; font-size:0.86rem;">👮 {pol_l}</span>
                        <a href="tel:112" style="background:#DC2626; color:#FFFFFF !important; font-weight:800; padding:4px 10px; border-radius:6px; font-size:0.85rem; text-decoration:none; display:inline-block;">112</a>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; padding:7px 10px; background:#FEF3C7; border-radius:8px; border-left:4px solid #D97706;">
                        <span style="font-weight:700; color:#1F2937; font-size:0.86rem;">🏛️ {tour_l}</span>
                        <a href="tel:1363" style="background:#D97706; color:#FFFFFF !important; font-weight:800; padding:4px 10px; border-radius:6px; font-size:0.85rem; text-decoration:none; display:inline-block;">1363</a>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; padding:7px 10px; background:#FDF2F8; border-radius:8px; border-left:4px solid #DB2777;">
                        <span style="font-weight:700; color:#1F2937; font-size:0.86rem;">👩 {wom_l}</span>
                        <a href="tel:1091" style="background:#DB2777; color:#FFFFFF !important; font-weight:800; padding:4px 10px; border-radius:6px; font-size:0.85rem; text-decoration:none; display:inline-block;">1091</a>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; padding:7px 10px; background:#ECFDF5; border-radius:8px; border-left:4px solid #059669;">
                        <span style="font-weight:700; color:#1F2937; font-size:0.86rem;">🚑 {med_l}</span>
                        <a href="tel:108" style="background:#059669; color:#FFFFFF !important; font-weight:800; padding:4px 10px; border-radius:6px; font-size:0.85rem; text-decoration:none; display:inline-block;">108</a>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; padding:7px 10px; background:#EFF6FF; border-radius:8px; border-left:4px solid #2563EB;">
                        <span style="font-weight:700; color:#1F2937; font-size:0.86rem;">🚌 {ksrtc_l}</span>
                        <a href="tel:08049596666" style="background:#2563EB; color:#FFFFFF !important; font-weight:800; padding:3px 8px; border-radius:6px; font-size:0.80rem; text-decoration:none; display:inline-block;">080-49596666</a>
                    </div>
                    <div style="display:flex; justify-content:space-between; align-items:center; padding:7px 10px; background:#F0FDFA; border-radius:8px; border-left:4px solid #0D9488;">
                        <span style="font-weight:700; color:#1F2937; font-size:0.86rem;">🏨 {kstdc_l}</span>
                        <a href="tel:08043344334" style="background:#0D9488; color:#FFFFFF !important; font-weight:800; padding:3px 8px; border-radius:6px; font-size:0.80rem; text-decoration:none; display:inline-block;">080-43344334</a>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with head_c_key:
    st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
    has_api_key = bool(get_gemini_api_key())
    if has_api_key:
        with st.popover("🟢 Gemini AI", help="Google Gemini 2.5 AI is connected and active"):
            st.markdown("<div style='color:#166534; font-weight:800; font-size:0.95rem; margin-bottom:4px;'>🟢 Google Gemini AI Active</div>", unsafe_allow_html=True)
            st.caption("Your Gemini API key is verified and powering real-time personalized synthesis.")
            cur_k = get_gemini_api_key()
            masked = cur_k[:4] + "..." + cur_k[-4:] if len(cur_k) > 8 else "***"
            st.code(f"Key: {masked}", language="text")
            new_k = st.text_input("Change Key:", type="password", key="update_key_input", placeholder="AIzaSy...")
            if st.button("Update Key", key="save_updated_key_btn", use_container_width=True):
                if new_k.strip():
                    st.session_state["gemini_api_key"] = new_k.strip()
                    os.environ["GEMINI_API_KEY"] = new_k.strip()
                    st.toast("✅ Gemini API Key updated!", icon="🔑")
                    st.rerun()
    else:
        with st.popover("🔑 Connect AI", help="Connect Google Gemini API Key for dynamic generative itineraries"):
            st.markdown("<div style='color:#88131B; font-weight:800; font-size:0.95rem; margin-bottom:4px;'>🔑 Connect Gemini AI</div>", unsafe_allow_html=True)
            st.caption("Paste your Gemini API key below to enable personalized AI synthesis right away.")
            entered_k = st.text_input("Gemini API Key:", type="password", placeholder="AIzaSy...", key="direct_api_key_input")
            if st.button("Activate AI", key="save_direct_key_btn", use_container_width=True):
                if entered_k.strip():
                    st.session_state["gemini_api_key"] = entered_k.strip()
                    os.environ["GEMINI_API_KEY"] = entered_k.strip()
                    st.toast("✅ Gemini API Key activated successfully!", icon="🎉")
                    st.rerun()
                else:
                    st.warning("Please enter a valid key.")

with head_c2:
    st.markdown("<div style='height: 2px;'></div>", unsafe_allow_html=True)
    lang_opts = ["English", "Kannada", "Hindi", "Tamil", "Telugu"]
    lang_curr_idx = lang_opts.index(cur_app_lang) if cur_app_lang in lang_opts else 0
    selected_lang = st.selectbox(
        "🌐 Language / ಭಾಷೆ",
        options=lang_opts,
        format_func=lambda l: {
            "English": "🇬🇧 English",
            "Kannada": "🇮🇳 ಕನ್ನಡ (Kannada)",
            "Hindi": "🇮🇳 हिन्दी (Hindi)",
            "Tamil": "🇮🇳 தமிழ் (Tamil)",
            "Telugu": "🇮🇳 తెలుగు (Telugu)",
        }.get(l, l),
        index=lang_curr_idx,
        key="top_app_lang_selector",
        help="Switch language for the entire app",
    )
    if selected_lang != cur_app_lang:
        st.session_state["app_lang"] = selected_lang
        st.session_state["tourist_lang"] = selected_lang
        st.rerun()

with head_c3:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button(ui_str["view_tutorial"], key="top_view_tutorial_btn", use_container_width=True, help="Revisit the onboarding tutorial and travel guide"):
        st.session_state["tutorial_completed"] = False
        st.rerun()

st.markdown("<div style='margin-bottom:1.2rem;'></div>", unsafe_allow_html=True)


def render_phrase_card(phrase, tourist_lang: str = "English") -> str:
    kn_escaped = phrase.kannada.replace("'", "\\'").replace('"', '&quot;')
    hint_html = (
        f"<div style='color:#9E1A22; font-size:0.82rem; margin-top:4px;'>📌 <i>{phrase.context_hint}</i></div>"
        if phrase.context_hint else ""
    )

    # Tailor meaning by tourist mother tongue
    if tourist_lang == "Hindi" and phrase.hindi:
        meaning_html = f"""<div style="color:#1E3A8A; font-weight:700; font-size:0.95rem; margin-top:5px;">🇮🇳 हिन्दी: {phrase.hindi}</div>
        <div style="color:#6B7280; font-size:0.82rem;">🇬🇧 English: {phrase.english}</div>"""
    elif tourist_lang == "Tamil" and phrase.tamil:
        meaning_html = f"""<div style="color:#1E3A8A; font-weight:700; font-size:0.95rem; margin-top:5px;">🇮🇳 தமிழ்: {phrase.tamil}</div>
        <div style="color:#6B7280; font-size:0.82rem;">🇬🇧 English: {phrase.english}</div>"""
    elif tourist_lang == "Telugu" and phrase.telugu:
        meaning_html = f"""<div style="color:#1E3A8A; font-weight:700; font-size:0.95rem; margin-top:5px;">🇮🇳 తెలుగు: {phrase.telugu}</div>
        <div style="color:#6B7280; font-size:0.82rem;">🇬🇧 English: {phrase.english}</div>"""
    elif tourist_lang == "Kannada":
        meaning_html = f"""<div style="color:#88131B; font-weight:700; font-size:0.95rem; margin-top:5px;">ಕನ್ನಡ: {phrase.kannada}</div>
        <div style="color:#6B7280; font-size:0.82rem;">🇬🇧 English: {phrase.english}</div>"""
    else:
        meaning_html = f"""<div style="color:#374151; font-weight:700; font-size:0.95rem; margin-top:5px;">🇬🇧 {phrase.english}</div>"""

    return f"""<div class="phrase-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:8px;">
            <div>
                <div class="kannada">{phrase.kannada}</div>
                <div class="phonetic">🗣️ {phrase.phonetic}</div>
            </div>
            <button onclick="
                if ('speechSynthesis' in window) {{
                    window.speechSynthesis.cancel();
                    var u = new SpeechSynthesisUtterance('{kn_escaped}');
                    u.lang = 'kn-IN';
                    u.rate = 0.85;
                    window.speechSynthesis.speak(u);
                }} else {{
                    alert('Audio playback not supported in this browser.');
                }}
            " class="audio-btn" title="Click to hear Kannada pronunciation aloud">
                🔊 Listen
            </button>
        </div>
        {meaning_html}
        {hint_html}
        <details style="margin-top:10px; background:#FEF3C7; border:1px solid #FDE68A; border-radius:8px; padding:6px 10px; cursor:pointer;">
            <summary style="font-size:0.78rem; font-weight:700; color:#88131B;">📱 Show Local Driver / Shopkeeper (Big Text)</summary>
            <div style="background:#FFFFFF; border-radius:6px; padding:12px; margin-top:6px; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.06);">
                <div style="font-size:1.75rem; font-weight:800; color:#88131B; font-family:'Noto Sans Kannada', sans-serif; line-height:1.3;">
                    {phrase.kannada}
                </div>
                <div style="font-size:0.92rem; font-weight:600; color:#4B5563; margin-top:4px;">
                    "{phrase.phonetic}"
                </div>
            </div>
        </details>
    </div>"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. TOP NAVIGATION BAR (WEBSITE TABS)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NAV_KEYS = [
    "explore",
    "builder",
    "itinerary",
    "survival",
    "budget",
    "culture",
    "guide",
]

def get_nav_label(key: str, lang: str) -> str:
    lang_dict = UI_LOCALIZATION.get(lang, UI_LOCALIZATION["English"])
    mapping = {
        "explore":   lang_dict.get("explore_tab", "🏠 Explore & Circuits"),
        "builder":   lang_dict.get("builder_tab", "⚙️ Custom Trip Planner"),
        "itinerary": lang_dict.get("itinerary_tab", "📍 Itinerary & Route Map"),
        "survival":  lang_dict.get("survival_tab", "🗣️ Multilingual Survival Kit"),
        "budget":    lang_dict.get("budget_tab", "💰 Budget Optimizer"),
        "culture":   lang_dict.get("culture_tab", "🎭 Cultural Explorer"),
        "guide":     lang_dict.get("guide_tab", "🧭 User Guide & Tutorial"),
    }
    return mapping.get(key, key)

curr_nav = st.session_state.get("main_nav_bar", "explore")
if curr_nav not in NAV_KEYS:
    if "itinerary" in str(curr_nav).lower():
        st.session_state["main_nav_bar"] = "itinerary"
        st.session_state["main_nav_bar_radio"] = "itinerary"
    elif "builder" in str(curr_nav).lower() or "custom" in str(curr_nav).lower():
        st.session_state["main_nav_bar"] = "builder"
    elif "survival" in str(curr_nav).lower():
        st.session_state["main_nav_bar"] = "survival"
    elif "budget" in str(curr_nav).lower():
        st.session_state["main_nav_bar"] = "budget"
    elif "culture" in str(curr_nav).lower():
        st.session_state["main_nav_bar"] = "culture"
    elif "guide" in str(curr_nav).lower():
        st.session_state["main_nav_bar"] = "guide"
    else:
        st.session_state["main_nav_bar"] = "explore"

desired_nav = st.session_state.get("main_nav_bar", "explore")
if desired_nav not in NAV_KEYS:
    desired_nav = "explore"
    st.session_state["main_nav_bar"] = "explore"

desired_idx = NAV_KEYS.index(desired_nav)

selected_nav = st.radio(
    "Main Navigation",
    options=NAV_KEYS,
    index=desired_idx,
    format_func=lambda k: get_nav_label(k, cur_app_lang),
    key="main_nav_bar_radio",
    horizontal=True,
    label_visibility="collapsed",
)
st.session_state["main_nav_bar"] = selected_nav


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1: EXPLORE & CURATED CIRCUITS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if selected_nav == "explore":
    render_hero_banner()

    # ── 1-Click Curated Circuits Showcase ──
    st.markdown(f"### {ui_str.get('popular_circuits_title', '🌟 Popular Curated Circuits (1-Click Itinerary Launchers)')}")
    st.markdown(
        f"<p style='color:#6B7280; margin-top:-0.5rem; margin-bottom:1.3rem; font-size:0.95rem;'>"
        f"{ui_str.get('popular_circuits_desc', 'Short on time? Pick an iconic, hand-crafted Karnataka route curated by local historians and food explorers. Click <b>Plan This Trip</b> to generate the complete timeline instantly.')}"
        f"</p>",
        unsafe_allow_html=True,
    )

    c_cols = st.columns(4)
    circuit_keys = list(CURATED_CIRCUITS.keys())

    for idx, c_key in enumerate(circuit_keys):
        c_info = CURATED_CIRCUITS[c_key]
        with c_cols[idx]:
            st.markdown(
                f"""<div class="circuit-card">
                    <div class="photo-header" style="background-image: url('{c_info.get('image_url', '')}'), linear-gradient(135deg, #88131B, #D97706); background-size: cover; background-position: center;">
                        <span class="badge" style="position: absolute; top: 10px; left: 10px;">{c_info['badge']}</span>
                    </div>
                    <div style="padding-top: 0.35rem;">
                        <h3 style="margin-bottom: 0.2rem;">{c_key}</h3>
                        <div class="tagline">{c_info['tagline']}</div>
                        <p>{c_info['description']}</p>
                    </div>
                    <div class="meta">
                        📍 <b>Stops:</b> {', '.join(c_info['stops'][:3])}…<br>
                        🍛 <b>Taste:</b> {c_info.get('highlight_dish', 'Regional food')}<br>
                        ⏱ <b>{c_info['days']} Days</b> · 💰 <b>{c_info['budget']}</b>
                    </div>
                </div>""",
                unsafe_allow_html=True,
            )
            if st.button(ui_str.get("plan_this_trip", "🚀 Plan This Trip"), key=f"launch_circuit_{idx}", use_container_width=True):
                with st.spinner(f"Generating {c_info['title']}…"):
                    itinerary, used_ai = generate_itinerary(
                        interests=c_info["interests"],
                        budget_tier=c_info["budget"],
                        days=c_info["days"],
                        travelers=c_info["travelers"],
                        companions=c_info["companions"],
                        fast_launch=True,
                    )
                    budget_data = compute_trip_budget(c_info["budget"], c_info["days"], c_info["travelers"])
                    st.session_state["itinerary"] = itinerary
                    st.session_state["budget_data"] = budget_data
                    st.session_state["generation_done"] = True
                    st.session_state["used_ai"] = used_ai
                    st.session_state["trip_prefs"] = {
                        "interests": c_info["interests"],
                        "budget_tier": c_info["budget"],
                        "days": c_info["days"],
                        "travelers": c_info["travelers"],
                        "companions": c_info["companions"],
                    }
                    st.session_state["main_nav_bar"] = "itinerary"
                    st.session_state["main_nav_bar_radio"] = "itinerary"
                    st.toast(f"✅ Loaded {c_info['title']}!", icon="🎉")
                    st.rerun()

    st.markdown("---")

    # ── State-level Highlight Metrics ──
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    with mcol1:
        st.markdown(
            '<div class="metric-card"><div class="value">30+</div>'
            '<div class="label">Curated Destinations</div></div>',
            unsafe_allow_html=True,
        )
    with mcol2:
        st.markdown(
            '<div class="metric-card"><div class="value">60+</div>'
            '<div class="label">Kannada Audio Phrases</div></div>',
            unsafe_allow_html=True,
        )
    with mcol3:
        st.markdown(
            '<div class="metric-card"><div class="value">10+</div>'
            '<div class="label">Living Cultural Festivals</div></div>',
            unsafe_allow_html=True,
        )
    with mcol4:
        st.markdown(
            '<div class="metric-card"><div class="value">6</div>'
            '<div class="label">Unique Culinary Regions</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Watermark-Free OpenStreetMap ──
    st.markdown("### 🗺️ Interactive Karnataka Explorer Map")
    st.caption("Explore Karnataka's top destinations. Click any marker to view entry fees, historical relevance, and secret local eateries.")

    m = folium.Map(location=[14.2, 75.8], zoom_start=7, tiles="OpenStreetMap")
    for dest in KARNATAKA_DESTINATIONS.values():
        color = "red" if "Heritage" in dest.categories else \
                "green" if "Nature" in dest.categories else \
                "orange" if "Food" in dest.categories else "blue"

        popup_content = f"""
        <div style='font-family: sans-serif; font-size:12px; width:220px;'>
            <b style='color:#9E1A22; font-size:14px;'>{dest.name}</b><br>
            <span style='color:#666;'>{dest.region} • {', '.join(dest.categories)}</span>
            <hr style='margin:5px 0;'>
            <p style='margin:4px 0;'>{dest.description[:110]}…</p>
            <b>⭐ Highlight:</b> {dest.highlights[0] if dest.highlights else 'Scenic'}<br>
            <b>🍛 Secret Food:</b> {dest.secret_eatery[:55] if dest.secret_eatery else 'Local food'}<br>
            <b>⏱ Visit:</b> {dest.time_needed_hrs} hrs · <b>🎫:</b> {'₹' + str(dest.entry_fee_inr) if dest.entry_fee_inr > 0 else 'Free'}
        </div>
        """
        folium.CircleMarker(
            location=[dest.lat, dest.lon],
            radius=8,
            popup=folium.Popup(popup_content, max_width=250),
            tooltip=f"{dest.name} ({dest.region})",
            color=color,
            fill=True,
            fill_opacity=0.85,
        ).add_to(m)

    st_folium(m, width=1150, height=520, returned_objects=[])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2: CUSTOM TRIP PLANNER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif selected_nav == "builder":
    st.markdown("## ⚙️ Custom Trip Planner")
    st.markdown(
        "<p style='color:#6B7280; font-size:0.95rem; margin-top:-0.5rem;'>"
        "Customize every parameter of your trip. Our dual-engine AI will synthesize a balanced, "
        "geographically logical itinerary tailored to your group size and budget."
        "</p>",
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown('<div class="builder-card">', unsafe_allow_html=True)
        st.markdown("<h3>🎯 1. Select Interests & Duration</h3>", unsafe_allow_html=True)

        col_b1, col_b2 = st.columns([3, 2])
        with col_b1:
            interests_input = st.multiselect(
                "Your Interests (Select 1 or more)",
                options=["Heritage", "Nature", "Food", "Adventure"],
                default=st.session_state.get("trip_prefs", {}).get("interests", ["Heritage", "Food"]),
                help="Shapes the primary theme and destinations chosen for your route.",
            )
        with col_b2:
            days_input = st.slider(
                "Trip Duration (Days)",
                min_value=1,
                max_value=14,
                value=st.session_state.get("trip_prefs", {}).get("days", 3),
                help="How many travel days will your trip last?",
            )

        st.markdown("<hr style='margin:1.2rem 0; border:none; border-top:1px solid #EFE8DE;'>", unsafe_allow_html=True)
        st.markdown("<h3>💰 2. Budget Level & Group Size</h3>", unsafe_allow_html=True)

        col_b3, col_b4, col_b5 = st.columns(3)
        with col_b3:
            budget_input = st.radio(
                "Budget Tier",
                options=["Budget", "Mid-range", "Luxury"],
                index=["Budget", "Mid-range", "Luxury"].index(
                    st.session_state.get("trip_prefs", {}).get("budget_tier", "Mid-range")
                ),
                horizontal=True,
                help="Budget: ₹1.5K-3K/day · Mid-range: ₹4K-8K/day · Luxury: ₹10K-25K/day",
            )
        with col_b4:
            travelers_input = st.number_input(
                "Number of Travelers",
                min_value=1,
                max_value=20,
                value=st.session_state.get("trip_prefs", {}).get("travelers", 2),
            )
        with col_b5:
            companions_input = st.selectbox(
                "Companions",
                options=["Solo", "Couple", "Family with Kids", "Friends Group", "Business Trip"],
                index=["Solo", "Couple", "Family with Kids", "Friends Group", "Business Trip"].index(
                    st.session_state.get("trip_prefs", {}).get("companions", "Friends Group")
                ),
            )

        st.markdown("<hr style='margin:1.4rem 0; border:none; border-top:1px solid #EFE8DE;'>", unsafe_allow_html=True)

        btn_c1, btn_c2, btn_c3 = st.columns([2, 1, 3])
        with btn_c1:
            plan_clicked = st.button("🚀 Generate My Personalized Itinerary", use_container_width=True, type="primary")
        with btn_c2:
            if st.button("🔄 Reset Form", use_container_width=True):
                reset_session_state()
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    if plan_clicked:
        if not interests_input:
            st.error("⚠️ Please select at least one interest category!")
        else:
            with st.spinner("🧠 Crafting your tailored Karnataka itinerary…"):
                itinerary, used_ai = generate_itinerary(
                    interests=interests_input,
                    budget_tier=budget_input,
                    days=days_input,
                    travelers=travelers_input,
                    companions=companions_input,
                )
                budget_data = compute_trip_budget(budget_input, days_input, travelers_input)

                st.session_state["itinerary"] = itinerary
                st.session_state["budget_data"] = budget_data
                st.session_state["generation_done"] = True
                st.session_state["used_ai"] = used_ai
                st.session_state["trip_prefs"] = {
                    "interests": interests_input,
                    "budget_tier": budget_input,
                    "days": days_input,
                    "travelers": travelers_input,
                    "companions": companions_input,
                }
                st.session_state["main_nav_bar"] = "itinerary"
                st.session_state["main_nav_bar_radio"] = "itinerary"
                st.toast("🎉 Custom Itinerary generated!", icon="📍")
                st.rerun()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3: ITINERARY & ROUTE MAP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif selected_nav == "itinerary":
    if not st.session_state.get("generation_done") or st.session_state.get("itinerary") is None:
        st.info("💡 No itinerary generated yet. Choose a preset from **'Explore & Circuits'** or customize one in **'Custom Trip Planner'**!")
    else:
        raw_itin: Itinerary = st.session_state["itinerary"]
        itin: Itinerary = localize_itinerary(raw_itin, cur_app_lang)
        budget_d = st.session_state["budget_data"]

        # Engine indicator
        has_ai_key = bool(get_gemini_api_key())
        if st.session_state.get("used_ai"):
            st.success(ui_str.get("status_ai_generated", "✨ Itinerary generated using **Google Gemini AI** - personalized for your group!"))
        elif has_ai_key:
            col_stat1, col_stat2 = st.columns([3.2, 1.2])
            with col_stat1:
                st.info(ui_str.get("status_curated_with_ai_ready", "⚡ **Verified Regional Ground Truth Engine Active** · 100% verified route."))
            with col_stat2:
                if st.button(ui_str.get("resynthesize_btn", "✨ Re-synthesize with Gemini AI"), key="resynthesize_ai_btn", use_container_width=True):
                    prefs = st.session_state.get("trip_prefs", {})
                    with st.spinner("Re-synthesizing itinerary with Google Gemini AI..."):
                        new_itin, ai_ok = generate_itinerary(
                            interests=prefs.get("interests", ["Heritage", "Food"]),
                            budget_tier=prefs.get("budget_tier", "Mid-range"),
                            days=prefs.get("days", 3),
                            travelers=prefs.get("travelers", 2),
                            companions=prefs.get("companions", "Friends"),
                            fast_launch=False,
                            language=cur_app_lang,
                        )
                        if ai_ok and new_itin:
                            st.session_state["itinerary"] = new_itin
                            st.session_state["used_ai"] = True
                            st.toast("✅ Re-synthesized with Google Gemini AI!", icon="✨")
                            st.rerun()
        else:
            st.info(ui_str.get("status_curated_active", "⚡ **Verified Regional Ground Truth Database Active** · 100% verified Karnataka circuits and logistics."))

        st.markdown(f"## {itin.trip_title}")
        if itin.overview:
            st.markdown(f"<p style='color:#4B5563; font-size:1.05rem; line-height:1.6;'><i>{itin.overview}</i></p>", unsafe_allow_html=True)

        st.markdown("---")

        # ── Trip summary metrics ──
        all_destinations = set()
        for day in itin.days:
            for slot in day.slots:
                if slot.destination:
                    all_destinations.add(slot.destination)

        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1:
            st.metric(ui_str.get("total_days", "📅 Total Days"), len(itin.days))
        with mc2:
            st.metric(ui_str.get("destinations_count", "📍 Destinations"), len(all_destinations))
        with mc3:
            st.metric(ui_str.get("travelers_count", "👥 Travelers"), itin.num_travelers)
        with mc4:
            st.metric(ui_str.get("budget_tier_label", "💰 Budget Tier"), itin.budget_tier)

        st.markdown("---")

        # ── Route Map ──
        st.markdown(f"### {ui_str.get('interactive_map_title', '🗺️ Interactive Travel Route')}")
        st.caption(ui_str.get("interactive_map_caption", "Visual travel route connecting all scheduled stops in chronological order."))

        route_map = folium.Map(location=[14.0, 76.0], zoom_start=7, tiles="OpenStreetMap")
        route_coords = []
        for day in itin.days:
            for slot in day.slots:
                dest = KARNATAKA_DESTINATIONS.get(slot.destination)
                if dest:
                    route_coords.append([dest.lat, dest.lon])
                    folium.Marker(
                        location=[dest.lat, dest.lon],
                        popup=f"<b>Day {day.day_number}: {slot.activity}</b><br>{slot.description[:100]}",
                        tooltip=f"Day {day.day_number}: {dest.name}",
                        icon=folium.Icon(color="red", icon="info-sign"),
                    ).add_to(route_map)

        if len(route_coords) > 1:
            unique_coords = [route_coords[0]]
            for c in route_coords[1:]:
                if c != unique_coords[-1]:
                    unique_coords.append(c)
            if len(unique_coords) > 1:
                folium.PolyLine(
                    unique_coords,
                    weight=4,
                    color="#9E1A22",
                    opacity=0.85,
                    dash_array="8",
                ).add_to(route_map)
        if route_coords:
            route_map.fit_bounds(route_coords)

        st_folium(route_map, width=1150, height=440, returned_objects=[])

        # ── Official Booking Bar ──
        st.markdown(
            f"""
            <div class="booking-cta-bar">
                <div>
                    <div class="title">{ui_str.get('booking_cta_title', '🎟️ Ready to Book Your Karnataka Experience?')}</div>
                    <div class="desc">{ui_str.get('booking_cta_desc', 'Lock in verified government transportation, jungle safari permits, and heritage packages directly:')}</div>
                </div>
                <div style="display:flex; gap:0.6rem; flex-wrap:wrap;">
                    <a href="https://kstdc.co" target="_blank" class="booking-btn">🏛️ KSTDC Tours</a>
                    <a href="https://www.ksrtc.in" target="_blank" class="booking-btn" style="background:#9E1A22; color:white !important;">🚌 KSRTC Airavat</a>
                    <a href="https://www.irctc.co.in" target="_blank" class="booking-btn" style="background:#0F766E; color:white !important;">🚆 Vande Bharat</a>
                    <a href="https://karnatakaecotourism.com" target="_blank" class="booking-btn" style="background:#7C2D12; color:white !important;">🌿 Safari & Trek</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # ── Day-by-Day Timeline ──
        st.markdown(f"### {ui_str.get('day_timeline_title', '📅 Day-by-Day Detailed Timeline')}")

        day_prefix = ui_str.get("day_prefix", "Day")
        overnight_prefix = ui_str.get("overnight_prefix", "🏨 Overnight:")
        highlights_prefix = ui_str.get("highlights_prefix", "✨ Highlights:")
        food_prefix = ui_str.get("local_secret", "🍛 Local Food Secret")
        timing_prefix = ui_str.get("optimal_timing", "⏰ Optimal Timing")
        transit_prefix = ui_str.get("transit_tip", "🚌 Transit Tip")

        for day in itin.days:
            st.markdown(
                f'<div class="day-header">{day_prefix} {day.day_number} - {day.title} '
                f'<span style="font-size:0.85rem; opacity:0.9; font-weight:600;">'
                f'{overnight_prefix} {day.overnight_stay}</span></div>',
                unsafe_allow_html=True,
            )

            if day.day_highlights:
                highlight_str = " · ".join(f"✦ {h}" for h in day.day_highlights)
                st.caption(f"{highlights_prefix} {highlight_str}")

            for slot in day.slots:
                dest_meta = KARNATAKA_DESTINATIONS.get(slot.destination)
                dest_img_url = get_destination_image(dest_meta.name if dest_meta else slot.destination)
                img_tag = f"""<img src="{dest_img_url}" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1609766857041-ed402ea8069a?auto=format&fit=crop&w=650&q=80';" style="width:72px; height:72px; object-fit:cover; border-radius:10px; float:left; margin-right:14px; margin-bottom:6px; box-shadow:0 2px 8px rgba(0,0,0,0.12); border:1px solid #E5E7EB; background:#88131B;" />"""
                secret_food = f"<div style='color:#9E1A22; font-size:0.85rem; margin-top:3px;'><b>{food_prefix}:</b> {dest_meta.secret_eatery}</div>" if dest_meta and dest_meta.secret_eatery else ""
                golden_hour = f"<div style='color:#B45309; font-size:0.85rem; margin-top:3px;'><b>{timing_prefix}:</b> {dest_meta.best_time_of_day}</div>" if dest_meta and dest_meta.best_time_of_day else ""
                crowd_note = f"<span style='float:right; font-size:0.75rem; background:#FEF3C7; color:#92400E; padding:2px 8px; border-radius:12px; font-weight:700;'>👥 {dest_meta.crowd_level}</span>" if dest_meta else ""
                transit_note = f"<div style='color:#1E3A8A; font-size:0.82rem; margin-top:2px;'><b>{transit_prefix}:</b> {dest_meta.transit_tip}</div>" if dest_meta and dest_meta.transit_tip else ""

                st.markdown(
                    f"""<div class="timeline-item" style="overflow:hidden;">
                        {img_tag}
                        <div>
                            <span class="time-badge">{slot.time}</span> <b>{slot.activity}</b>
                            <span style="color:#6B7280; font-size:0.85rem;">({slot.duration_hrs}h)</span>
                            {crowd_note}
                            <div style="color:#374151; margin-top:6px; font-size:0.92rem; line-height:1.5;">{slot.description}</div>
                            {"<div style='color:#0F766E; font-size:0.85rem; margin-top:4px;'>💡 <i>" + slot.travel_tip + "</i></div>" if slot.travel_tip else ""}
                            {golden_hour}
                            {secret_food}
                            {transit_note}
                        </div>
                    </div>""",
                    unsafe_allow_html=True,
                )

        st.markdown("---")

        # ── Pro Tips & Export ──
        col_p1, col_p2 = st.columns([2, 1])
        with col_p1:
            if itin.pro_tips:
                st.markdown(f"### {ui_str.get('pro_tips_title', '💡 Local Expert Pro-Tips')}")
                for tip in itin.pro_tips:
                    st.markdown(f"- {tip}")

        with col_p2:
            st.markdown("### 📱 Export Travel Pass")
            summary_text = f"🏛️ KannadaYatra AI Travel Pass\n"
            summary_text += f"Trip: {itin.trip_title}\n"
            summary_text += f"Duration: {len(itin.days)} Days | Budget: {itin.budget_tier}\n\n"
            for day in itin.days:
                summary_text += f"Day {day.day_number}: {day.title} (Stay: {day.overnight_stay})\n"
                for s in day.slots[:3]:
                    summary_text += f"- {s.time}: {s.activity}\n"
                summary_text += "\n"
            summary_text += "🚨 Karnataka 24x7 Helplines:\n"
            summary_text += "- Police: 112\n- KSTDC Tourism: 1363 / 080-43344334\n- KSRTC: 080-49596666\n"

            st.download_button(
                "📥 Download Travel Pass (.txt)",
                data=summary_text,
                file_name="KannadaYatra_Travel_Pass.txt",
                mime="text/plain",
                use_container_width=True,
            )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4: MULTILINGUAL KANNADA SURVIVAL KIT & COMMUNICATION CENTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif selected_nav == "survival":
    st.markdown("## 🗣️ Multilingual Tourist Communication Center & Survival Kit")
    st.markdown(
        "<p style='color:#6B7280; font-size:1.02rem; margin-top:-0.5rem;'>"
        "Bridging communication across <b>Kannada, Hindi, Tamil, Telugu, and English</b>. "
        "Learn essential travel phrases, hear authentic native pronunciation, or show high-contrast cards directly to auto drivers and local vendors."
        "</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # Native Language Selector for Tourist
    mother_tongue = st.radio(
        "🌐 Choose Your Native Language / Mother Tongue (for translations & phonetic guidance):",
        options=["English", "Hindi", "Tamil", "Telugu", "Kannada"],
        format_func=lambda l: {
            "English": "🇬🇧 English",
            "Hindi": "🇮🇳 हिन्दी (Hindi)",
            "Tamil": "🇮🇳 தமிழ் (Tamil)",
            "Telugu": "🇮🇳 తెలుగు (Telugu)",
            "Kannada": "🇮🇳 ಕನ್ನಡ (Kannada)",
        }.get(l, l),
        index=["English", "Hindi", "Tamil", "Telugu", "Kannada"].index(st.session_state.get("tourist_lang", "English")),
        horizontal=True,
        key="tourist_mother_tongue_radio",
    )
    st.session_state["tourist_lang"] = mother_tongue

    # Live Cross-Lingual Search & Quick Translator
    search_col1, search_col2 = st.columns([3.5, 1.2])
    with search_col1:
        search_kw = st.text_input(
            "🔍 Quick Translator & Search across all 5 languages:",
            placeholder="Type any word (e.g. 'water', 'pani', 'thanni', 'neellu', 'coffee', 'dosa', 'auto', 'meter', 'cost', 'kitna', 'evvalavu', 'enta')...",
            key="phrase_live_search",
        )
    with search_col2:
        st.markdown("<div style='height:28px;'></div>", unsafe_allow_html=True)
        if search_kw and st.button("❌ Clear Search", use_container_width=True):
            st.session_state["phrase_live_search"] = ""
            st.rerun()

    if search_kw:
        matches = search_travel_phrases(search_kw)
        if matches:
            st.success(f"🎯 Found {len(matches)} matching travel phrase(s) for **'{search_kw}'**:")
            cols = st.columns(2)
            for i, m in enumerate(matches):
                with cols[i % 2]:
                    st.markdown(render_phrase_card(m, tourist_lang=mother_tongue), unsafe_allow_html=True)
        else:
            st.info(f"💡 No exact phrase found for '{search_kw}'. Try browsing the full categories below!")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # 3 Sub-tabs: Categories, Scenarios, Basics
    sub_phrases, sub_scenarios, sub_basics = st.tabs([
        "📚 Essential Phrases (51)",
        "🎭 Real-World Roleplay Dialogues (4)",
        "🔤 Numbers, Road Signs & Etiquette",
    ])

    with sub_phrases:
        col_s1, col_s2 = st.columns([2, 3])
        with col_s1:
            available_dests = []
            if st.session_state.get("itinerary"):
                for d in st.session_state["itinerary"].days:
                    for s in d.slots:
                        if s.destination and s.destination not in available_dests:
                            available_dests.append(s.destination)
            if not available_dests:
                available_dests = list(KARNATAKA_DESTINATIONS.keys())[:8]

            selected_dest_phrase = st.selectbox(
                "🏛️ Filter by Trip Destination",
                options=available_dests,
            )

        with col_s2:
            phrase_view = st.radio(
                "Catalog Filter",
                options=["By Selected Destination", "Full State Phrase Book"],
                horizontal=True,
            )

        if phrase_view == "By Selected Destination":
            ctx = get_full_cultural_context(selected_dest_phrase)
            st.markdown(f"### Location-Tied Phrases for **{selected_dest_phrase}**")
            for cat_name, p_list in ctx.survival_phrases.items():
                with st.expander(f"{cat_name} ({len(p_list)} phrases)", expanded=True):
                    pcols = st.columns(2)
                    for idx, p in enumerate(p_list):
                        with pcols[idx % 2]:
                            st.markdown(render_phrase_card(p, tourist_lang=mother_tongue), unsafe_allow_html=True)
        else:
            st.markdown("### 📖 Complete 51-Phrase Karnataka Travel Phrasebook")
            for cat_name, p_list in PHRASE_CATEGORIES.items():
                with st.expander(f"{cat_name} ({len(p_list)} phrases)", expanded=False):
                    pcols = st.columns(2)
                    for idx, p in enumerate(p_list):
                        with pcols[idx % 2]:
                            st.markdown(render_phrase_card(p, tourist_lang=mother_tongue), unsafe_allow_html=True)

    with sub_scenarios:
        st.markdown("### 🎭 Interactive Practical Dialogues for Karnataka Travel")
        st.markdown(
            "<p style='color:#6B7280; font-size:0.92rem; margin-top:-0.5rem;'>"
            "Step through multi-turn conversations you will actually experience on the street. "
            "Listen to each line aloud and read the native translation in your mother tongue."
            "</p>",
            unsafe_allow_html=True,
        )

        for sc in TRAVEL_SCENARIOS:
            with st.expander(f"{sc.icon} **{sc.title}** ({sc.location})", expanded=True):
                st.caption(f"📌 Scenario Context: {sc.description}")
                for turn in sc.turns:
                    is_tourist = "tourist" in turn.speaker.lower()
                    card_bg = "#EFF6FF" if is_tourist else "#FFFBEB"
                    card_border = "#BFDBFE" if is_tourist else "#FDE68A"
                    badge_bg = "#2563EB" if is_tourist else "#D97706"
                    badge_title = "Tourist (You)" if is_tourist else turn.speaker

                    # Meaning in mother tongue
                    meaning_line = turn.english
                    if mother_tongue == "Hindi" and turn.hindi:
                        meaning_line = f"🇮🇳 {turn.hindi} <span style='color:#6B7280; font-size:0.82rem;'>(EN: {turn.english})</span>"
                    elif mother_tongue == "Tamil" and turn.tamil:
                        meaning_line = f"🇮🇳 {turn.tamil} <span style='color:#6B7280; font-size:0.82rem;'>(EN: {turn.english})</span>"
                    elif mother_tongue == "Telugu" and turn.telugu:
                        meaning_line = f"🇮🇳 {turn.telugu} <span style='color:#6B7280; font-size:0.82rem;'>(EN: {turn.english})</span>"

                    kn_escaped = turn.kannada.replace("'", "\\'").replace('"', '&quot;')
                    tip_box = f"<div style='margin-top:6px; color:#9E1A22; font-size:0.82rem; background:rgba(255,255,255,0.7); padding:4px 8px; border-radius:6px;'>💡 <b>Pro-Tip:</b> {turn.tip}</div>" if turn.tip else ""

                    st.markdown(
                        f"""<div style="background:{card_bg}; border:1px solid {card_border}; border-radius:12px; padding:12px 16px; margin-bottom:10px;">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                                <span style="background:{badge_bg}; color:#FFFFFF; font-weight:800; font-size:0.75rem; padding:2px 10px; border-radius:12px;">{badge_title}</span>
                                <button onclick="
                                    if ('speechSynthesis' in window) {{
                                        window.speechSynthesis.cancel();
                                        var u = new SpeechSynthesisUtterance('{kn_escaped}');
                                        u.lang = 'kn-IN';
                                        u.rate = 0.85;
                                        window.speechSynthesis.speak(u);
                                    }}
                                " style="background:#88131B; color:#FFFFFF; border:none; border-radius:8px; padding:3px 10px; font-size:0.75rem; font-weight:700; cursor:pointer;">
                                    🔊 Play
                                </button>
                            </div>
                            <div style="font-size:1.15rem; font-weight:800; color:#88131B; font-family:'Noto Sans Kannada', sans-serif;">{turn.kannada}</div>
                            <div style="font-size:0.88rem; font-weight:600; color:#4B5563; margin-top:2px;">🗣️ {turn.phonetic}</div>
                            <div style="margin-top:4px; font-size:0.92rem; color:#1F2937;">{meaning_line}</div>
                            {tip_box}
                        </div>""",
                        unsafe_allow_html=True,
                    )

    with sub_basics:
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            st.markdown("### 🔢 Kannada Numbers (1 to 10)")
            numbers_data = [
                ("1", "ಒಂದು", "Ondu", "One", "एक (Ek)", "ஒன்று (Ondru)", "ఒకటి (Okati)"),
                ("2", "ಎರಡು", "Eraḍu", "Two", "दो (Do)", "இரண்டு (Irandu)", "రెండు (Rendu)"),
                ("3", "ಮೂರು", "Mūru", "Three", "तीन (Teen)", "மூன்று (Moondru)", "మూడు (Moodu)"),
                ("4", "ನಾಲ್ಕು", "Nālku", "Four", "चार (Chaar)", "நான்கு (Naangu)", "నాలుగు (Naalugu)"),
                ("5", "ಐದು", "Aidu", "Five", "पाँच (Paanch)", "ஐந்து (Ainthu)", "ఐదు (Aidu)"),
                ("6", "ಆರು", "Āru", "Six", "छह (Chhah)", "ஆறு (Aaru)", "ఆరు (Aaru)"),
                ("7", "ಏಳು", "Ēḷu", "Seven", "सात (Saat)", "ஏழு (Ezhu)", "ఏడు (Eedu)"),
                ("8", "ಎಂಟು", "Enṭu", "Eight", "आठ (Aath)", "எட்டு (Ettu)", "ఎనిమిది (Enimidi)"),
                ("9", "ಒಂಬತ್ತು", "Ombattu", "Nine", "नौ (Nau)", "ஒன்பது (Onpathu)", "తొమ్మిది (Tommidi)"),
                ("10", "ಹತ್ತು", "Hattu", "Ten", "दस (Das)", "பத்து (Pathu)", "పది (Padi)"),
            ]
            st.markdown(
                """<table style="width:100%; border-collapse:collapse; background:#FFFFFF; border-radius:10px; overflow:hidden; border:1px solid #E5E7EB; font-size:0.88rem;">
                    <thead style="background:#88131B; color:#FFFFFF;">
                        <tr><th style="padding:6px;">#</th><th style="padding:6px;">Kannada</th><th style="padding:6px;">Phonetic</th><th style="padding:6px;">English</th><th style="padding:6px;">Hindi</th><th style="padding:6px;">Tamil</th><th style="padding:6px;">Telugu</th></tr>
                    </thead>
                    <tbody>""" + "".join(
                    f"<tr style='border-bottom:1px solid #F3F4F6; text-align:center;'><td style='padding:6px; font-weight:700;'>{r[0]}</td><td style='padding:6px; font-weight:800; color:#88131B;'>{r[1]}</td><td style='padding:6px;'>{r[2]}</td><td style='padding:6px;'>{r[3]}</td><td style='padding:6px;'>{r[4]}</td><td style='padding:6px;'>{r[5]}</td><td style='padding:6px;'>{r[6]}</td></tr>"
                    for r in numbers_data
                ) + """</tbody></table>""",
                unsafe_allow_html=True,
            )

        with b_col2:
            st.markdown("### 🪧 Common Street & Station Signboards")
            signs_data = [
                ("ಪ್ರವೇಶ", "Pravēsha", "Entry / Entrance", "प्रवेश", "நுழைவாயில்", "ప్రవేశం"),
                ("ನಿರ್ಗಮನ", "Nirgamana", "Exit", "निकास", "வெளியேறும் வழி", "నిష్క్రమణ"),
                ("ಶೌಚಾಲಯ", "Shauchālaya", "Restroom / Toilet", "शौचालय", "கழிப்பறை", "మరుగుదొడ్డి"),
                ("ಕುಡಿಯುವ ನೀರು", "Kuḍiyuva Nīru", "Drinking Water", "पीने का पानी", "குடிநீர்", "త్రాగునీరు"),
                ("ನಿಲುಗಡೆ", "Nilugaḍe", "Bus / Taxi Stop", "स्टॉप / ठहराव", "நிறுத்தம்", "స్టాప్"),
                ("ಉಚಿತ", "Uchita", "Free (No fee)", "मुफ़्त", "இலவசம்", "ఉచితం"),
                ("ಶುಲ್ಕ", "Shulka", "Entry Fee / Charge", "शुल्क", "கட்டணம்", "రుసుము"),
            ]
            st.markdown(
                """<table style="width:100%; border-collapse:collapse; background:#FFFFFF; border-radius:10px; overflow:hidden; border:1px solid #E5E7EB; font-size:0.88rem;">
                    <thead style="background:#D97706; color:#FFFFFF;">
                        <tr><th style="padding:6px;">Signboard</th><th style="padding:6px;">Phonetic</th><th style="padding:6px;">English</th><th style="padding:6px;">Hindi</th><th style="padding:6px;">Tamil</th><th style="padding:6px;">Telugu</th></tr>
                    </thead>
                    <tbody>""" + "".join(
                    f"<tr style='border-bottom:1px solid #F3F4F6; text-align:center;'><td style='padding:6px; font-weight:800; color:#88131B;'>{s[0]}</td><td style='padding:6px;'>{s[1]}</td><td style='padding:6px; font-weight:700;'>{s[2]}</td><td style='padding:6px;'>{s[3]}</td><td style='padding:6px;'>{s[4]}</td><td style='padding:6px;'>{s[5]}</td></tr>"
                    for s in signs_data
                ) + """</tbody></table>""",
                unsafe_allow_html=True,
            )

            st.markdown("---")
            st.markdown("### 🛕 Cultural Etiquette for Travelers")
            st.markdown(
                """
                - 👟 **Footwear:** Always remove shoes before entering temple premises and sanctums. Dedicated free shoe counters are available.
                - 🙏 **Greeting:** Use **'Namaskāra'** with hands folded. It expresses deep respect and warms hearts everywhere.
                - 🍛 **Dining:** When receiving prasada or food, always accept with your **right hand**.
                - 📷 **Photography:** Taking photos of sanctum sanctorum deities is strictly prohibited; temple architecture and outer corridors are usually fine.
                """
            )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 5: BUDGET TRACKER & OPTIMIZER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif selected_nav == "budget":
    st.markdown("## 💰 Smart Budget Tracker & Optimizer")
    st.markdown(
        "<p style='color:#6B7280; font-size:0.95rem; margin-top:-0.5rem;'>"
        "Accurate financial forecasting calibrated specifically to Karnataka pricing across KSRTC transport, "
        "darshini eateries, and heritage accommodations."
        "</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    budget_info = st.session_state.get("budget_data")
    if not budget_info:
        # Provide default mid-range 3-day projection if none generated
        budget_info = compute_trip_budget("Mid-range", 3, 2)
        st.info("Showing default 3-day Mid-range budget estimate. Generate an itinerary to see your exact trip budget.")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f'<div class="metric-card"><div class="value">{format_inr(budget_info["total_min"])}</div>'
            f'<div class="label">Estimated Minimum</div></div>',
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f'<div class="metric-card"><div class="value" style="color:#0F766E;">{format_inr(budget_info["total_avg"])}</div>'
            f'<div class="label">Expected Average</div></div>',
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f'<div class="metric-card"><div class="value" style="color:#B81D24;">{format_inr(budget_info["total_max"])}</div>'
            f'<div class="label">Maximum Estimated Budget</div></div>',
            unsafe_allow_html=True,
        )

    st.caption(
        f"📊 Projection for **{budget_info['travelers']} traveler(s)** · **{budget_info['days']} days** · **{budget_info['tier']}** tier"
    )
    st.markdown("---")

    daily_df = budget_info["daily"]
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig_donut = px.pie(
            daily_df,
            values="avg_cost",
            names="category",
            title="Daily Spend Distribution",
            hole=0.45,
            color_discrete_sequence=["#9E1A22", "#E67E22", "#F59E0B", "#0F766E", "#3B82F6"],
        )
        fig_donut.update_traces(textinfo="percent+label", textposition="outside")
        fig_donut.update_layout(
            showlegend=False,
            margin=dict(t=50, b=20, l=20, r=20),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with chart_col2:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name="Min", x=daily_df["category"], y=daily_df["min_cost"], marker_color="#86EFAC"))
        fig_bar.add_trace(go.Bar(name="Avg", x=daily_df["category"], y=daily_df["avg_cost"], marker_color="#F59E0B"))
        fig_bar.add_trace(go.Bar(name="Max", x=daily_df["category"], y=daily_df["max_cost"], marker_color="#F87171"))
        fig_bar.update_layout(
            title="Daily Cost Category Breakdown (₹)",
            barmode="group",
            xaxis_title="Category",
            yaxis_title="Cost (₹)",
            margin=dict(t=50, b=20, l=20, r=20),
            height=380,
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # ── Cumulative Projection ──
    st.markdown("### 📈 Cumulative Trip Spend Projection")
    trip_days_range = list(range(1, budget_info["days"] + 1))
    cumulative_min = [daily_df["min_cost"].sum() * d for d in trip_days_range]
    cumulative_avg = [daily_df["avg_cost"].sum() * d for d in trip_days_range]
    cumulative_max = [daily_df["max_cost"].sum() * d for d in trip_days_range]

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=trip_days_range, y=cumulative_min, mode="lines+markers", name="Min Budget", line=dict(color="#10B981", width=2)))
    fig_line.add_trace(go.Scatter(x=trip_days_range, y=cumulative_avg, mode="lines+markers", name="Expected", line=dict(color="#F59E0B", width=3)))
    fig_line.add_trace(go.Scatter(x=trip_days_range, y=cumulative_max, mode="lines+markers", name="Max Ceiling", line=dict(color="#EF4444", width=2, dash="dash")))
    fig_line.update_layout(
        xaxis_title="Trip Day",
        yaxis_title="Cumulative Cost (₹)",
        margin=dict(t=30, b=20, l=20, r=20),
        height=320,
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_line, use_container_width=True)

    # ── Saving Tips ──
    st.markdown("### 💡 Smart Money-Saving Tips for Karnataka")
    tips = budget_saving_tips(budget_info["tier"])
    for tip in tips:
        st.markdown(f"- {tip}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 6: REGIONAL CULTURAL EXPLORER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif selected_nav == "culture":
    st.markdown("## 🎭 Regional Cultural Explorer")
    st.markdown(
        "<p style='color:#6B7280; font-size:0.95rem; margin-top:-0.5rem;'>"
        "Deep-dive into culinary traditions, living festivals, and heritage stories tied directly to Karnataka's distinct regions."
        "</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    all_dests_culture = list(KARNATAKA_DESTINATIONS.keys())
    culture_dest = st.selectbox("🏛️ Select Karnataka Destination", options=all_dests_culture, key="culture_select")

    context = get_full_cultural_context(culture_dest)
    dest_obj = KARNATAKA_DESTINATIONS.get(culture_dest)

    if dest_obj:
        dest_img = get_destination_image(culture_dest)
        st.markdown(
            f"""<div style="margin: 0.8rem 0 1.2rem 0; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 18px rgba(0,0,0,0.08); border: 1.5px solid #E5E7EB; background: #ffffff;">
<div style="height: 230px; background-image: url('{dest_img}'), linear-gradient(135deg, #7A0C16, #D97706); background-size: cover; background-position: center; position: relative;">
<span style="position: absolute; top: 12px; left: 14px; background: rgba(0,0,0,0.65); backdrop-filter: blur(6px); color: #FFFFFF; font-weight: 800; font-size: 0.82rem; padding: 0.35rem 0.85rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.4);">
📍 {dest_obj.region}
</span>
<span style="position: absolute; bottom: 14px; left: 14px; background: rgba(136,19,27,0.88); backdrop-filter: blur(6px); color: #FFFFFF; font-weight: 800; font-size: 1.25rem; padding: 0.45rem 1.1rem; border-radius: 10px; border: 1px solid rgba(255,255,255,0.3); text-shadow: 0 1px 3px rgba(0,0,0,0.4);">
🏛️ {culture_dest}
</span>
</div>
</div>""",
            unsafe_allow_html=True,
        )

        ib1, ib2, ib3 = st.columns(3)
        with ib1:
            st.markdown(
                f"""<div style="background:#FFFBEB; border:1px solid #FED7AA; border-radius:10px; padding:0.8rem; text-align:center;">
                    <div style="font-size:0.8rem; color:#B45309; font-weight:700;">⏰ BEST VISIT WINDOW</div>
                    <div style="font-size:0.9rem; font-weight:600; color:#1F2937; margin-top:3px;">{dest_obj.best_time_of_day or 'Morning hours'}</div>
                </div>""",
                unsafe_allow_html=True,
            )
        with ib2:
            st.markdown(
                f"""<div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:10px; padding:0.8rem; text-align:center;">
                    <div style="font-size:0.8rem; color:#DC2626; font-weight:700;">👥 CROWD LEVEL</div>
                    <div style="font-size:0.9rem; font-weight:600; color:#1F2937; margin-top:3px;">{dest_obj.crowd_level}</div>
                </div>""",
                unsafe_allow_html=True,
            )
        with ib3:
            st.markdown(
                f"""<div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:10px; padding:0.8rem; text-align:center;">
                    <div style="font-size:0.8rem; color:#16A34A; font-weight:700;">🚌 TRANSIT TIP</div>
                    <div style="font-size:0.85rem; font-weight:600; color:#1F2937; margin-top:3px;">{dest_obj.transit_tip[:45] + '…' if len(dest_obj.transit_tip) > 45 else dest_obj.transit_tip or 'Highway connected'}</div>
                </div>""",
                unsafe_allow_html=True,
            )

        if dest_obj.secret_eatery:
            st.markdown(
                f"""<div style="background:#FFFDF7; border:1px solid #FDE68A; border-left:5px solid #F59E0B; border-radius:10px; padding:0.9rem 1.2rem; margin:1rem 0;">
                    <b style="color:#B45309;">🍛 Local Food Secret:</b> {dest_obj.secret_eatery}
                </div>""",
                unsafe_allow_html=True,
            )

    # ── Heritage History ──
    st.markdown("### 📜 Heritage History & Cultural Lore")
    if context.history:
        st.markdown(f'<div class="culture-block">{context.history}</div>', unsafe_allow_html=True)
    elif dest_obj:
        st.markdown(f'<div class="culture-block">{dest_obj.description}</div>', unsafe_allow_html=True)

    # ── Culinary Specialties ──
    st.markdown("### 🍽️ Regional Culinary Specialties")
    if context.cuisine:
        cuisine = context.cuisine
        st.markdown(f"**Region:** {cuisine.region}")
        st.markdown(f"**🌟 Must Try:** {cuisine.must_try}")
        st.markdown(f"**📖 Food Culture:** {cuisine.food_culture_note}")

        st.markdown("**Signature Dishes:**")
        dish_cols = st.columns(min(len(cuisine.signature_dishes), 4))
        for i, dish in enumerate(cuisine.signature_dishes):
            with dish_cols[i % len(dish_cols)]:
                st.markdown(
                    f'<div style="background:#FFF7ED; border:1px solid #FED7AA; padding:8px 12px; '
                    f'border-radius:8px; text-align:center; margin:4px 0; '
                    f'font-weight:600; color:#9E1A22;">🍛 {dish}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown("---")

    # ── Festivals ──
    st.markdown("### 🎪 Living Festivals & Events")
    if context.festivals:
        for fest in context.festivals:
            with st.expander(f"🎉 {fest.name} ({', '.join(fest.months)})", expanded=False):
                st.markdown(f"**📍 Region:** {fest.region}")
                st.markdown(f"**📖 About:** {fest.description}")
                st.markdown(f"**💡 Traveler Tip:** {fest.traveler_tip}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 7: USER GUIDE & TUTORIAL
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif selected_nav == "guide":
    st.markdown(
        f"""<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem; margin-bottom:0.5rem;">
  <div>
    <h2 style="margin:0;">🧭 How to Use KannadaYatra AI (Interactive User Guide)</h2>
    <p style="color:#6B7280; font-size:1.02rem; margin:0.3rem 0 0 0;">
      Welcome to your ultimate companion for exploring Karnataka! Follow this 4-step tutorial
      to plan, navigate, and experience the state authentically.
    </p>
  </div>
  <div>{GANDABERUNDA_HERITAGE_BADGE_HTML}</div>
</div>""",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # ── Step-by-Step Tutorial Walkthrough Cards ──
    st.markdown(
        """
        <div class="tutorial-step-card">
            <div class="step-number">1</div>
            <div class="step-content">
                <h4>Choose Your Route (1-Click Presets or Custom Planner)</h4>
                <p>
                    • <b>Short on time?</b> Go to the <b>Explore & Circuits</b> tab and click <b>Plan This Trip</b> on any of the 4 iconic presets (Royal Wadiyar, Misty Ghats, Karavali Coast, or UNESCO Stone Empires).<br>
                    • <b>Want full control?</b> Open the <b>Custom Trip Planner</b> tab to set your exact duration (1-14 days), budget level (Budget, Mid-range, Luxury), group size, and companion style.
                </p>
                <span class="step-tip">💡 Pro-Tip: You don't need an API key to plan a trip - our curated engine works 100% offline!</span>
            </div>
        </div>

        <div class="tutorial-step-card">
            <div class="step-number">2</div>
            <div class="step-content">
                <h4>Explore Your Interactive Timeline & Route Map</h4>
                <p>
                    • Switch to the <b>Itinerary & Route Map</b> tab to view your chronological day-by-day plan.<br>
                    • Notice the golden hour alerts (<b>⏰ Optimal Timing</b>) to beat crowds at monuments and sunset points.<br>
                    • Check the <b>🍛 Local Food Secret</b> tags for hidden culinary gems known only to locals (like Guru Sweet Mart in Mysore or Town Canteen in Chikmagalur).
                </p>
                <span class="step-tip">💡 Pro-Tip: Click the 'Download Travel Pass (.txt)' button to keep an offline cheat-sheet on your phone.</span>
            </div>
        </div>

        <div class="tutorial-step-card">
            <div class="step-number">3</div>
            <div class="step-content">
                <h4>Learn Real-World Kannada with Audio Pronunciation</h4>
                <p>
                    • Head to the <b>Kannada Survival Kit</b> tab.<br>
                    • Select your current destination to get phrases automatically filtered for your scenario (food ordering in Udupi, bargaining at Mysore Palace bazaar, auto navigation).<br>
                    • Click the <b>🔊 Listen</b> button on any phrase to hear clear native audio pronunciation directly through your browser speakers!
                </p>
                <span class="step-tip">💡 Pro-Tip: Even simple phrases like 'Namaskāra' (Hello) and 'Dhanyavādagaḷu' (Thank you) open warm doors across Karnataka!</span>
            </div>
        </div>

        <div class="tutorial-step-card">
            <div class="step-number">4</div>
            <div class="step-content">
                <h4>Track Budget & Lock in Official Bookings</h4>
                <p>
                    • In the <b>Budget Optimizer</b> tab, inspect your daily spend breakdown (stay, food, transit, activities) via interactive donut and bar charts.<br>
                    • Use the direct links in the <b>Booking Action Bar</b> to book official KSTDC guided tours, KSRTC Airavat buses, and wildlife safari permits without paying middleman commissions.
                </p>
                <span class="step-tip">💡 Pro-Tip: Check the 'Smart Money-Saving Tips' section for tier-specific hacks like KSRTC bus passes and temple dharamshalas.</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ── Interactive "Find Your Travel Vibe" Mini-Quiz ──
    st.markdown("### 🎯 Find Your Karnataka Travel Vibe")
    vibe_choice = st.selectbox(
        "What describes your ideal travel dream?",
        options=[
            "👑 Walking through majestic palaces, whispering domes & 900-year-old temples",
            "☕ Sipping filter coffee on misty mountain peaks & walking through rain-kissed spice estates",
            "🌊 Trekking sea cliffs, swimming in crescent beaches & eating fresh seafood",
            "🏛️ Standing in awe before boulder ruins, ancient monolithic statues & rock-cut caves",
        ],
    )

    if "palaces" in vibe_choice:
        st.success("✨ **Your Match:** *Royal Wadiyar Heritage Trail* (Mysore, Srirangapatna, Belur, Halebidu). Head to **Explore & Circuits** to launch!")
    elif "coffee" in vibe_choice:
        st.success("✨ **Your Match:** *Misty Ghats & Coffee Trails* (Chikmagalur, Mullayanagiri, Coorg). Head to **Explore & Circuits** to launch!")
    elif "beaches" in vibe_choice:
        st.success("✨ **Your Match:** *Karavali Coastal Odyssey* (Gokarna, Murdeshwar, Udupi, Mangalore). Head to **Explore & Circuits** to launch!")
    else:
        st.success("✨ **Your Match:** *UNESCO Stone Empires* (Hampi, Badami, Pattadakal, Bijapur). Head to **Explore & Circuits** to launch!")

    st.markdown("---")

    # ── Karnataka Cultural Etiquette Cheat-Sheet ──
    st.markdown("### 🕉️ Essential Karnataka Travel Etiquette")
    e_col1, e_col2 = st.columns(2)
    with e_col1:
        st.markdown(
            """
            * **Temple Footwear:** Remove shoes outside temple complexes. Many ancient granite temples heat up under midday sun - visit early morning (before 9 AM).
            * **Dress Code:** Modest attire is expected at major pilgrimage shrines (Chamundeshwari, Udupi Krishna Matha, Gokarna Mahabaleshwar). Avoid shorts.
            * **Auto-Rickshaw Protocol:** In Bangalore and Mysore, politely ask *"Meter hāki, dayaviṭṭu"* (Please use the meter) or use Rapido / Ola auto for fixed pricing.
            """
        )
    with e_col2:
        st.markdown(
            """
            * **Darshini Eating Culture:** At traditional stand-and-eat *darshinis*, purchase a token at the cash counter first, then hand it to the kitchen counter.
            * **Filter Coffee Ritual:** Pour the coffee back and forth between the steel tumbler and *dabarah* cup from a height to cool it and froth the top.
            * **Eco-Responsible Travel:** Kudremukh and Western Ghats shola reserves have strict zero-plastic policies. Carry reusable water bottles.
            """
        )

    st.markdown("---")

    # ── 24x7 Verified Helplines ──
    st.markdown("### 🚨 Emergency 24x7 Helplines")
    h1, h2, h3, h4 = st.columns(4)
    with h1:
        st.info("👮 **Police Emergency**\n\n**Dial:** `112`")
    with h2:
        st.info("🏛️ **Karnataka Tourism**\n\n**Dial:** `1363` / `080-43344334`")
    with h3:
        st.info("🚌 **KSRTC Control Room**\n\n**Dial:** `080-49596666`")
    with h4:
        st.info("🚑 **Ambulance Medical**\n\n**Dial:** `108`")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#78716C; font-size:0.85rem; padding:1.2rem 0;">
        <b>KannadaYatra AI</b> - Built for the <b>Kannada Digital Innovation Hackathon 2026</b><br>
        Problem Statement 6: AI Travel Planner for Karnataka • Developed with ❤️ using Streamlit, Google Gemini & OpenStreetMap
    </div>
    """,
    unsafe_allow_html=True,
)
