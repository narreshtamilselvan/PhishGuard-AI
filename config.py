"""
Application Configuration — Centralised Constants and Paths.

All tuneable knobs for the Phishing Detection System live here.
Environment variables take precedence where applicable.
"""

import os


class Config:
    """Global configuration for the Phishing Detection System."""

    # ── Paths ──────────────────────────────────────────────────────────
    BASE_DIR: str = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY: str = os.environ.get(
        "SECRET_KEY", "phishing-detector-secret-key-2024"
    )
    DEBUG: bool = os.environ.get("FLASK_DEBUG", "True").lower() == "true"

    # ── Database ───────────────────────────────────────────────────────
    DB_PATH: str = os.path.join(BASE_DIR, "phishing_detector.db")

    # ── ML Models ──────────────────────────────────────────────────────
    MODELS_DIR: str = os.path.join(BASE_DIR, "models")
    URL_MODEL_PATH: str = os.path.join(MODELS_DIR, "url_model.pkl")
    EMAIL_MODEL_PATH: str = os.path.join(MODELS_DIR, "email_model.pkl")

    # ── Dataset ────────────────────────────────────────────────────────
    DATA_DIR: str = os.path.join(BASE_DIR, "data")

    # ── Scanning ───────────────────────────────────────────────────────
    REQUEST_TIMEOUT: int = 10
    MAX_REDIRECTS: int = 5

    # ── Threat Thresholds (0–100 scale) ────────────────────────────────
    THREAT_LOW: int = 30
    THREAT_MEDIUM: int = 60
    THREAT_HIGH: int = 80
