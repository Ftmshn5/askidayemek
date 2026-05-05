# 🥣 Askıda Yemek (Food Bridge) Platform

Askıda Yemek (Food Bridge) is a modern web platform developed to prevent food waste and increase social solidarity. It allows restaurants to share their remaining fresh products at the end of the day with those in need at a discount or for free (suspended).

## 🚀 Key Features

- **📍 Interactive Map:** Track restaurants and suspended products in the region in real-time via a Leaflet.js-based map.
- **🛡️ PIN Verification System:** Confirm your transactions with a 6-digit unique PIN code generated for each match for safe delivery.
- **🌍 Multi-Language Support:** Inclusive usage with Turkish and English (i18n) language options.
- **👥 Advanced Registration System:** Customized registration processes for Restaurant owners and People in Need (Students, Disabled, Pregnant, etc.).
- **⚡ Smart Matching:** Fair product distribution with "Greedy Matching" algorithm and priority score system.
- **📊 Impact Report:** Track the amount of rescued food and donations made with visual charts.
- **🐳 Docker Integration:** Boot up the entire development environment with a single command.

## 🛠️ Technology Stack

- **Backend:** Python / Flask
- **Frontend:** Jinja2 / Vanilla JS / CSS3
- **Database:** SQLAlchemy / SQLite
- **Map:** Leaflet.js / OpenStreetMap
- **Container:** Docker / Docker Compose

## 📦 Installation and Running

It is recommended to use Docker for the most stable operation of the project.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Ftmshn5/askidayemek.git
    cd askidayemek
    ```

2.  **Run with Docker:**
    ```bash
    docker compose up --build -d
    ```

3.  **Initialize the Database (First Setup):**
    ```bash
    docker compose exec web python -c "from app import app, db; from seed_data import seed_database; with app.app_context(): db.create_all(); seed_database()"
    ```

4.  **Access:**
    Go to `http://localhost:5001` in your browser.

## 👥 Demo Accounts

| Role | Username | Password |
| :--- | :--- | :--- |
| **Restaurant** | `lezzet_sofrasi` | `123456` |
| **Person in Need** | `ahmet_yilmaz` | `123456` |

---
*This project has been modernized as part of the HAVSAN Engineering Standards and Advanced Programming Techniques course.*
