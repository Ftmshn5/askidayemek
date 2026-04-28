# 🦅 HAVSAN YAZILIM GELİŞTİRME VE ALTYAPI KILAVUZU

Bu belge, HAVSAN'da yazılım geliştiren mühendisler için **Tek Gerçek Kaynak (Single Source of Truth)** niteliğindedir. Altyapı, Kurulum ve Standartları içerir.

---

## 🏗️ 1. MİMARİ VE ALTYAPI

### ☁️ HAVSAN Cloud (Ana Sunucu)
*   **Panel:** [https://coolify.havsan.cloud](https://coolify.havsan.cloud)
*   **Servisler:**
    *   ✅ **Workflow:** n8n (Otomasyon)
    *   ✅ **DB/Auth:** Supabase (PostgreSQL)

### ☁️ Google Cloud (GCP)
*   **Kullanım:** AI (Vertex AI), Serverless (Apps Script).
*   **Projeler:** `6SIGMA`, `big-five-app`.

### 💻 Geliştirme Ortamı (DOCKER-FIRST)
*   **Kural:** Local bilgisayarda (Host) hiçbir dil (Node, Python) çalıştırılmaz.
*   **Yöntem:** Her proje kendi `docker-compose.yml` dosyasına sahiptir.

## 📖 1.1. ANTIGRAVITY SÖZLÜĞÜ (KAVRAMLAR)

Antigravity IDE'de gördüğünüz terimlerin anlamları ve diskteki yerleri:

*   **RULES (Kurallar)**
    *   **Ne İşe Yarar?:** "Anayasa". Yapay zeka'nın sınırları (Örn: "Türkçe konuş").
    *   **Nerede Bulunur?:** Global (`~/.gemini/GEMINI.md`) ve Local (`.agent/rules/*.md`).

*   **WORKFLOWS (İş Akışları)**
    *   **Ne İşe Yarar?:** "Tarifler". `/komut` ile çalışan süreçler (Örn: `/deploy` gibi).
    *   **Nerede Bulunur?:** Global (`~/.gemini/antigravity/workflows/`) ve Local (`.agent/workflows/`).

*   **SKILLS (Beceriler)**
    *   **Ne İşe Yarar?:** "Yetenekler". Proje tipine göre otomatik devreye giren araçlar.
    *   **Nerede Bulunur?:** Global (`~/.gemini/antigravity/skills/`).

> **Not:** IDE'de gördüğünüz liste, **Global** (PC'nizdeki) ve **Workspace** (Projedeki) dosyaların toplamıdır.
> *   Örn: 2 Global İş Akışı + 2 Proje İş Akışı = Panelde 4 tane görürsünüz.

## ⚙️ 1.2. ANTIGRAVITY ÇALIŞMA MANTIĞI (NASIL ÇALIŞIR?)

HAVSAN Antigravity sistemi, **Hibrit Zeka (Hybrid Intelligence)** prensibiyle çalışır. Bu yapı, hem standartları korur hem de projeye özel esneklik sağlar.

### 🧠 1. Global Zeka (SENİN KİŞİSEL MENTÖRÜN)
Bu katman (`C:\Users\SİZ\.gemini`), sizin bilgisayarınızdaki sabittir. Hangi projeyi açarsanız açın sizinle gelir.
*   **Görevi:** Anayasayı korumak, size teknik öğretmenlik yapmak (Git, Docker anlatmak) ve HAVSAN standartlarını dayatmak.
*   **Örnek:** Yeni proje başlattığınızda devreye giren `havsan-development` becerisi buradadır.

### 📂 2. Yerel Zeka (PROJE HAFIZASI)
Bu katman (`PROJE/.agent`), o anki işe özeldir.
*   **Görevi:** O projenin özel kurallarını (Örn: "Mavi buton kullan") ve operasyonlarını (Örn: "Deploy et") saklamak.
*   **Örnek:** `/deploy` komutu sadece ilgili projede çalışır, çünkü o projenin sunucu ayarlarını bilir.

### 🎓 3. Eğitmen Modu (Teacher Persona)
Sistem sadece kod yazan bir robot değildir. Sizin **"Kıdemli Takım Arkadaşınız"**dır.
*   Bilmediğiniz terimleri açıklar.
*   Hata yapmanızı engeller (Örn: *"Dur! Git push yapmadan analize geçemezsin"*).
*   Sizi gerçek dünya süreçlerine (Müşteri onayı, Saha analizi) zorlar.

---

## 🧠 2. ANTIGRAVITY IDE KURULUMU (ZEKA TRANSFERİ)

Antigravity IDE'nizi "Senior HAVSAN Mühendisi" seviyesine getirmek için, **Atıf Ertuğrul KAN**'dan güncel zeka dosyalarını alıp aşağıdaki ağaç yapısındaki gibi kendi bilgisayarınıza (`C:\Users\SİZ\.gemini`) yerleştiriniz.

### 🌳 Global Zeka Yapısı (Bilgisayarınızda Olması Gereken)

```text
C:\Users\KULLANICI_ADI\.gemini/
│
├── GEMINI.md                              <-- Global kurallar (Anayasa)
│
└── antigravity/
    ├── skills/                            <-- Beceriler
    │   ├── havsan-appsscript/
    │   │   └── SKILL.md
    │   ├── havsan-code-review/
    │   │   └── SKILL.md
    │   └── havsan-development/
    │       ├── SKILL.md
    │       ├── examples/
    │       └── resources/
    │
    ├── workflows/                         <-- İş akışları
    │   ├── analist.md
    │   ├── backend-architect.md
    │   ├── dagitim-paketi-guncelle.md
    │   └── frontend-design.md
    │
    └── [diğer sistem klasörleri]          <-- brain, code_tracker, etc.
                                               (Bunları kopyalamayın)
```

> **Not:** `brain`, `code_tracker`, `conversations` gibi klasörler Antigravity'nin çalışma dosyalarıdır. Bunları dağıtım paketine eklemeyin.

### 🔄 Kritik Adım: Ayarları Aktifleştirme (Customizations)
Zeka dosyalarını (Rules, Skills, Workflows) yerine koyduktan sonra, Antigravity'nin bunları okuyabilmesi için:

1.  Antigravity IDE'de sağ üst köşedeki **üç nokta (⋮)** ikonuna tıklayın.
2.  **Customizations** seçeneğine tıklayın.
3.  Bu işlem, diskteki yeni kuralları ve yetenekleri sisteme yükleyecektir. Bunu yapmazsanız zeka eski ayarlarla çalışır.

### 🤖 Önemli: Model Seçimi
HAVSAN projeleri için **en iyi performansı** almak için:

1.  Sağ üst köşedeki model seçim menüsünden **"Claude Sonnet 4.5 (Thinking)"** modelini seçin.
2.  Bu model, kompleks analiz, planlama ve kod yazma görevlerinde en yüksek başarıyı gösterir.

> **Not:** "Thinking" modu, sistemin kararlarını daha detaylı düşünmesini sağlar ve hata oranını düşürür.

---

## 🎁 2.1. DAĞITIM PAKETİNDEN KURULUM (Ekip İçin)

Eğer size **HAVSAN_Antigravity_Dagitim_Paketi.rar** dosyası gönderildiyse, kurulum çok basit:

### Adım 1: RAR Dosyasını Çıkart
1.  RAR dosyasını herhangi bir klasöre çıkartın (Örn: Masaüstü)
2.  İçinden `DAGITIM_PAKETI` klasörünü göreceksiniz

### Adım 2: Dosyaları Kopyala
1.  `DAGITIM_PAKETI` klasöründeki **`.gemini`** klasörünü kopyalayın
2.  Aşağıdaki konuma yapıştırın:
    ```
    C:\Users\KULLANICI_ADI\
    ```
3.  **Önemli:** Mevcut `.gemini` klasörünüz varsa, üzerine yazmasına izin verin (veya önce yedekleyin)

### Adım 3: Antigravity'yi Yenile
1.  Antigravity IDE'yi açın (veya zaten açıksa kapatıp yeniden açın)
2.  Sağ üst köşedeki **⋮** (üç nokta) menüsüne tıklayın
3.  **Customizations** seçeneğine tıklayın
4.  IDE'yi tamamen kapatıp yeniden açın

### Adım 4: Model Seçimi
1.  Sağ üst köşeden model seçim menüsünü açın
2.  **"Claude Sonnet 4.5 (Thinking)"** modelini seçin

### Adım 5: Test Et
1.  Yeni bir proje klasörü açın
2.  Chat'e şunu yazın:
    ```
    Merhaba! Yeni bir HAVSAN projesi başlatıyorum...
    ```
3.  Sistem size adınızı sorup analiz sürecini başlatmalı

**Tebrikler! HAVSAN Antigravity kurulumu tamamlandı.** 🎉


---

## 📂 3. PROJE STANDARTLARI

Her proje başlatıldığında (`git init` sonrası) projenin kök dizini şu standart yapıya sahip olmalıdır:

```text
PROJE_ADI/
│
├── .agent/                       <-- (PROJEYE ÖZEL AYARLAR)
│   ├── rules/
│   │   └── docker-clasp.md       (Örn: Bu projede Clasp zorunlu)
│   └── workflows/
│       └── deploy.md             (Örn: Bu projeyi deploy et)
│
├── docs/                         <-- (DOKÜMANTASYON)
│   ├── ANALIZ/
│   │   ├── PRD.md                (ZORUNLU: Koddan önce bu yazılır)
│   │   └── Gereksinimler.md
│   └── ...
│
├── frontend/                     <-- (ÖNCE BURASI BİTER)
│   └── ...
│
├── backend/                      <-- (FRONTEND BİTMEDEN AÇILMAZ)
│   └── ...
│
└── docker-compose.yml            <-- (ZORUNLU: Çalışma Motoru)
```

### 🧠 3.1. Projeye Özel Kural Ekleme (Memory)
Geliştirici olarak projeye özel kalıcı bir kural eklemek istediğinizde (Örn: "Bu projede asla jQuery kullanma"), karmaşık dosya işlemleriyle uğraşmanıza gerek yoktur.

1.  **Söyle:** Chat ekranına gelip sadece şöyle deyin:
    > *"Bu projede renk paleti olarak sadece pastel tonlar kullanılacak. Bunu kural olarak kaydet."*
2.  **Otomatik İşlem:** Global Zeka (`GEMINI.md`), bu emrinizi algılar ve `.agent/rules/tasarim-kurallari.md` gibi bir dosyayı sizin yerinize oluşturur.
3.  **Kontrol:** Sağ üstteki **Customizations > Rules > Workspace** sekmesinden yeni kuralınızı görebilirsiniz.


---

## 🚀 4. YENİ PROJE BAŞLATMA PROMPTU (ÖNERİLEN)

Yeni bir projeye başlarken **bu promptu kullanmanız önerilir**. Bu, tüm HAVSAN protokollerini aktive eder:

```
Merhaba! Yeni bir HAVSAN projesi başlatıyorum ve HAVSAN standartlarına tam uyum sağlamak istiyorum.

Önce tanışalım: Adım ne diye sormak ister misin? 😊

**İTERATİF ANALİZ SİSTEMİ:**

1. **TEK BELGE ÜZERİNDEN ÇALIŞALIM:**
   - `analiz_master.md` adında tek bir dosya oluştur
   - Tüm sorular bu dosyada checkbox formatında (- [ ] soru)
   - Yanıtları bu dosyada toplayayım (yorum yazarak)

2. **YANIT YÖNTEMİM:**
   - IDE'de soruların yanına yorum yazacağım
   - Tüm soruları birden yanıtlamak zorunda DEĞİLİM (4 soru yanıtlayıp göndersem de olur)
   - Sen yorumları okuyup:
     - Yanıtlanan soruları [x] işaretle
     - Yanıtları soruların altına KALICI olarak yaz (→ **YANIT:** "...")
     - Böylece eski yanıtlarımı görebilirim
     - gereksinim_analizi.md (sadece %100 olunca) güncelle
     - musteri_gorusme_sorulari.md (açık sorular) güncelle

3. **İTERATİF İLERLEME:**
   - Yanıtlarıma göre YENİ sorular üret
   - Eksik noktaları tespit et
   - Sonraki round sorularını AYNI dosyaya ekle
   - Eksik nokta kalmayana kadar devam et (5-10 round)

4. **İLERLEME TAKİBİ:**
   - Her round başında: "Round X/10, Tamamlanma: Y/Z (%ABC)"
   - Checkbox'larla ilerlemeyi göster

**BAŞLAYALIM:**
- Minimum 15-20 derinlemesine soru sor
- Ben yanıtladıkça ilerleyelim, sakin sakin
- Analiz %100 tamamlanmadan frontend'e GEÇMEYELİM
- Git deposunu oluşturalım ve güvenli bir şekilde push edelim
- Docker, teknoloji seçimi gibi konuları analiz bittikten sonra konuşalım

Hazırım, başlayalım!
```

> **Not:** Bu prompt, IDE yorumlarıyla yanıt verme imkanı sağlar ve iteratif olarak derinleşir.

---

## � 5. EK KAYNAKLAR VE DESTEK

### 📖 İlgili Belgeler
*   **Teknik Detaylar:** `HAVSAN_ANTIGRAVITY_KURULUM.md` - Daha detaylı kurulum adımları
*   **Proje Şablonları:** `~/.gemini/antigravity/skills/havsan-development/examples/`

### 🆘 Sık Karşılaşılan Sorunlar

**Problem:** "Customizations yeniledim ama yeni kurallar görünmüyor"  
**Çözüm:** Antigravity IDE'yi tamamen kapatıp yeniden açın.

**Problem:** "Git push sırasında 'pull first' hatası"  
**Çözüm:** GitHub'da **BOŞ (Empty)** repo oluşturun, README/License eklemeyin.

**Problem:** "Yapay zeka teknolojilerden bahsediyor, analiz yapmıyor"  
**Çözüm:** Bölüm 4'teki başlangıç promptunu aynen kullanın.

**Problem:** "Yapay zeka adımı sormuyor"  
**Çözüm:** Promptta "Önce tanışalım" kısmını mutlaka ekleyin.

### 📞 Destek
Sorularınız için: **Atıf Ertuğrul KAN**

---

**Son Güncelleme:** 2026-01-17  
**Versiyon:** 2.0 - Antigravity Protokolleri Entegre Edildi
