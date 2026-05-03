---

## 🧭 İnteraktif Dokümantasyon (Swagger / Postman)

- `openapi.yaml` dosyası proje kökünde üretildi. Bu spec'i kullanarak Swagger UI veya ReDoc ile interaktif dokümantasyon çalıştırabilirsiniz.

- Lokal olarak Swagger UI çalıştırmak için (docker-compose):

```bash
docker compose -f docker-compose.swagger.yml up -d
# Swagger UI → http://localhost:8080
```

- Postman kullanmak isterseniz, `askida_yemek_postman_collection.json` dosyasını Postman'a içe aktarabilirsiniz.

Dosyalar:

- [openapi.yaml](openapi.yaml)
- [docker-compose.swagger.yml](docker-compose.swagger.yml)
- [askida_yemek_postman_collection.json](askida_yemek_postman_collection.json)

# Askıda Yemek (Food Bridge) - API Dokümantasyonu

**Versiyon:** 1.0.0  
**Son Güncelleme:** Mayıs 2026  
**Framework:** Flask 3.1.0  
**Veritabanı:** SQLAlchemy 2.0.36  

---

## 📋 İçindekiler

1. [Giriş](#giriş)
2. [Kimlik Doğrulama](#kimlik-doğrulama)
3. [API Endpoints](#api-endpoints)
   - [Kimlik Doğrulama Endpoints](#kimlik-doğrulama-endpoints)
   - [Kullanıcı Endpoints](#kullanıcı-endpoints)
   - [Restoran Endpoints](#restoran-endpoints)
   - [Ürün Endpoints](#ürün-endpoints)
   - [İşlem/Talep Endpoints](#işlemtalep-endpoints)
4. [Veri Modelleri](#veri-modelleri)
5. [Hata Kodları](#hata-kodları)
6. [Örnekler](#örnekler)

---

## 🎯 Giriş

**Askıda Yemek**, Elazığ'daki ihtiyaç sahibi bireylerle sorun çözümü yaklaşan yemekleri bağlayan bir sosyal yardımlaşma platformudur.

### Temel Özellikler
- **İki Rol Sistemi:** Restoran Sahipleri ve İhtiyaç Sahipleri
- **Coğrafi Eşleştirme:** OpenStreetMap ile harita tabanlı restoran keşfi
- **Dinamik Öncelik Skoru:** Kullanıcı tipi ve zamanı göz önüne alan algoritma
- **PIN Doğrulama:** Güvenli teslimat teslim alma işlemi
- **Etki Raporlama:** CSV dışa aktarma ve istatistik

### Sistem Özellikleri
- **Otomatik SKT Kontrolü:** 5 dakikada bir süresi yaklaşan ürünler askıya alınır
- **Toplu Eşleştirme:** 1 dakikada bir greedy algoritması ile talepler eşleştirilir
- **Günlük İstek Limiti:** Anti-spam için kullanıcı başına 3 restoran talebi/gün
- **Çoklu Dil Desteği:** Türkçe ve İngilizce

---

## 🔐 Kimlik Doğrulama

Uygulama Flask-Login ve session tabanlı kimlik doğrulama kullanmaktadır.

### Login Gerekmesi
- **`@login_required` Dekoratörü:** Endpoint korunmak için kullanılır
- **Rol Kontrolü:** Endpoint'te `current_user.role` ile izin kontrol edilir
  - `'owner'` - Restoran Sahibi
  - `'user'` - İhtiyaç Sahibi / Kullanıcı

### Login Akışı
1. Kullanıcı `/login` endpoint'ine POST isteği gönderir
2. Başarılı giriş sonrası `current_user` context'inde kullanılabilir
3. `/logout` ile session temizlenir

---

## 📡 API Endpoints

### Kimlik Doğrulama Endpoints

#### 1. Giriş Yap (Login)
```
POST /login
Content-Type: application/x-www-form-urlencoded
```

**Request Body (Form Data):**
```
username=ahmet_yilmaz
password=123456
role=user
```

**Response (Başarılı):**
- HTTP 302 (Redirect)
- `Location: /user/dashboard` (kullanıcı) veya `/owner/dashboard` (owner)

**Response (Başarısız):**
- HTTP 200
- Flash mesajı: "Kullanıcı adı veya şifre hatalı!"
- Sayfa yeniden `/login` template'ini render'lar

**Hata Durumları:**
- Geçersiz kullanıcı adı
- Hatalı şifre
- Rol uyumsuzluğu

---

#### 2. Kayıt Ol (Register)
```
POST /register
Content-Type: application/x-www-form-urlencoded
```

**Request Body (Form Data):**
```
full_name=Ahmet Yılmaz
username=ahmet_yilmaz
password=123456
role=user
# Eğer role='owner' ise:
restaurant_name=Lezzet Sofrası
```

**Response (Başarılı):**
- HTTP 302 → `/login`
- Flash: "Kayıt başarılı! Şimdi giriş yapabilirsiniz."

**Response (Başarısız):**
- HTTP 200
- Flash: "Bu kullanıcı adı zaten alınmış."

**Notlar:**
- Restoran için `restaurant_name` gönderilirse otomatik restoran oluşturulur
- Koordinatlar rastgele Elazığ merkezi etrafında belirlenir
- Şifre hash'lenerek saklanır (Werkzeug)

---

#### 3. Çıkış Yap (Logout)
```
GET /logout
```

**Gereklilik:** `@login_required`

**Response:**
- HTTP 302 → `/login`
- Session temizlenir

---

### Kullanıcı (İhtiyaç Sahibi) Endpoints

#### 4. Kullanıcı Dashboard
```
GET /user/dashboard
```

**Gereklilik:** `@login_required`, `current_user.role == 'user'`

**Response:** HTML Template (`user/dashboard.html`)
- OpenStreetMap harita
- Restoran marker'ları
- Ürün seçim modalı

**Parametreler:**
- Hiçbir query/path parametresi yok (session'dan kullanıcı bilgisi alınır)

---

#### 5. Kullanıcı Profili
```
GET /user/profile
```

**Gereklilik:** `@login_required`, `current_user.role == 'user'`

**Response:** HTML Template (`user/profile.html`)

**Döndürülen Veriler:**
- `total_requests`: Toplam talep sayısı
- `active_transactions`: Teslim bekleyen talepler (matched durumunda)
- `completed_transactions`: Puanlanmamış teslim alınmış işlemler

**Kontrol Akışı:**
- Eğer role != 'user' → `/owner/dashboard` yönlendir

---

#### 6. Kullanıcı Etki Raporu
```
GET /user/report
```

**Gereklilik:** `@login_required`, `current_user.role == 'user'`

**Response:** HTML Template (`user/report.html`)

**Döndürülen İstatistikler (stats):**
- Kullanıcı bazlı etki verileri
- Eşleştirme başarı oranları
- İşlem geçmişi

**Çağrılan Algoritma:**
```python
stats = get_impact_stats(user_id=current_user.id)
```

---

#### 7. Konuk Dashboard
```
GET /guest/dashboard
```

**Gereklilik:** Yok (Açık erişim)

**Response:** HTML Template (`user/dashboard.html`, `is_guest=True`)

**Not:** SKT süresi yaklaşan ürünler otomatik askıya alınır

---

### Restoran Sahibi (Owner) Endpoints

#### 8. Restoran Dashboard
```
GET /owner/dashboard
```

**Gereklilik:** `@login_required`, `current_user.role == 'owner'`

**Response:** HTML Template (`owner/dashboard.html`)

**Döndürülen Veriler:**
- `restaurant`: Restoran bilgileri
- `products`: Tüm ürünler (SKT'ye göre sıralanmış)
- `stats`: İstatistikler
  - `total_products`: Toplam ürün sayısı
  - `suspended_count`: Askıda olan ürün sayısı
  - `today_donations`: Bugün eşleştirilen talep sayısı
  - `critical_skt`: 6 saate kadar SKT olan ürünler
- `pending_transactions`: Teslimat bekleme talepler

---

#### 9. Restoran Profili
```
GET /owner/profile
```

**Gereklilik:** `@login_required`, `current_user.role == 'owner'`

**Response:** HTML Template (`owner/profile.html`)

**Döndürülen Veriler:**
- `restaurant`: Restoran bilgileri
- `total_donations`: Toplam başarılı bağış sayısı

---

#### 10. Restoran Etki Raporu
```
GET /owner/report
```

**Gereklilik:** `@login_required`, `current_user.role == 'owner'`

**Response:** HTML Template (`owner/report.html`)

**Döndürülen Veriler:**
- `stats`: Restoran bazlı etki istatistikleri
- `restaurant`: Restoran bilgileri

---

#### 11. Ürün Ekle
```
POST /owner/product/add
Content-Type: application/x-www-form-urlencoded
```

**Gereklilik:** `@login_required`, `current_user.role == 'owner'`

**Request Body (Form Data):**
```
name=Kızartılmış Tavuk                    (String, zorunlu)
quantity=5                                 (Integer, varsayılan: 1)
original_price=50.00                       (Float, varsayılan: 0)
price=0                                    (Float, varsayılan: 0)
skt_date=2026-05-04                        (YYYY-MM-DD formatı, zorunlu)
status=on_sale                             (on_sale | suspended, varsayılan: on_sale)
```

**Response (Başarılı):**
- HTTP 302 → `/owner/dashboard`
- Flash: `"Kızartılmış Tavuk başarıyla eklendi!"`

**Response (Başarısız):**
- HTTP 302 → `/owner/dashboard`
- Flash: "Ürün adı ve SKT zorunludur!" (eksik alanlar için)
- Flash: "Geçersiz tarih formatı!" (yanlış tarih)

**Validasyonlar:**
- `name` ve `skt_date` zorunlu
- Tarih formatı: `YYYY-MM-DD`
- `status` sadece `on_sale` veya `suspended` olabilir

---

#### 12. Ürün Durumunu Değiştir (Toggle)
```
POST /owner/product/toggle/<product_id>
```

**Gereklilik:** `@login_required`, `current_user.role == 'owner'`

**Path Parametreleri:**
```
product_id = 42 (Integer, ürün ID)
```

**Response (Başarılı):**
- HTTP 302 → `/owner/dashboard`
- Flash: `"Ürün Adı askıya alındı."` (status: `on_sale` → `suspended`)
- Flash: `"Ürün Adı satışa alındı."` (status: `suspended` → `on_sale`)

**Response (Başarısız):**
- HTTP 302 → `/owner/dashboard`
- Flash: "Bu ürünü değiştirme yetkiniz yok!" (yetki hatası)

**İş Mantığı:**
- `on_sale` → `suspended`: Ürün askıya alınır, ihtiyaç sahiplerine açılır
- `suspended` → `on_sale`: Askıya alınan ürün satışa geri alınır

---

#### 13. Ürün Sil
```
POST /owner/delete_product/<product_id>
```

**Gereklilik:** `@login_required`, `current_user.role == 'owner'`

**Path Parametreleri:**
```
product_id = 42 (Integer)
```

**Response (Başarılı):**
- HTTP 302 → `/owner/dashboard`
- Flash: "Ürün silindi."

**Response (Başarısız):**
- HTTP 404: Ürün bulunamadı
- HTTP 302 → `/owner/dashboard`, Flash: "Yetkisiz işlem."

---

#### 14. PIN Doğrula (Teslimat)
```
POST /owner/verify_pin
Content-Type: application/x-www-form-urlencoded
```

**Gereklilik:** `@login_required`, `current_user.role == 'owner'`

**Request Body (Form Data):**
```
transaction_id=15                          (Integer, işlem ID)
pin_code=4825                              (String, PIN kodu)
```

**Response (Başarılı):**
- HTTP 302 → `/owner/dashboard`
- Flash: "PIN Doğrulandı! Teslimat başarılı, kullanıcıya +10 Güven Puanı eklendi."
- İşlem durumu: `pending` → `completed`
- Ürün durumu: `matched` → `completed`
- Kullanıcı puanı: +10

**Response (Başarısız):**
- HTTP 302 → `/owner/dashboard`
- Flash: "Geçersiz istek." (eksik parametreler)
- Flash: "Yetkisiz işlem." (yanlış restoran)
- Flash: "Bu işlem teslimat bekleyen durumunda değil." (yanlış durum)
- Flash: "Hatalı PIN kodu!" (PIN eşleşmiyor)

---

### Ürün Endpoints

#### 15. Restoran Ürünlerini Listele (API)
```
GET /api/products/<restaurant_id>
```

**Gereklilik:** Yok (Açık erişim)

**Path Parametreleri:**
```
restaurant_id = 1 (Integer, restoran ID)
```

**Response (Başarılı):**
```json
{
  "restaurant": {
    "id": 1,
    "name": "Lezzet Sofrası",
    "rating": 4.5,
    "address": "Elazığ Merkez"
  },
  "products": [
    {
      "id": 42,
      "name": "Kızartılmış Tavuk",
      "quantity": 5,
      "original_price": 50.0,
      "price": 0.0,
      "skt_date": "2026-05-04 15:30"
    }
  ],
  "queue_count": 2
}
```

**Response (Başarısız):**
- HTTP 404: Restoran bulunamadı

**Not:** Sadece `status='suspended'` ürünler listelenir (askıdaki yemekler)

---

### İşlem/Talep Endpoints

#### 16. Tüm Restoranları Listele (API)
```
GET /api/restaurants
```

**Gereklilik:** Yok (Açık erişim)

**Query Parametreleri:** Hiçbiri

**Response (Başarılı):**
```json
[
  {
    "id": 1,
    "name": "Lezzet Sofrası",
    "lat": 38.6748,
    "lon": 39.1920,
    "rating": 4.5,
    "address": "Elazığ Merkez",
    "suspended_count": 3,
    "has_suspended": true
  }
]
```

**Amaç:** Harita için marker veri sağlamak

---

#### 17. Talep Oluştur (API)
```
POST /api/request
Content-Type: application/json
```

**Gereklilik:** `@login_required`, `current_user.role == 'user'`

**Request Body (JSON):**
```json
{
  "product_ids": [42, 45, 48]
}
```

**Response (Başarılı):**
```json
{
  "success": true,
  "message": "3 ürün için talep oluşturuldu.",
  "transactions": [
    {
      "id": 42,
      "name": "Kızartılmış Tavuk",
      "priority_score": 85.5
    }
  ],
  "matched_count": 0
}
```

**Response (Başarısız):**
```json
{
  "error": "En az bir ürün seçmelisiniz"
}
```

**HTTP Durumları:**
- 200: Başarılı
- 400: Geçersiz istek (örn: 3'ten fazla ürün)
- 403: Yetkiniz yok

**Validasyonlar:**
- En az 1 ürün seçilmeli
- En fazla 3 ürün seçilebilir
- Günlük 3 restoran talep limiti
- Aynı ürüne iki kez talep verilemez

**İş Mantığı:**
1. Kullanıcı tarafından seçilen ürünler kontrol edilir
2. Ürün `status='suspended'` olmalı
3. Her ürün için Öncelik Skoru hesaplanır (kullanıcı tipi + saat)
4. `Transaction` kaydı oluşturulur (`status='pending'`)
5. Toplama süresi: 15 dakika
6. Periyodik batch matching sonra eşleştirme yapılır

---

#### 18. İşlemi Puanla (API)
```
POST /api/rate_transaction
Content-Type: application/json
```

**Gereklilik:** `@login_required`, `current_user.role == 'user'`

**Request Body (JSON):**
```json
{
  "transaction_id": 15,
  "rating": 5
}
```

**Response (Başarılı):**
```json
{
  "success": true,
  "message": "Puanınız kaydedildi, +5 Güven Puanı kazandınız!"
}
```

**Response (Başarısız):**
```json
{
  "error": "Eksik veri"
}
```

**HTTP Durumları:**
- 200: Başarılı
- 400: Geçersiz puan (1-5 aralığı dışında)
- 403: Yetkiniz yok
- 404: İşlem bulunamadı

**Validasyonlar:**
- Puan 1-5 aralığında olmalı
- İşlem `status='completed'` olmalı
- Aynı işlem iki kez puanlanamaz

**Ödüller:**
- Puan verdiği için: +5 Güven Puanı

---

#### 19. CSV Dışa Aktarma (API)
```
GET /api/export/csv
```

**Gereklilik:** `@login_required`

**Query Parametreleri:** Hiçbiri

**Response (Başarılı):**
```
HTTP 200
Content-Type: text/csv; charset=utf-8-sig
Content-Disposition: attachment; filename=askida_yemek_rapor.csv
```

**CSV Yapısı:**
```csv
İşlem ID,Tarih,Kullanıcı,Restoran,Ürün,Miktar,Öncelik Skoru,Durum,Eşleşme Tarihi
1,2026-05-03 14:30,Ahmet Yılmaz,Lezzet Sofrası,Kızartılmış Tavuk,5,85.5,completed,2026-05-03 14:35
```

**Veri Filtresi:**
- Owner: Kendi restoranının işlemleri
- User: Kendi işlemleri
- Durum: Sadece `matched` ve `completed`

**Gerekli Kütüphaneler:**
```python
import pandas as pd
import io
```

---

### Dil (Localization) Endpoints

#### 20. Dil Değiştir
```
GET /set_lang/<lang_code>
```

**Gereklilik:** Yok (Açık erişim)

**Path Parametreleri:**
```
lang_code = 'tr' | 'en'
```

**Response:**
- HTTP 302 → Önceki sayfa (referrer)
- Session'a `lang` kaydedilir

**Çeviriler:** `translations.json` dosyasından yüklenir

---

## 📊 Veri Modelleri

### User (Kullanıcı)
```python
{
  "id": 1,
  "username": "ahmet_yilmaz",
  "full_name": "Ahmet Yılmaz",
  "role": "user" | "owner",
  "user_type": "student" | "disabled" | "pregnant" | "standard",
  "points": 0,
  "created_at": "2026-05-03T14:30:00Z"
}
```

**Rol Tanımları:**
- `user`: İhtiyaç Sahibi (talep oluşturabilen)
- `owner`: Restoran Sahibi (ürün ekleyebilen)

**Kullanıcı Tipi Ağırlıkları (Öncelik Skoru):**
- `pregnant`: 100 (Hamile)
- `disabled`: 100 (Engelli)
- `student`: 80 (Öğrenci)
- `standard`: 50 (Standart)

---

### Restaurant (Restoran)
```python
{
  "id": 1,
  "owner_id": 2,
  "name": "Lezzet Sofrası",
  "latitude": 38.6748,
  "longitude": 39.1920,
  "address": "Elazığ Merkez",
  "created_at": "2026-05-03T14:30:00Z",
  "rating": 4.5,
  "total_products": 10
}
```

**Özellikler:**
- `rating`: İşlemlerden alınan puanların ortalaması (varsayılan: 4.0)
- `suspended_count`: Askıda olan ürün sayısı
- `total_products`: Toplam ürün sayısı

---

### Product (Ürün)
```python
{
  "id": 42,
  "restaurant_id": 1,
  "name": "Kızartılmış Tavuk",
  "quantity": 5,
  "original_price": 50.0,
  "price": 0.0,
  "skt_date": "2026-05-04T15:30:00Z",
  "status": "on_sale" | "suspended" | "matched" | "completed",
  "created_at": "2026-05-03T14:30:00Z"
}
```

**Durum Adımları:**
1. `on_sale`: Satışta (ön tarafta gizli)
2. `suspended`: Askıda/Bağış (kullanıcılara açık)
3. `matched`: Eşleştirildi (talep onaylandı)
4. `completed`: Teslim edildi (PIN ile doğrulı)

---

### Transaction (İşlem/Talep)
```python
{
  "id": 15,
  "user_id": 1,
  "product_id": 42,
  "restaurant_id": 1,
  "priority_score": 85.5,
  "status": "pending" | "matched" | "completed" | "cancelled",
  "user_rating": 5,
  "pin_code": "4825",
  "created_at": "2026-05-03T14:30:00Z",
  "matched_at": "2026-05-03T14:35:00Z",
  "completed_at": "2026-05-03T15:30:00Z"
}
```

**Durum Akışı:**
1. `pending`: Talep beklemede (15 dakikalık toplama süresi)
2. `matched`: Eşleştirildi (talep onaylandı)
3. `completed`: Teslim edildi + PIN doğrulı
4. `cancelled`: İptal edildi

**PIN Kodu:**
- Sistem tarafından otomatik generate edilir
- Teslimat sırasında restoran tarafından doğrulanır
- Başarılı PIN → +10 Güven Puanı

---

## ⚠️ Hata Kodları

| HTTP Kodu | Anlamı | Örnek |
|-----------|--------|-------|
| 200 | OK - Başarılı | İstek başarılı işlendi |
| 302 | Redirect | Form gönderimi sonrası yönlendirme |
| 400 | Bad Request | Geçersiz veri / Eksik parametreler |
| 403 | Forbidden | Yetkiniz yok (rol kontrol hatası) |
| 404 | Not Found | Kayıt bulunamadı |
| 500 | Server Error | Beklenmeyen hata |

**Hata Mesajları (Flash):**
```
- "Kullanıcı adı veya şifre hatalı!"
- "Bu kullanıcı adı zaten alınmış."
- "Ürün adı ve SKT zorunludur!"
- "Geçersiz tarih formatı!"
- "Hatalı PIN kodu!"
- "En az bir ürün seçmelisiniz"
- "Günlük maksimum 3 restoran talep limitine ulaştınız."
```

---

## 📚 Örnekler

### Örnek 1: Kullanıcı Kayıt ve Login

**1. Kayıt:**
```bash
curl -X POST http://localhost:5000/register \
  -d "full_name=Ahmet Yılmaz" \
  -d "username=ahmet_yilmaz" \
  -d "password=123456" \
  -d "role=user"
```

**2. Login:**
```bash
curl -X POST http://localhost:5000/login \
  -d "username=ahmet_yilmaz" \
  -d "password=123456" \
  -d "role=user" \
  -c cookies.txt
```

**3. Dashboard Erişim:**
```bash
curl -b cookies.txt http://localhost:5000/user/dashboard
```

---

### Örnek 2: Ürün Ekleme ve Yönetim

**1. Restoran Sahibi Kayıt:**
```bash
curl -X POST http://localhost:5000/register \
  -d "full_name=Mehmet Şef" \
  -d "username=mehmet_chef" \
  -d "password=123456" \
  -d "role=owner" \
  -d "restaurant_name=Lezzet Sofrası"
```

**2. Login:**
```bash
curl -X POST http://localhost:5000/login \
  -d "username=mehmet_chef" \
  -d "password=123456" \
  -d "role=owner" \
  -c cookies.txt
```

**3. Ürün Ekle:**
```bash
curl -X POST http://localhost:5000/owner/product/add \
  -b cookies.txt \
  -d "name=Kızartılmış Tavuk" \
  -d "quantity=5" \
  -d "original_price=50" \
  -d "price=0" \
  -d "skt_date=2026-05-04" \
  -d "status=on_sale"
```

**4. Ürün Durumunu Değiştir (Askıya Al):**
```bash
curl -X POST http://localhost:5000/owner/product/toggle/42 \
  -b cookies.txt
```

---

### Örnek 3: Talep Oluştur ve Eşleştir

**1. Tüm Restoranları Al (Harita):**
```bash
curl http://localhost:5000/api/restaurants | jq
```

**Yanıt:**
```json
[
  {
    "id": 1,
    "name": "Lezzet Sofrası",
    "lat": 38.6748,
    "lon": 39.1920,
    "rating": 4.5,
    "suspended_count": 3,
    "has_suspended": true
  }
]
```

**2. Restoran Ürünlerini Al:**
```bash
curl http://localhost:5000/api/products/1 | jq
```

**Yanıt:**
```json
{
  "restaurant": {
    "id": 1,
    "name": "Lezzet Sofrası",
    "rating": 4.5,
    "address": "Elazığ Merkez"
  },
  "products": [
    {
      "id": 42,
      "name": "Kızartılmış Tavuk",
      "quantity": 5,
      "original_price": 50.0,
      "price": 0.0,
      "skt_date": "2026-05-04 15:30"
    }
  ],
  "queue_count": 2
}
```

**3. Talep Oluştur:**
```bash
curl -X POST http://localhost:5000/api/request \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"product_ids": [42, 45]}'
```

**Yanıt:**
```json
{
  "success": true,
  "message": "2 ürün için talep oluşturuldu.",
  "transactions": [
    {
      "id": 42,
      "name": "Kızartılmış Tavuk",
      "priority_score": 85.5
    }
  ],
  "matched_count": 0
}
```

---

### Örnek 4: PIN ile Teslimat

**1. Owner Dashboard'dan Bekleyen Taleplerini Görür**
- `/owner/dashboard` → pending_transactions listesi

**2. PIN Doğrulama:**
```bash
curl -X POST http://localhost:5000/owner/verify_pin \
  -b cookies.txt \
  -d "transaction_id=15" \
  -d "pin_code=4825"
```

**Yanıt (Başarılı):**
- Flash: "PIN Doğrulandı! Teslimat başarılı, kullanıcıya +10 Güven Puanı eklendi."
- Transaction: `pending` → `completed`
- User.points: +10

---

### Örnek 5: CSV Dışa Aktarma

```bash
curl http://localhost:5000/api/export/csv \
  -b cookies.txt \
  -o askida_yemek_rapor.csv
```

**CSV İçeriği:**
```csv
İşlem ID,Tarih,Kullanıcı,Restoran,Ürün,Miktar,Öncelik Skoru,Durum,Eşleşme Tarihi
1,2026-05-03 14:30,Ahmet Yılmaz,Lezzet Sofrası,Kızartılmış Tavuk,5,85.5,completed,2026-05-03 14:35
2,2026-05-03 15:00,Fatma Can,Lezzet Sofrası,Pide,3,92.0,matched,2026-05-03 15:05
```

---

## 🛠️ Teknik Detaylar

### Otomatik Scheduler (Arka Plan İşleri)

```python
BackgroundScheduler()
- Job 1: auto_suspend_expiring_products() → Aralık: 5 dakika
  * Süresi 6 saat içinde biten ürünleri `suspended` durumuna alır
  
- Job 2: run_batch_matching() → Aralık: 1 dakika
  * Pending talepleri greedy algoritması ile eşleştirir
  * Talepler priority_score'a göre sıralanır
```

### Öncelik Skoru Hesaplaması

```
Priority Score = Base Score + (User Type Weight * 1.2) + Time Bonus

Base Score: 50
User Type Weight: 50-100 (student: 80, disabled: 100, vb.)
Time Bonus: Saat başına artan değer
```

### Anti-Spam Mekanizması

- Kullanıcı başına günde en fazla 3 restoran talebi
- Aynı ürüne iki kez talep verilemez
- Başarısız talepler spam sayılmaz

---

## 🌐 Ortam Değişkenleri

```bash
FLASK_ENV=development          # development | production
DEBUG=True                     # Debug modu
DATABASE_URL=sqlite:///...     # Veritabanı URI
SECRET_KEY=your-secret-key     # Flask secret key
```

---

## 📝 Notlar

- Tüm tarihler **UTC Timezone** ile saklanır
- API endpoint'ler session tabanlı kimlik doğrulama kullanır (cookie)
- Güvenlik için HTTPS önerilir (production ortamı)
- CORS ayarları gerekirse config.py'de yapılandırılabilir

---

## 📞 Destek

Sorular ve sorunlar için lütfen teknik rapor ve wireframe'leri referans alınız:
- **Teknik Rapor:** `ASKIDA YEMEK TEKNİK RAPOR.md`
- **Wireframe:** `wireframe_output.txt`
- **Analiz:** `docs/ANALIZ/`
