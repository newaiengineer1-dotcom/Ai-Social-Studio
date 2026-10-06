from localization.profiles import LANGUAGES, COUNTRIES
from rag.retriever import BrandRAG
from connectors.registry import connector_status

def test_profiles():
    assert "English" in LANGUAGES
    assert "Arabic" in LANGUAGES
    assert "Urdu" in LANGUAGES
    assert "UAE" in COUNTRIES
    assert "Pakistan" in COUNTRIES

def test_rag():
    r = BrandRAG()
    r.add_text("Solar battery storage for commercial facilities.")
    assert "battery" in r.retrieve("battery storage").lower()

def test_connectors():
    assert "LinkedIn" in connector_status()
