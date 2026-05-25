#!/usr/bin/env python3
"""🔐 PhishGuard AI — Setup & Training Script

Run this script to:
1. Configure UTF-8 encoding for Windows terminals
2. Generate synthetic training datasets
3. Train ML models for URL and email phishing detection
4. Initialize the SQLite database
5. Verify everything is ready

Usage:
    python setup_and_train.py
"""

import os
import sys
import time
import traceback
import io
from pathlib import Path

# Force UTF-8 on Windows command prompts to prevent UnicodeEncodeError
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ---------------------------------------------------------------------------
# ANSI color helpers
# ---------------------------------------------------------------------------
class _C:
    """ANSI color / style constants."""
    BOLD      = "\033[1m"
    DIM       = "\033[2m"
    UNDERLINE = "\033[4m"
    RESET     = "\033[0m"
    GREEN     = "\033[92m"
    CYAN      = "\033[96m"
    YELLOW    = "\033[93m"
    RED       = "\033[91m"
    WHITE     = "\033[97m"


def _ok(msg: str) -> None:
    print(f"  {_C.GREEN}[✓]{_C.RESET} {msg}")

def _info(msg: str) -> None:
    print(f"  {_C.CYAN}[ℹ]{_C.RESET} {msg}")

def _warn(msg: str) -> None:
    print(f"  {_C.YELLOW}[⚠]{_C.RESET} {msg}")

def _fail(msg: str) -> None:
    print(f"  {_C.RED}[✗]{_C.RESET} {msg}")

def _header(msg: str) -> None:
    print(f"\n{_C.BOLD}{_C.CYAN}{'─' * 60}")
    print(f"  {msg}")
    print(f"{'─' * 60}{_C.RESET}")

def _sub(msg: str) -> None:
    print(f"    {_C.DIM}{msg}{_C.RESET}")


def _format_size(size_bytes: int) -> str:
    """Human-readable file size."""
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024  # type: ignore[assignment]
    return f"{size_bytes:.1f} TB"


def _print_metrics(metrics: dict) -> None:
    """Pretty-print sklearn classification metrics."""
    acc  = metrics.get("accuracy", 0)
    prec = metrics.get("precision", 0)
    rec  = metrics.get("recall", 0)
    f1   = metrics.get("f1", 0)

    bar_len = 30
    def bar(val: float) -> str:
        filled = int(val * bar_len)
        return (
            f"{_C.GREEN}{'█' * filled}{_C.DIM}{'░' * (bar_len - filled)}"
            f"{_C.RESET} {val * 100:5.1f}%"
        )

    _sub(f"Accuracy  {bar(acc)}")
    _sub(f"Precision {bar(prec)}")
    _sub(f"Recall    {bar(rec)}")
    _sub(f"F1-Score  {bar(f1)}")


# ---------------------------------------------------------------------------
# BANNER
# ---------------------------------------------------------------------------
BANNER = rf"""
{_C.BOLD}{_C.CYAN}
    ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗
    ██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
    ██████╔╝███████║██║███████╗███████║██║  ███╗██║   ██║███████║██████╔╝██║  ██║
    ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
    ██║     ██║  ██║██║███████║██║  ██║╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
    ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
{_C.RESET}
{_C.BOLD}{_C.WHITE}         AI-Powered Phishing Detection System — Setup & Training{_C.RESET}
{_C.DIM}         ───────────────────────────────────────────────────────{_C.RESET}
"""


# ============================================================================
#  MAIN SETUP PIPELINE
# ============================================================================
def main() -> None:
    """Execute the full setup & training pipeline."""
    print(BANNER)
    start_time = time.time()

    # Resolve project root (directory containing this script)
    project_root = Path(__file__).resolve().parent
    os.chdir(project_root)
    sys.path.insert(0, str(project_root))

    # ------------------------------------------------------------------
    # STEP 1 — Create directories
    # ------------------------------------------------------------------
    _header("STEP 1 / 6 — Creating project directories")
    dirs_to_create = ["data", "models", "database"]
    for d in dirs_to_create:
        path = project_root / d
        path.mkdir(parents=True, exist_ok=True)
        _ok(f"Directory ready: {_C.WHITE}{path}{_C.RESET}")

    # ------------------------------------------------------------------
    # STEP 2 — Generate training datasets
    # ------------------------------------------------------------------
    _header("STEP 2 / 6 — Generating training datasets")
    try:
        from ml.dataset_generator import generate_url_dataset, generate_email_dataset, save_datasets

        _info("Generating URL and Email datasets …")
        save_datasets(output_dir="data/")
        
        url_df = generate_url_dataset()
        url_count = len(url_df)
        url_path = project_root / "data" / "url_dataset.csv"
        
        email_df = generate_email_dataset()
        email_count = len(email_df)
        email_path = project_root / "data" / "email_dataset.csv"
        
        _ok(f"URL dataset: {_C.WHITE}{url_count:,}{_C.RESET} samples → {url_path.name}")
        _ok(f"Email dataset: {_C.WHITE}{email_count:,}{_C.RESET} samples → {email_path.name}")

        phish_url = url_df["label"].sum() if "label" in url_df.columns else 0
        legit_url = url_count - phish_url
        phish_email = email_df["label"].sum() if "label" in email_df.columns else 0
        legit_email = email_count - phish_email
        _sub(f"URL     →  phishing: {phish_url}  |  legitimate: {legit_url}")
        _sub(f"Email   →  phishing: {phish_email}  |  legitimate: {legit_email}")

    except Exception as exc:
        _fail(f"Dataset generation failed: {exc}")
        traceback.print_exc()
        sys.exit(1)

    # ------------------------------------------------------------------
    # STEP 3 — Train URL phishing model
    # ------------------------------------------------------------------
    _header("STEP 3 / 6 — Training URL phishing model")
    try:
        from ml.train_model import train_url_model

        _info("Extracting URL features & fitting Random Forest …")
        url_model, url_metrics = train_url_model(url_df)
        _ok(f"URL model trained successfully  {_C.GREEN}✓{_C.RESET}")
        _print_metrics(url_metrics)

    except Exception as exc:
        _fail(f"URL model training failed: {exc}")
        traceback.print_exc()
        sys.exit(1)

    # ------------------------------------------------------------------
    # STEP 4 — Train email phishing model
    # ------------------------------------------------------------------
    _header("STEP 4 / 6 — Training email phishing model")
    try:
        from ml.train_model import train_email_model

        _info("Building TF-IDF pipeline & fitting Random Forest …")
        email_model, email_metrics = train_email_model(email_df)
        _ok(f"Email model trained successfully  {_C.GREEN}✓{_C.RESET}")
        _print_metrics(email_metrics)

    except Exception as exc:
        _fail(f"Email model training failed: {exc}")
        traceback.print_exc()
        sys.exit(1)

    # ------------------------------------------------------------------
    # STEP 5 — Save models
    # ------------------------------------------------------------------
    _header("STEP 5 / 6 — Saving trained models")
    try:
        from ml.train_model import save_models
        models_dir = project_root / "models"
        save_models(url_model, email_model, str(models_dir))

        for model_file in sorted(models_dir.glob("*.joblib")):
            size = _format_size(model_file.stat().st_size)
            _ok(f"{model_file.name}  ({_C.WHITE}{size}{_C.RESET})")

    except Exception as exc:
        _fail(f"Model saving failed: {exc}")
        traceback.print_exc()
        sys.exit(1)

    # ------------------------------------------------------------------
    # STEP 6 — Initialise database
    # ------------------------------------------------------------------
    _header("STEP 6 / 6 — Initialising database")
    try:
        from config import Config
        from database.db_manager import DatabaseManager

        db = DatabaseManager(Config.DB_PATH)
        _ok(f"SQLite database ready: {_C.WHITE}{Config.DB_PATH}{_C.RESET}")
        _sub("Tables: scans")

    except Exception as exc:
        _fail(f"Database initialisation failed: {exc}")
        traceback.print_exc()
        sys.exit(1)

    # ------------------------------------------------------------------
    # DONE 🎉
    # ------------------------------------------------------------------
    elapsed = time.time() - start_time

    print(f"\n{_C.BOLD}{_C.GREEN}{'═' * 60}")
    print(f"  🎉  SETUP COMPLETE — All systems operational!")
    print(f"{'═' * 60}{_C.RESET}")
    print()
    _ok(f"Total time: {_C.WHITE}{elapsed:.1f}s{_C.RESET}")
    _ok(f"URL model accuracy:   {_C.WHITE}{url_metrics.get('accuracy', 0) * 100:.1f}%{_C.RESET}")
    _ok(f"Email model accuracy: {_C.WHITE}{email_metrics.get('accuracy', 0) * 100:.1f}%{_C.RESET}")
    print()
    print(f"  {_C.BOLD}{_C.CYAN}🚀 Launch the application:{_C.RESET}")
    print(f"     {_C.WHITE}python app.py{_C.RESET}")
    print()
    print(f"  {_C.BOLD}{_C.CYAN}🌐 Then open in your browser:{_C.RESET}")
    print(f"     {_C.UNDERLINE}{_C.WHITE}http://localhost:5000{_C.RESET}")
    print()


if __name__ == "__main__":
    main()
