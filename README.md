# 🥣 Askıda Yemek (Food Bridge) Platformu

*🌍 [Click here for the English version](README_en.md)*

Askıda Yemek, gıda israfını önlemek ve toplumsal dayanışmayı artırmak amacıyla geliştirilmiş modern bir web platformudur. Restoranların gün sonunda ellerinde kalan taze ürünleri indirimli veya ücretsiz (askıda) olarak ihtiyaç sahipleriyle paylaşmasını sağlar.

## 🚀 Öne Çıkan Özellikler

- **📍 Etkileşimli Harita:** Bölgedeki restoranları ve askıda ürünleri Leaflet.js tabanlı harita üzerinden anlık takip edin.
- **🛡️ PIN Doğrulama Sistemi:** Güvenli teslimat için her eşleşmede üretilen 6 haneli benzersiz PIN kodu ile işlemlerinizi onaylayın.
- **🌍 Çoklu Dil Desteği:** Türkçe ve İngilizce (i18n) dil seçenekleriyle kapsayıcı kullanım.
- **👥 Gelişmiş Kayıt Sistemi:** Restoran sahipleri ve İhtiyaç Sahipleri (Öğrenci, Engelli, Hamile vb.) için özelleştirilmiş kayıt süreçleri.
- **⚡ Akıllı Eşleştirme:** "Greedy Matching" algoritması ve öncelik skoru sistemi ile adil ürün dağıtımı.
- **📊 Etki Raporu:** Kurtarılan gıda miktarını ve yapılan bağışları görsel grafiklerle takip edin.
- **🐳 Docker Entegrasyonu:** Tek komutla tüm geliştirme ortamını ayağa kaldırın.

## 🛠️ Teknoloji Yığını

- **Backend:** Python / Flask
- **Frontend:** Jinja2 / Vanilla JS / CSS3
- **Veritabanı:** SQLAlchemy / SQLite
- **Harita:** Leaflet.js / OpenStreetMap
- **Container:** Docker / Docker Compose

## 📦 Kurulum ve Çalıştırma

Projenin en stabil çalışması için Docker kullanılması önerilir.

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/betulbilhan2/askida-yemek-web.git
    cd askida-yemek-web
    ```

2.  **Docker ile Çalıştırın:**
    ```bash
    docker compose up --build -d
    ```

3.  **Veritabanını Başlatın (İlk Kurulum):**
    ```bash
    docker compose exec web python -c "from app import app, db; from seed_data import seed_database; with app.app_context(): db.create_all(); seed_database()"
    ```

4.  **Erişim:**
    Tarayıcınızdan `http://localhost:5001` adresine gidin.

## 👥 Demo Hesaplar

| Rol | Kullanıcı Adı | Şifre |
| :--- | :--- | :--- |
| **Restoran** | `lezzet_sofrasi` | `123456` |
| **İhtiyaç Sahibi** | `ahmet_yilmaz` | `123456` |

---
*Bu proje HAVSAN Mühendislik Standartları ve İleri Programlama Teknikleri dersi kapsamında modernize edilmiştir.*
