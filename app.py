"""
🔐 PhishGuard AI — Main Flask Application

Central application module that ties together:
- ML-based phishing prediction (URL & Email)
- Live URL scanning (SSL, redirects, headers)
- Email content analysis (NLP-powered)
- SQLite-backed scan history & statistics
- REST API for programmatic access
- Premium dark-mode cybersecurity dashboard
"""

import os
import sys
import json
import math
import logging
from datetime import datetime
from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
)
from config import Config
from ml.predictor import PhishingPredictor
from scanner.url_scanner import URLScanner
from scanner.email_scanner import EmailScanner
from database.db_manager import DatabaseManager

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("PhishGuard")

# ---------------------------------------------------------------------------
# Application Factory
# ---------------------------------------------------------------------------
app = Flask(__name__)
app.config.from_object(Config)

# --- Database -----------------------------------------------------------------
db_manager = DatabaseManager(Config.DB_PATH)
logger.info("Database initialized at %s", Config.DB_PATH)

# --- ML Predictor -------------------------------------------------------------
predictor: PhishingPredictor | None = None
try:
    predictor = PhishingPredictor(Config.MODELS_DIR)
    logger.info("ML models loaded from %s", Config.MODELS_DIR)
except FileNotFoundError:
    logger.warning(
        "Trained models not found in '%s'. "
        "Run  python setup_and_train.py  to train the models first.",
        Config.MODELS_DIR,
    )
except Exception as exc:  # noqa: BLE001
    logger.error("Failed to load ML models: %s", exc, exc_info=True)

# --- Scanners -----------------------------------------------------------------
url_scanner = URLScanner()
email_scanner = EmailScanner()
logger.info("URL & Email scanners ready")


# ============================================================================
# CORS — simple middleware (avoids external dependency)
# ============================================================================
@app.after_request
def _add_cors_headers(response):
    """Attach permissive CORS headers so the API can be consumed from any origin."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


# ============================================================================
#  PAGE ROUTES
# ============================================================================
@app.route("/")
def dashboard():
    """Render the main dashboard / command-centre page."""
    return render_template("dashboard.html")


@app.route("/scan/url")
def scan_url_page():
    """Render the URL scanner page."""
    return render_template("scan_url.html")


@app.route("/scan/email")
def scan_email_page():
    """Render the email scanner page."""
    return render_template("scan_email.html")


@app.route("/history")
def history_page():
    """Render the scan-history / audit-trail page."""
    return render_template("history.html")


# ============================================================================
#  API ROUTES — Scanning
# ============================================================================
@app.route("/api/scan/url", methods=["POST"])
def api_scan_url():
    """Analyse a URL for phishing indicators.

    **Request JSON**::

        {"url": "https://example.com"}

    **Response JSON** includes ML prediction, threat score, confidence,
    risk factors, and live-scan results.
    """
    data = request.get_json(silent=True) or {}
    url: str = (data.get("url") or "").strip()

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Model availability gate
    if predictor is None:
        return (
            jsonify({
                "error": (
                    "Models not trained yet. "
                    "Run setup_and_train.py first."
                )
            }),
            503,
        )

    try:
        # --- ML prediction ---------------------------------------------------
        prediction = predictor.predict_url(url)

        # --- Live website scan -----------------------------------------------
        scan_results = url_scanner.scan(url)

        # --- Combine results --------------------------------------------------
        combined: dict = {
            "url": url,
            "scan_type": "url",
            "timestamp": datetime.now().isoformat(),
            # ML results
            "is_phishing": prediction.get("is_phishing", False),
            "threat_score": prediction.get("threat_score", 0),
            "confidence": prediction.get("confidence", 0),
            "risk_factors": prediction.get("risk_factors", []),
            "features": prediction.get("features", {}),
            # Live-scan results
            "scan_details": scan_results,
        }

        # --- Persist ----------------------------------------------------------
        scan_id = db_manager.save_scan(
            scan_type="url",
            target=url,
            result=combined,
        )
        combined["scan_id"] = scan_id

        logger.info(
            "URL scan complete — %s | phishing=%s | score=%s",
            url,
            combined["is_phishing"],
            combined["threat_score"],
        )
        return jsonify(combined), 200

    except Exception as exc:  # noqa: BLE001
        logger.error("URL scan failed for '%s': %s", url, exc, exc_info=True)
        return jsonify({"error": f"Scan failed: {str(exc)}"}), 500


@app.route("/api/scan/email", methods=["POST"])
def api_scan_email():
    """Analyse email text for phishing indicators.

    **Request JSON**::

        {"email_text": "Dear user, click here to verify …"}

    **Response JSON** mirrors the URL scan structure with email-specific
    risk factors and content-analysis results.
    """
    data = request.get_json(silent=True) or {}
    email_text: str = (data.get("email_text") or "").strip()

    if not email_text:
        return jsonify({"error": "Email text is required"}), 400

    if predictor is None:
        return (
            jsonify({
                "error": (
                    "Models not trained yet. "
                    "Run setup_and_train.py first."
                )
            }),
            503,
        )

    try:
        # --- ML prediction ---------------------------------------------------
        prediction = predictor.predict_email(email_text)

        # --- Content scan -----------------------------------------------------
        scan_results = email_scanner.scan(email_text)

        # --- Combine ----------------------------------------------------------
        combined: dict = {
            "email_text": email_text[:500],  # truncate for storage
            "scan_type": "email",
            "timestamp": datetime.now().isoformat(),
            "is_phishing": prediction.get("is_phishing", False),
            "threat_score": prediction.get("threat_score", 0),
            "confidence": prediction.get("confidence", 0),
            "risk_factors": prediction.get("risk_factors", []),
            "features": prediction.get("features", {}),
            "scan_details": scan_results,
        }

        scan_id = db_manager.save_scan(
            scan_type="email",
            target=email_text[:200],
            result=combined,
        )
        combined["scan_id"] = scan_id

        logger.info(
            "Email scan complete — phishing=%s | score=%s",
            combined["is_phishing"],
            combined["threat_score"],
        )
        return jsonify(combined), 200

    except Exception as exc:  # noqa: BLE001
        logger.error("Email scan failed: %s", exc, exc_info=True)
        return jsonify({"error": f"Scan failed: {str(exc)}"}), 500


# ============================================================================
#  API ROUTES — Statistics & History
# ============================================================================
@app.route("/api/stats", methods=["GET"])
def api_stats():
    """Return aggregate scan statistics for the dashboard."""
    try:
        stats = db_manager.get_statistics()
        return jsonify(stats), 200
    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to fetch stats: %s", exc, exc_info=True)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/history", methods=["GET"])
def api_history():
    """Return paginated scan history.

    **Query params:**

    - ``page``      — page number (default 1)
    - ``per_page``  — items per page (default 20, max 100)
    - ``type``      — filter: ``all`` | ``url`` | ``email`` (default all)
    """
    try:
        page = max(1, request.args.get("page", 1, type=int))
        per_page = min(100, max(1, request.args.get("per_page", 20, type=int)))
        scan_type = request.args.get("type", "all").lower()

        if scan_type not in ("all", "url", "email"):
            scan_type = "all"

        history = db_manager.get_history(
            page=page,
            per_page=per_page,
            scan_type=scan_type,
        )

        total_count = db_manager.get_history_count(scan_type=scan_type)
        total_pages = max(1, math.ceil(total_count / per_page))

        return jsonify({
            "scans": history,
            "page": page,
            "per_page": per_page,
            "total_count": total_count,
            "total_pages": total_pages,
            "scan_type": scan_type,
        }), 200

    except Exception as exc:  # noqa: BLE001
        logger.error("Failed to fetch history: %s", exc, exc_info=True)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/history/<int:scan_id>", methods=["DELETE"])
def api_delete_scan(scan_id: int):
    """Delete a single scan record by ID."""
    try:
        deleted = db_manager.delete_scan(scan_id)
        if deleted:
            return jsonify({"success": True, "message": f"Scan {scan_id} deleted"}), 200
        return jsonify({"success": False, "error": "Scan not found"}), 404
    except Exception as exc:  # noqa: BLE001
        logger.error("Delete scan %s failed: %s", scan_id, exc, exc_info=True)
        return jsonify({"error": str(exc)}), 500


@app.route("/api/history/clear", methods=["POST"])
def api_clear_history():
    """Delete **all** scan history records."""
    try:
        count = db_manager.clear_history()
        return jsonify({
            "success": True,
            "message": f"Cleared {count} scan records",
            "count": count,
        }), 200
    except Exception as exc:  # noqa: BLE001
        logger.error("Clear history failed: %s", exc, exc_info=True)
        return jsonify({"error": str(exc)}), 500


# ============================================================================
#  ERROR HANDLERS
# ============================================================================
def _is_api_request() -> bool:
    """Return *True* when the client expects a JSON response."""
    return (
        request.path.startswith("/api/")
        or request.accept_mimetypes.best == "application/json"
    )


@app.errorhandler(404)
def not_found(error):
    """Handle 404 — JSON for API consumers, HTML for browsers."""
    if _is_api_request():
        return jsonify({"error": "Resource not found", "status": 404}), 404
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 — JSON for API consumers, HTML for browsers."""
    if _is_api_request():
        return jsonify({"error": "Internal server error", "status": 500}), 500
    return render_template("errors/500.html"), 500


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 — Method Not Allowed."""
    if _is_api_request():
        return jsonify({"error": "Method not allowed", "status": 405}), 405
    return jsonify({"error": "Method not allowed"}), 405


# ============================================================================
#  ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    logger.info("🔐 PhishGuard AI starting on http://0.0.0.0:5000")
    app.run(debug=Config.DEBUG, host="0.0.0.0", port=5000)
