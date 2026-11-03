"""Quick integration test for KannadaYatra AI modules."""
import sys
import os
os.environ["PYTHONIOENCODING"] = "utf-8"
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")

from utils.helpers import (
    filter_destinations, compute_trip_budget, format_inr,
    get_all_regions, KARNATAKA_DESTINATIONS,
)
from core.insights import (
    get_full_cultural_context, PHRASE_CATEGORIES, KARNATAKA_FESTIVALS,
    REGIONAL_CUISINES,
)
from core.planner import generate_itinerary

print("=== All modules imported successfully ===")

# Test destination filtering
dests = filter_destinations(["Heritage", "Food"])
print(f"Filtered {len(dests)} destinations for Heritage+Food")

# Test budget engine
budget = compute_trip_budget("Mid-range", 3, 2)
print(f"Budget total_avg: {format_inr(budget['total_avg'])}")
print(f"Budget total_min: {format_inr(budget['total_min'])}")
print(f"Budget total_max: {format_inr(budget['total_max'])}")

# Test cultural context
ctx = get_full_cultural_context("Mysore Palace")
print(f"Cultural context for Mysore Palace:")
print(f"  Phrase categories: {len(ctx.survival_phrases)}")
print(f"  Has history: {bool(ctx.history)}")
print(f"  Has cuisine: {bool(ctx.cuisine)}")
print(f"  Festivals: {len(ctx.festivals)}")

# Test data completeness
print(f"Total destinations: {len(KARNATAKA_DESTINATIONS)}")
print(f"Total phrase categories: {len(PHRASE_CATEGORIES)}")
print(f"Total festivals: {len(KARNATAKA_FESTIVALS)}")
print(f"Total regional cuisines: {len(REGIONAL_CUISINES)}")
print(f"Regions: {get_all_regions()}")

# Test itinerary generation (curated fallback)
itin, ai_used = generate_itinerary(
    interests=["Heritage", "Food"],
    budget_tier="Mid-range",
    days=3,
    travelers=2,
    companions="Couple",
)
print(f"\nItinerary: {itin.trip_title}")
print(f"Days: {len(itin.days)}, AI used: {ai_used}")
for day in itin.days:
    print(f"  Day {day.day_number}: {day.title} ({len(day.slots)} slots, stay: {day.overnight_stay})")

print("\n=== ALL TESTS PASSED ===")
