"""All words and facts for bluefrogplumbingofalpharetta.com. Edit here, then run: python3 build.py (rewrites docs/).
Public repo: no private data. Rules: only true copy; no "licensed", no years, no reviews/testimonials,
no Bluefrog corporate text. Logo + mascot: supplied by the client on 23 Oct 2026 (src/img, made by src/prep_images.py)."""
import json, os

INDEXABLE = True        # LIVE site (switched on 16 Oct 2026). Never noindex.

SITE = {
    "domain": "https://bluefrogplumbingofalpharetta.com",
    "base": "",
    "name": "Bluefrog Plumbing + Drain of Alpharetta",   # Brian Kingsley's own spelling.
    "phone_display": "(678) 331-5843",                  # CallScaler tracking number (bought 16 Oct 2026)
    "phone_tel": "+16783315843",
    "phone_e164": "+1-678-331-5843",
    "sms_tel": None,                                    # no text line announced: call-only
    "email": None,
    "street": "1007 Mansell Rd #A122",
    "city": "Roswell", "region": "GA", "zip": "30076",
    "schema_type": "Plumber",
}
# Bluefrog brand colours, sampled from the client's logo file (23 Oct 2026): blue #0078BA, dark blue #006CA3, green #8DC63F.
PALETTE = {"brand": "#0078ba", "brand_dk": "#006ca3", "accent": "#8dc63f", "dark": "#0b3554"}
LOGO_IMG = ("logo-60.png", "logo-120.png", 392, 60)    # 1x, 2x, width, height - client's own logo
MASCOT = ("mascot.webp", 593, 900)                      # client's frog mascot, shown in the image panels
FONTS = ["fredoka-latin.woff2", "nunito-latin.woff2"]  # brand-matched rounded fonts (SIL OFL); first one is preloaded

COPY = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "copy.json")))

SERVICES = [  # slug, name, short blurb
    ("drain-cleaning", "Drain Cleaning", "Clogged sinks, tubs, showers and slow drains cleared."),
    ("water-heater", "Water Heater Repair & Installation", "Repair or replace a water heater that is failing or leaking."),
    ("leak-repair", "Leak Repair", "Track down and fix dripping pipes and supply line leaks."),
    ("sewer-line", "Sewer Line Service", "Backups, slow main drains, gurgling and sewer odors."),
    ("toilet-faucet-fixtures", "Toilet, Faucet & Fixture Repair", "Running toilets, dripping faucets and worn fixtures."),
    ("repiping", "Repiping", "Replace aging supply piping in your home."),
    ("garbage-disposal", "Garbage Disposal", "Jammed, leaking or humming disposals repaired or replaced."),
    ("emergency-plumbing", "Emergency Plumbing", "Burst pipes, major leaks, overflowing toilets and backups."),
]
AREAS = [("johns-creek", "Johns Creek"), ("sandy-springs", "Sandy Springs"), ("alpharetta", "Alpharetta"),
         ("cumming", "Cumming"), ("milton", "Milton")]
WHY = [  # icon, title, text
    ("focus", "Plumbing only", "Plumbing is the only trade on this site. Every call is a plumbing call."),
    ("call", "Call to book", "Reach us by phone and book an appointment."),
    ("doc", "Clear service pages", "Each service page explains the signs to watch for and what a visit generally involves."),
    ("local", "North Fulton and Forsyth", "Serving Alpharetta, Johns Creek, Sandy Springs, Cumming and Milton."),
]
STRIP = [("drain-cleaning", "Drain cleaning"), ("water-heater", "Water heaters"), ("leak-repair", "Leak repair"),
         ("emergency-plumbing", "Emergency plumbing")]

LOGO_TOP = "BLUEFROG PLUMBING"
LOGO_SUB = "+ Drain of Alpharetta"
TOPBAR = "1007 Mansell Rd #A122, Roswell, GA 30076"
TOPBAR2 = "Plumbing only"
TOPBAR_CALL = "Call to book"
EYEBROW = "Plumbing · Alpharetta, GA"
HERO_BTN = "Call to book"
ASIDE_TITLE = "Call to book"
LEGAL_LINE = "Plumbing, Roswell, GA"
WHY_TITLE = "Why homeowners call us"
HOME_H2 = "Serving Johns Creek, Sandy Springs, Alpharetta, Cumming and Milton"
HERO_CARD = {"title": "Call to book", "text": "Reach us by phone and book an appointment. There is no online form to fill out.",
             "ticks": ["Plumbing is the only trade", "Office in Roswell, GA", "Alpharetta, Johns Creek, Sandy Springs, Cumming and Milton"]}
CTA = {"title": "Need a plumber in North Fulton or Forsyth?", "text": "Call to book an appointment."}

HOME = dict(
    title="Plumber in Alpharetta, GA | Bluefrog Plumbing + Drain of Alpharetta",
    description="Bluefrog Plumbing + Drain of Alpharetta is a plumbing company with an office in Roswell, GA, serving Alpharetta, Johns Creek, Sandy Springs, Cumming and Milton. Call to book an appointment.",
    h1="Plumber in Alpharetta, GA",
    lead="{BIZ} handles drains, water heaters, leaks, sewer lines and more for homeowners in Alpharetta, Johns Creek, Sandy Springs, Cumming and Milton. Call to book an appointment.")
SERVICES_HUB = dict(
    title="Plumbing Services in Alpharetta, GA | Bluefrog Plumbing + Drain of Alpharetta",
    description="Drain cleaning, water heaters, leak repair, sewer lines, fixtures, repiping, disposals and emergency plumbing.",
    h1="Plumbing Services", lead="Plumbing services from {BIZ}, with an office in Roswell, GA.")
SERVICE_TITLE = "{n} in Alpharetta, GA | Bluefrog Plumbing + Drain of Alpharetta"
SERVICE_DESC = "{n} from Bluefrog Plumbing + Drain of Alpharetta, serving Alpharetta, Johns Creek, Sandy Springs, Cumming and Milton. {b}"
SERVICE_H1 = "{n} in Alpharetta, GA and Nearby"
AREAS_HUB = dict(
    title="Plumbing Service Areas: Johns Creek, Sandy Springs, Alpharetta and More | Bluefrog Plumbing + Drain of Alpharetta",
    description="Plumbing service in Johns Creek, Sandy Springs, Alpharetta, Cumming and Milton, GA.",
    h1="Service Areas", lead="With an office in Roswell, GA, we serve homeowners in these cities.")
AREA_TITLE = "Plumber in {c}, GA | Bluefrog Plumbing + Drain of Alpharetta"
AREA_DESC = "Plumbing service in {c}, Georgia from Bluefrog Plumbing + Drain of Alpharetta. Drains, water heaters, leaks and more. Call to book."
AREA_H1 = "Plumber in {c}, GA"
AREA_LEAD = "Plumbing service in {c}, Georgia. Call to book an appointment."
ABOUT = dict(
    title="About Bluefrog Plumbing + Drain of Alpharetta | Roswell, GA Plumbing",
    description="Bluefrog Plumbing + Drain of Alpharetta is a plumbing company with an office in Roswell, GA, serving Alpharetta, Johns Creek, Sandy Springs, Cumming and Milton.",
    h1=("About", "Bluefrog Plumbing + Drain of Alpharetta"), lead="")
CONTACT = dict(
    title="Contact Bluefrog Plumbing + Drain of Alpharetta | Call for a Plumber",
    description="Call Bluefrog Plumbing + Drain of Alpharetta to book a plumbing appointment in Alpharetta, Johns Creek, Sandy Springs, Cumming or Milton, GA.",
    h1=("Contact", "Bluefrog Plumbing + Drain of Alpharetta"),
    lead="The fastest way to reach us is to call. Tell us what is happening with your plumbing and we will book an appointment. There is no online form.",
    after="We serve: Johns Creek, Sandy Springs, Alpharetta, Cumming and Milton.")
