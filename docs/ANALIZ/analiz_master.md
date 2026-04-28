# Askıda Yemek (Food-Bridge) Web - Gereksinim Analizi Master Dosyası

**İlerleme Durumu:** Round 2/10 | Tamamlanma: 15/20 (%75)

## 📌 Netleşen Gereksinimler (PROJECT_GAP_QUESTIONS.md'den)
Senin verdiğin yanıtlara göre şu konuları **kilitledik ve onayladık**:
- **Platform:** Sadece Web (Masaüstü yok).
- **Roller:** Owner, User, Admin, Guest (Hepsi var). Guest haritayı görebilir. İçeriden kayıt olunabilecek.
- **Restoran Yönetimi:** Bir Owner birden fazla restoran yönetebilecek.
- **Eşleştirme:** 15 dk talep süresi, ilk taleple başlar. Zaman ağırlığı azalır. Bir kullanıcı en fazla 4 ürün seçebilir. 1 porsiyon alır, miktar 1 düşer. Aynı kullanıcı aynı ürüne birden fazla talep açamaz.
- **Otomasyon:** Arka planda çalışan basit bir zamanlayıcı (Scheduler) ile SKT ve Batch Matching otomatik tetiklenecek.
- **Raporlama:** Tüm metrikler (Gıda kurtarma, CO2, vs) dahil. Admin CSV export yapabilir. "En çok bağış yapılan gün" dinamik hesaplanacak.
- **Harita:** Kullanıcı 5 km yarıçapa göre filtrelenecek. Askıda ürün olan/olmayan restoran filtrelemesi olacak.
- **Güvenlik:** CSRF koruması aktif. Günde maks 3 talep limiti (Rate Limit).
- **Test & Dil:** Unit testler yazılacak, TR/EN dil desteği eklenecek, UI tamamen iyileştirilecek.
- **Veritabanı:** Kurulum kolaylığı ve Docker uyumu nedeniyle `SQLite` ile devam edilecek.

---

## ❓ Yanıt Bekleyen Sorular (Round 2)

Lütfen aşağıdaki soruları `<!-- YANIT: ... -->` bloklarına cevapla. "HTMLL/CSS kesinlikle kullanılmayacak" altın kuralını `.agent/rules/ui-html-css-kurali.md` dosyasına kalıcı olarak ekledim. Bu kuralın pratik uygulamasını netleştirmemiz gerekiyor.

### 1. "Sıfır HTML/CSS" Kuralının Uygulanışı
- [ ] **Soru 1.1:** "Hiç HTML/CSS kullanılmayacak" derken kastettiğin şey; sıfırdan `style.css` yazmayalım, bunun yerine **TailwindCSS** veya **Bootstrap** gibi hazır framework componentleri kullanalım mı? YOKSA hiç HTML tag'i dahi görmeyelim, **Streamlit** veya **Reflex** gibi sadece Python yazarak arayüz çıkaran bir kütüphane mi kullanalım? (Not: Flask + Jinja kararı verilmişti, Jinja yapısı HTML tagleri içerir. Eğer Streamlit vb. kullanırsak Flask'tan vazgeçmemiz gerekebilir).
  <!-- YANIT:  -->

### 2. Harita Altyapısı (Leaflet vs. Alternatifler)
- [ ] **Soru 2.1:** Web haritası (5km çap gösterme, marker ekleme vb.) için ücretsiz ve çok güçlü olan **Leaflet.js** kütüphanesini kullanmayı öneriyorum. Onaylıyor musun? (Aksi takdirde Google Maps API Key gerekecektir).
  <!-- YANIT:  -->

### 3. Çoklu Dil Desteği (TR/EN)
- [ ] **Soru 3.1:** TR/EN dil desteği istedin. Uygulamanın varsayılan (ilk açılış) dili Türkçe mi olsun, İngilizce mi? Kullanıcının tarayıcı dilini mi baz alalım yoksa menüden seçimi zorunlu mu tutalım?
  <!-- YANIT:  -->

### 4. Admin Paneli Yönetimi
- [ ] **Soru 4.1:** Admin kullanıcısı, sistemdeki restoranları veya kullanıcıları manuel olarak silebilsin / banlayabilsin mi? Yoksa Admin sadece raporları görüp izleme mi yapsın?
  <!-- YANIT:  -->

---
*Not: Bu sorular da tamamlandıktan sonra, tam kapsamlı `gereksinim_analizi.md` raporunu ve yazılım mimarisi şemasını çıkararak projeyi kodlamaya (önce tasarım) başlayacağız.*
