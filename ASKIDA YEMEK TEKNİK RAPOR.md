Bu teknik rapor, "Askıda Yemek" projesinin akademik standartlara uygun, modüler ve ölçeklenebilir bir yapıda gerçekleştirilmesi için hazırlanan kapsamlı bir yol haritasıdır.

**TEKNİK PROJE RAPORU: ASKIDA YEMEK (FOOD-BRIDGE)**

**Kurum:** Fırat Üniversitesi Teknoloji Fakültesi

**Bölüm:** Yazılım Mühendisliği Bölümü

**Ders:** YMH220 İleri Programlama Teknikleri

**Geliştiriciler:** Betül Bilhan, Sudenaz Koçoğlu, Dilan Çiçek, Fatma Şahin, Nisa Nur Erkuş

**Tarih:** Mart 2026

**1\. Proje Tanımı ve Amacı**

Bu proje, restoranlardaki ihtiyaç fazlası ve son tüketim tarihi (SKT) yaklaşan gıdaların, ihtiyaç sahiplerine (öğrenciler, engelliler, düşük gelirli gruplar) optimize edilmiş bir eşleştirme algoritmasıyla ulaştırılmasını sağlayan bir masaüstü simülasyon uygulamasıdır. Temel amaç, gıda israfını minimuma indirirken toplumsal dayanışmayı teknolojik bir altyapıya kavuşturmaktır.

**2\. Sistem Mimarisi (System Architecture)**

Uygulama, sürdürülebilirliği sağlamak amacıyla **Katmanlı Mimari (Layered Architecture)** prensibiyle tasarlanmıştır.

- **Sunum Katmanı (UI):** Kullanıcı dostu, harita entegrasyonlu arayüz.
- **İş Mantığı Katmanı (Business Logic):** Eşleştirme algoritmaları, önceliklendirme ve otomatik SKT kontrolü.
- **Veri Katmanı (Data Access):** Nesne ilişkisel eşleme (ORM) üzerinden veritabanı yönetimi.

**3\. Teknik Veri Yapısı ve Teknolojiler**

Projede modern Python ekosistemi ve akademik gereksinimleri karşılayan şu teknolojiler kullanılacaktır:

- **Dil:** Python 3.12+
- **Arayüz (GUI):** PySide6 (Qt) veya Tkinter (Modern görünüm ve harita desteği için).
- **Veritabanı (DB):** SQLite (Taşınabilirlik için) ve **SQLAlchemy (ORM)** (Veri yönetimi için).
- **Harita:** tkintermapview (OpenStreetMap verileri ile restoran lokasyon görselleştirmesi).
- **Veri Analizi:** **Pandas** (İşlem geçmişi raporlama ve istatistik üretimi için).
- **Veri Yapısı:** heapq (Min-Heap kullanılarak en acil gıdaların önceliklendirilmesi).

**4\. Sistem Çalışma Mantığı ve Algoritmalar**

**4.1. Hibrid İlan Sistemi**

Sistem iki tür veri girişi kabul eder:

1.  **Otomatik Giriş:** Restoran envanterindeki ürünlerin SKT'sine 6 saatten az kaldığında sistem ürünü otomatik olarak "Askıda" statüsüne geçirir.
2.  **Manuel Giriş:** Restoran sahibi (Owner), elinde kalan fazla porsiyonları anlık olarak sisteme yükleyebilir.

**4.2. Önceliklendirme ve Eşleştirme (Batch Matching)**

Talep açıldıktan sonra 15 dakikalık bir "Talep Toplama" süreci başlar. Bu sürede her talep sahibi için bir **Öncelik Skoru ($P$)** hesaplanır:

$$P = (W_{type} \\times 0.6) + (W_{time} \\times 0.4)$$

- $W_{type}$: Kullanıcı tipi puanı (Hamile/Engelli: 100, Öğrenci: 80, Standart: 50).
- $W_{time}$: Talebin yapıldığı anın önceliği (İlk gelen avantajı).

Süre sonunda **Greedy Matching** algoritması, en yüksek puanlı kullanıcıları en yakın tarihli ürünlerle eşleştirir.

**5\. Use Case (Kullanım Durumu) Analizi**

| **Rol** | **Ana Görevler** |
| --- | --- |
| **Restoran Sahibi (Owner)** | Ürün ekleme, stok takibi, bağış geçmişini görüntüleme. |
| **Kullanıcı (User)** | Harita üzerinde restoranları görme, ürün detayı inceleme, talep oluşturma. |
| **Sistem (Admin/Auto)** | SKT kontrolü, eşleştirme algoritmasını tetikleme, CSV raporu oluşturma. |

**6\. Veritabanı Şeması (İskelet)**

- **Users Table:** id, username, password, user_type, points
- **Restaurants Table:** id, name, lat, lon, rating
- **Products Table:** id, res_id, name, skt_date, status (Available/Suspended)
- **Transactions Table:** id, user_id, prod_id, date, status

**7\. Uygulama Yol Haritası (Roadmap)**

1.  **Hafta 1:** SQLAlchemy modellerinin kurulması ve SQLite veritabanı bağlantısı.
2.  **Hafta 2:** heapq tabanlı öncelik kuyruğu ve Greedy algoritmasının kodlanması.
3.  **Hafta 3:** Harita modülünün (marker ekleme) ve ana kullanıcı arayüzünün tasarımı.
4.  **Hafta 4:** Pandas ile raporlama sistemi, hata yönetimi (try-except) ve testler.

**8\. Sonuç**

"Askıda Yemek" projesi, gıda yönetimini algoritmik bir temele oturtarak sadece bir veri yönetimi değil, aynı zamanda etik bir çözüm sunmaktadır. SQLite ve SQLAlchemy kullanımı, sistemin farklı platformlarda kolayca çalıştırılabilmesini garanti eder.