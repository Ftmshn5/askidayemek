# Askıda Yemek (Food-Bridge) Web - Gereksinim Analizi ve Mimari Karar Raporu (PRD)

**Durum:** Onaylandı (%100 Tamamlandı)
**Tarih:** Mart 2026 (Güncel)

## 1. Proje Özeti
"Askıda Yemek" projesi, başlangıçta planlanan masaüstü mimarisinden çıkarak modern, ölçeklenebilir ve HAVSAN standartlarına uygun **Konteynerize Web Uygulaması (Docker tabanlı)** formatına dönüştürülmüştür. Temel amaç, restoranlardaki SKT'si yaklaşan gıdaların ihtiyaç sahiplerine (öğrenciler vb.) optimize edilmiş bir algoritma ile ulaştırılmasıdır.

## 2. Teknoloji Yığını (Tech Stack)
Kullanıcının direktifleri doğrultusunda projede kullanılacak teknolojiler sabitlenmiştir:

- **Backend:** Python 3.12+ & Flask (Hafif ve amaca uygun)
- **Frontend (UI):** Jinja2 Şablon Motoru + **TailwindCSS (CDN)** + **Leaflet.js** (Sıfırdan saf HTML/CSS yazma kuralı yasaklandığı için, stil işlemleri tamamen Tailwind sınıfları kullanılarak hızlı ve modern bir şekilde halledilecektir.)
- **Veritabanı:** SQLite & SQLAlchemy (ORM)
- **Görev Zamanlayıcı (Scheduler):** APScheduler (Flask içine entegre, basit ve hafif arka plan görevleri için).
- **Geliştirme Ortamı:** Docker & Docker Compose (`docker-first` anayasasına tam uyum).

## 3. Sistem Özellikleri ve Kurallar

### 3.1. Kullanıcı Rolleri ve Yetkiler
1.  **Guest (Misafir):** Haritayı ve restoranları görüntüleyebilir, ancak talep oluşturamaz.
2.  **User (İhtiyaç Sahibi):** Sisteme kayıt olabilir, günde maksimum **3 talep** oluşturabilir. Aynı ürüne birden fazla talep açamaz.
3.  **Owner (Restoran Sahibi):** Birden fazla restoran yönetebilir, manuel ürün/porsiyon ekleyebilir.
4.  **Admin (Sistem Yöneticisi):** İstatistikleri ve raporları (CSV formatında) çekebilir. Tüm sistemi izleyebilir.

### 3.2. Eşleştirme ve İş Mantığı
- **15 Dakika Kuralı:** Bir ürün için ilk talep geldiğinde **15 dakikalık bir pencere** açılır. Bu pencere süresince talepler toplanır.
- **Puanlama (Greedy Matching):** Süre sonunda, kullanıcı tiplerine (Hamile, Engelli, Öğrenci) ve talebin yapıldığı zamana göre puan hesaplanır. Zamanın ağırlığı giderek azalır.
- **Kısmi Karşılama:** Eşleşme olduğunda kullanıcı 1 porsiyon alır ve ürünün genel miktarı 1 düşer.

### 3.3. Otomasyon (Background Tasks)
- **Otomatik Askıya Alma:** SKT'sine 6 saat kalan ürünler, restoran sahibinin müdahalesine gerek kalmadan sistem (APScheduler) tarafından otomatik olarak "Askıda" statüsüne alınır.
- **Eşleştirme Tetikleyicisi:** 15 dakikası dolan taleplerin eşleştirmeleri arka planda asenkron olarak tamamlanır.

### 3.4. Arayüz ve Harita (UI/UX)
- Harita altyapısı olarak **Leaflet.js** kullanılacaktır.
- Kullanıcıya sadece kendi konumuna **5 km** çapındaki restoranlar gösterilecektir.
- Haritada "Sadece Askıda Ürünü Olanları Göster" şeklinde dinamik bir filtre yer alacaktır.
- Uygulama dilleri **TR ve EN** olarak desteklenecektir.
- Formlarda **CSRF koruması** aktif olacaktır.

## 4. Geliştirme Süreci (Roadmap)
1. **Faz 1:** `docker-compose.yml`, `Dockerfile` ve temel Flask iskeletinin oluşturulması.
2. **Faz 2:** Veritabanı (SQLite + SQLAlchemy) şemalarının tasarlanması.
3. **Faz 3:** Frontend (Jinja2 + Tailwind) şablonlarının ve haritanın entegrasyonu. (Öncelikli)
4. **Faz 4:** Eşleştirme algoritması (Heapq/Greedy) ve APScheduler otomasyonu.
5. **Faz 5:** Raporlama, İstatistikler ve Testler.
