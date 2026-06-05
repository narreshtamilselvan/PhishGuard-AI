<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/5220d484-f67e-4ea0-866c-bc9fa8ff76d9" /><div align="center">

# 🔐 PhishGuard AI

### AI-Powered Phishing Detection System

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](#)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](#)
[![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-1.4-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](#)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](#)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](#license)

**A full-stack machine learning system that detects phishing URLs and emails in real-time<br>using Random Forest classifiers, advanced feature engineering, and a premium cybersecurity dashboard.**

[Features](#-features) · [Demo](#-demo) · [Quick Start](#-quick-start) · [Tech Stack](#%EF%B8%8F-tech-stack) · [ML Pipeline](#-ml-pipeline) · [API Reference](#-api-reference) · [Project Structure](#-project-structure) · [Contributing](#-contributing)

---

<img src="https://img.shields.io/badge/STATUS-Production_Ready-brightgreen?style=flat-square" alt="status" />
<img src="https://img.shields.io/badge/ML_Accuracy-95%25+-blue?style=flat-square" alt="accuracy" />
<img src="https://img.shields.io/badge/API-REST-orange?style=flat-square" alt="api" />

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔗 **URL Phishing Detection** | 15+ engineered features analysed by a Random Forest classifier — detects suspicious domains, IP-based URLs, excessive subdomains, and deceptive patterns |
| 📧 **Email Phishing Detection** | NLP-powered analysis with TF-IDF vectorisation — catches social-engineering language, urgency cues, and spoofed sender patterns |
| 🌐 **Live Website Scanner** | Real-time SSL certificate validation, redirect chain analysis, security header inspection, and content-based heuristics |
| 📊 **Threat Score Dashboard** | A cybersecurity command centre with real-time statistics, scan history charts, and threat-level breakdowns |
| 🎯 **Threat Score (0–100)** | Intuitive scoring with confidence levels and a detailed risk-factor breakdown so you know *why* something is flagged |
| 📋 **Scan History & Audit Trail** | Every scan is persisted in SQLite — filter, paginate, search, and export your entire scanning history |
| 🔌 **REST API** | Clean JSON endpoints for URL scanning, email scanning, statistics, and history — integrate PhishGuard into any workflow |
| 🎨 **Premium Dark UI** | Glassmorphic design with smooth CSS animations, responsive layout, and a hacker-aesthetic dark theme |

---

## 🖥️ Demo

> **Dashboard** — Real-time overview of all scanning activity

```
┌────────────────────────────────────────────────────┐
│  🔐 PhishGuard AI Dashboard                       │
│                                                    │
│  Total Scans    Threats Found    Safe URLs          │
│  ┌──────┐       ┌──────┐        ┌──────┐          │
│  │  142 │       │   23 │        │  119 │          │
│  └──────┘       └──────┘        └──────┘          │
│                                                    │
│  [Scan URL]  [Scan Email]  [View History]          │
└────────────────────────────────────────────────────┘
```

> **URL Scan Result** — Detailed threat analysis

```
┌────────────────────────────────────────────────────┐
│  ⚠️  PHISHING DETECTED — Threat Score: 87/100      │
│                                                    │
│  URL: http://paypa1-secure.login-verify.tk/auth    │
│  Confidence: 94.2%                                 │
│                                                    │
│  Risk Factors:                                     │
│   • Suspicious TLD (.tk)                           │
│   • Brand impersonation detected (paypal)          │
│   • Excessive URL length                           │
│   • No SSL certificate                             │
│   • Multiple subdomains                            │
└────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/phishing-detector.git
cd phishing-detector

# 2. Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run setup & training (generates data, trains models, initialises DB)
python setup_and_train.py

# 5. Launch the application
python app.py
```

### 🌐 Open in your browser

```
http://localhost:5000
```

You should see the **PhishGuard AI Dashboard** — start scanning URLs and emails immediately!

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Flask 3.0 | REST API & server-side rendering |
| **ML** | scikit-learn 1.4 | Random Forest classifiers, TF-IDF vectorisation |
| **NLP** | TF-IDF + Custom Tokeniser | Email text feature extraction |
| **Database** | SQLite 3 | Scan history & statistics persistence |
| **Frontend** | HTML5, CSS3, Vanilla JS | Premium dark-mode responsive UI |
| **HTTP Analysis** | Requests + urllib | Live URL scanning, SSL checks, header analysis |
| **Data** | pandas, NumPy | Dataset generation & feature engineering |
| **Serialisation** | joblib / pickle | Model persistence |

---

## 🧠 ML Pipeline

PhishGuard AI uses a **dual-model architecture** — one classifier for URLs and one for emails — each with purpose-built feature engineering.

### 🔗 URL Model

```
Raw URL → Feature Extraction (15+ features) → Random Forest → Prediction
```

**Engineered Features:**

| # | Feature | Description |
|---|---------|-------------|
| 1 | `url_length` | Total character count of the URL |
| 2 | `domain_length` | Length of the domain portion |
| 3 | `num_dots` | Count of dots (subdomain indicator) |
| 4 | `num_hyphens` | Count of hyphens (common in phishing) |
| 5 | `num_underscores` | Underscores in domain |
| 6 | `num_slashes` | Path depth indicator |
| 7 | `num_query_params` | Complexity of query string |
| 8 | `has_ip_address` | Whether the URL uses a raw IP |
| 9 | `has_at_symbol` | Deceptive `@` in URL |
| 10 | `has_https` | SSL usage |
| 11 | `has_suspicious_tld` | TLD in suspicious list (.tk, .ml, etc.) |
| 12 | `has_brand_name` | Known brand impersonation |
| 13 | `entropy` | Shannon entropy of domain (randomness) |
| 14 | `digit_ratio` | Proportion of digits in URL |
| 15 | `path_length` | Length of URL path component |

**Performance:** ~95%+ accuracy, ~94% precision, ~95% recall on synthetic dataset

### 📧 Email Model

```
Raw Email → TF-IDF Vectorisation → Random Forest → Prediction
```

- **TF-IDF** converts email text into numerical feature vectors
- **Custom preprocessing**: lowercasing, punctuation removal, stop-word filtering
- **Pipeline** combines vectoriser + classifier in a single sklearn Pipeline object
- Detects urgency language, credential requests, suspicious links, spoofed senders

**Performance:** ~93%+ accuracy, ~92% precision, ~93% recall on synthetic dataset

### Model Selection Rationale

| Criterion | Why Random Forest? |
|-----------|-------------------|
| **Interpretability** | Feature importance scores explain *why* something is flagged |
| **Robustness** | Ensemble method — resistant to overfitting on noisy data |
| **Speed** | Fast inference for real-time scanning (<50ms per prediction) |
| **No GPU required** | Runs on any machine — no CUDA, no cloud, no cost |

---

## 🔌 API Reference

All endpoints return JSON. The base URL is `http://localhost:5000`.

### Scan URL

```http
POST /api/scan/url
Content-Type: application/json

{"url": "https://suspicious-site.tk/login"}
```

**Response:**
```json
{
  "url": "https://suspicious-site.tk/login",
  "scan_type": "url",
  "is_phishing": true,
  "threat_score": 87,
  "confidence": 0.942,
  "risk_factors": [
    "Suspicious TLD (.tk)",
    "No SSL certificate",
    "High URL entropy"
  ],
  "scan_details": { "ssl_valid": false, "redirects": 2 },
  "scan_id": 42
}
```

### Scan Email

```http
POST /api/scan/email
Content-Type: application/json

{"email_text": "Dear user, your account has been compromised. Click here immediately to verify your identity: http://bit.ly/xyz123"}
```

**Response:**
```json
{
  "scan_type": "email",
  "is_phishing": true,
  "threat_score": 91,
  "confidence": 0.967,
  "risk_factors": [
    "Urgency language detected",
    "Shortened URL in body",
    "Credential request"
  ],
  "scan_id": 43
}
```

### Get Statistics

```http
GET /api/stats
```

```json
{
  "total_scans": 142,
  "phishing_detected": 23,
  "safe_scans": 119,
  "url_scans": 98,
  "email_scans": 44,
  "detection_rate": 16.2
}
```

### Get History (paginated)

```http
GET /api/history?page=1&per_page=20&type=url
```

```json
{
  "scans": [ ... ],
  "page": 1,
  "per_page": 20,
  "total_count": 98,
  "total_pages": 5,
  "scan_type": "url"
}
```

### Delete Scan

```http
DELETE /api/history/42
```

```json
{ "success": true, "message": "Scan 42 deleted" }
```

### Clear All History

```http
POST /api/history/clear
```

```json
{ "success": true, "message": "Cleared 142 scan records", "count": 142 }
```

### cURL Examples

```bash
# Scan a URL
curl -X POST http://localhost:5000/api/scan/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Scan an email
curl -X POST http://localhost:5000/api/scan/email \
  -H "Content-Type: application/json" \
  -d '{"email_text": "Click here to claim your prize!"}'

# Get dashboard stats
curl http://localhost:5000/api/stats

# Get scan history
curl "http://localhost:5000/api/history?page=1&per_page=10&type=all"
```

---

## 📁 Project Structure

```
phishing-detector/
│
├── app.py                      # Flask application (routes, API, error handlers)
├── config.py                   # Centralised configuration
├── setup_and_train.py          # One-command setup & training script
├── requirements.txt            # Python dependencies
├── README.md                   # You are here!
│
├── ml/                         # Machine Learning module
│   ├── __init__.py
│   ├── feature_extractor.py    # URL feature engineering (15+ features)
│   ├── trainer.py              # Model training & evaluation
│   └── predictor.py            # Inference / prediction interface
│
├── scanner/                    # Live scanning module
│   ├── __init__.py
│   ├── url_scanner.py          # SSL, redirects, headers, content checks
│   └── email_scanner.py        # Email content & header analysis
│
├── database/                   # Persistence layer
│   ├── __init__.py
│   └── db_manager.py           # SQLite CRUD, statistics, history
│
├── data/                       # Training data (generated)
│   ├── generate_dataset.py     # Synthetic dataset generator
│   ├── url_dataset.csv         # (generated) URL training data
│   └── email_dataset.csv       # (generated) Email training data
│
├── models/                     # Trained models (generated)
│   ├── url_model.pkl           # (generated) Serialised URL classifier
│   └── email_model.pkl         # (generated) Serialised email classifier
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Base layout with dark theme
│   ├── dashboard.html          # Main dashboard
│   ├── scan_url.html           # URL scanner page
│   ├── scan_email.html         # Email scanner page
│   ├── history.html            # Scan history with pagination
│   └── errors/
│       ├── 404.html
│       └── 500.html
│
└── static/                     # Frontend assets
    ├── css/
    │   └── style.css           # Glassmorphic dark theme styles
    └── js/
        └── app.js              # Frontend interactivity & API calls
```

---

## 🔒 Security Considerations

- **Input Validation** — All user inputs are sanitised before processing
- **SQL Injection Prevention** — Parameterised queries throughout
- **Rate Limiting** — Recommended for production deployment (use Flask-Limiter)
- **CORS** — Configurable cross-origin headers
- **No External Data Leakage** — URLs are scanned server-side; nothing is sent to third parties

---
## SCREENSHOTS 

<img width="1920" height="1080" alt="Screenshot (23)" src="https://github.com/user-attachments/assets/7e098dfa-34c1-4cbe-8d68-a080b683fa1b" />
<img width="1920" height="1080" alt="Screenshot (24)" src="https://github.com/user-attachments/assets/6ec67989-16bf-4abe-94f1-ab8458191ce1" />
<img width="1920" height="1080" alt="Screenshot (21)" src="https://github.com/user-attachments/assets/86e6a866-5b4e-4123-aeeb-04f6d7a32e9e" />



## 🗺️ Roadmap

- [ ] 🔄 Real-time browser extension integration
- [ ] 📈 Advanced analytics dashboard with D3.js charts
- [ ] 🧪 A/B testing with XGBoost / LightGBM models
- [ ] 🐳 Docker containerisation
- [ ] ☁️ One-click cloud deployment (AWS / GCP / Azure)
- [ ] 📱 Mobile-responsive progressive web app (PWA)
- [ ] 🔗 VirusTotal API integration for cross-referencing
- [ ] 📬 IMAP/POP3 email inbox scanner

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

Please make sure to:
- Follow the existing code style
- Add docstrings to new functions
- Update the README if you add new features
- Write tests for new functionality

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for cybersecurity**

*If you found this project useful, please consider giving it a ⭐*

[![GitHub stars](https://img.shields.io/github/stars/yourusername/phishing-detector?style=social)](#)

</div>
