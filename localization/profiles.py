LANGUAGES = {
    "English": "English",
    "Arabic": "Arabic",
    "Urdu": "Urdu",
}

COUNTRIES = {
    "UAE": {"style": "UAE/Gulf professional business style"},
    "Pakistan": {"style": "Pakistani professional business style"},
    "Saudi Arabia": {"style": "Saudi/Gulf professional business style"},
    "Global": {"style": "international professional style"},
}

PLATFORM_OPTIONS = ["LinkedIn", "Instagram", "Facebook", "TikTok", "YouTube", "X"]

def build_localization_context(language, country, dialect):
    return f"{language}; {country}; {dialect}. Use culturally appropriate vocabulary and natural phrasing."
