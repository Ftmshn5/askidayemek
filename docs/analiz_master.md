# Askıda Yemek (Food-Bridge) - Gereksinim Analizi (Master)
**Round 1/10, Tamamlanma: 28/31 (%90)**

Bu belge, HAVSAN standartlarına uygun olarak iteratif analiz sürecini yönetmek için oluşturulmuştur. Lütfen cevaplanmamış soruların yanındaki `<!-- YANIT: ... -->` kısımlarına cevaplarınızı yazın.

## 1. Kapsam ve Platform
- [x] Q1. Proje sadece web olacak mi (masaüstü uygulama yok)?
  → **YANIT:** Web kalacak.
- [x] Q2. Mobil web uyumlulugu gerekli mi, yoksa sadece masaüstü mu?
  → **YANIT:** Gerekli değil, masaüstü yeter.
- [x] Q3. Flask + Jinja devam mi, yoksa ileride bir frontend framework planli mi?
  → **YANIT:** Devam edelim böyle, değişmeye gerek yoksa.

## 2. Temel Akış ve Roller
- [x] Q4. Şu an hangi roller kapsamda? (owner, user, admin, guest)
  → **YANIT:** Hepsini ekleyelim rapordaki.
- [x] Q5. Uygulama icinden kayit (user/owner) gerekli mi, yoksa demo yeterli mi?
  → **YANIT:** Kayıt da olsun.
- [x] Q6. Bir owner birden fazla restoran yönetebilmeli mi?
  → **YANIT:** Evet yönetebilmeli.

## 3. Eşleştirme Mantığı
- [x] Q7. Raporda 15 dakikalik talep penceresi var. 15 dk kalsın mı, değişsin mi?
  → **YANIT:** Kalsın.
- [x] Q8. Pencere başlangıç zamanını nasıl tanımlayalım?
  → **YANIT:** Ürün bazlı; ilgili ürüne gelen ilk talep anında başlasın.
- [x] Q9. Zaman ağırlığı pencerede gerçekten azalmalı mı? (Evet/Hayir)
  → **YANIT:** Evet.
- [x] Q10. Talep başına maksimum 3 ürün seçimi zorunlu mu?
  → **YANIT:** Evet. Maksimum 4 ürün seçimi olsun.

## 4. Miktar ve Envanter
- [x] Q11. Talep eşleştiğinde ürün miktarı düşmeli mi?
  → **YANIT:** Evet.
- [x] Q12. Miktar > 1 ise aynı ürüne birden fazla kullanıcı eşleşebilsin mi?
  → **YANIT:** Hayır. Aynı kullanıcı aynı ürün için birden fazla talep oluşturamasın.
- [x] Q13. Kısmi karşılama gerekli mi? (örneğin 5 porsiyondan 2 talep)
  → **YANIT:** Seçenek A. Bir kullanıcı en fazla 1 porsiyon alır; eşleşme olunca miktar 1 azalır.

## 5. Zamanlayıcı ve Otomasyon
- [x] Q14. SKT otomatik askılama ve batch matching arkaplanda (scheduler) çalışsın mı?
  → **YANIT:** Çalışsın.
- [x] Q15. Evetse APScheduler mi, yoksa basit cron mu tercih edelim?
  → **YANIT:** Basit olan (sunum için hafif çözüm).

## 6. Raporlama
- [x] Q16. Hangi metrikler gerekli? (gıda kurtarma, co2, mutlu kullanıcı, günlük istatistik)
  → **YANIT:** Hepsi olsun rapordakilerin.
- [x] Q17. “En çok bağış yapılan gün” veriden dinamik hesaplansın mı?
  → **YANIT:** Evet.
- [x] Q18. CSV export sadece user/owner için mi, admin da olsun mu?
  → **YANIT:** Admin de dahil olsun.

## 7. Harita ve Lokasyon
- [x] Q19. Restoranlar kullanıcının konumuna göre filtrelensin mi?
  → **YANIT:** Evet. 5 km yarıçap yeterli.
- [x] Q20. Sadece askıda ürün olan restoranlar mı gösterilsin?
  → **YANIT:** Bunun için bir filtreleme olsun. Yani bir filtre aktifken kayıtlı tüm restoranlar, filtre değişince de sadece askıda yemek olan restoranlar.

## 8. Güvenlik ve Erişim
- [x] Q21. Formlar için CSRF koruması gerekli mi?
  → **YANIT:** Evet.
- [x] Q22. Rate limit veya kötüye kullanım önlemi gerekli mi?
  → **YANIT:** Evet. Aynı kullanıcı günde en fazla 3 talep oluşturabilsin.

## 9. Test ve Teslim
- [x] Q23. Otomatik test ister misiniz? (unit/integration)
  → **YANIT:** Unit test yeterli (sunum için hafif tutalım).
- [x] Q24. Çalıştırma adımları için README gerekli mi?
  → **YANIT:** Evet.

## 10. UI ve İçerik
- [x] Q25. Mevcut UI kalsın mı, yoksa teknik rapordaki görünüme yaklaştıralım mı?
  → **YANIT:** Tüm alanlarda (login, harita, owner panel, raporlar) iyileştirme olsun.
- [x] Q26. Dil gereksinimi var mı? (TR/EN, lokalizasyon)
  → **YANIT:** TR/EN olsun sadece yeterli.

## 11. Veri ve Seed
- [x] Q27. Seed veriler kalsın mı, yoksa sadece geliştirme için opsiyonel mi?
  → **YANIT:** Kalsın.
- [x] Q28. Veri saklama sqlite ile mi kalsın, yoksa Postgres planlanıyor mu?
  → **YANIT:** Sqlite daha uyumluysa o kalsın.

---

## 🟢 YENİ SORULAR (Round 1)

## 12. Tasarım ve Kullanıcı Deneyimi (UI/UX)
- [ ] Q29. UI tarafında ciddi bir iyileştirme istendi. Tasarım dili olarak HAVSAN standartlarına uygun, modern ve koyu (Dark Mode) ağırlıklı, renkli vurgular barındıran (glassmorphism vb.) premium bir tasarım uygulayalım mı? Yoksa daha kurumsal ve sade (Light Mode vb.) bir tasarım mı istersiniz? <!-- YANIT: ... -->

## 13. Bildirim ve İletişim Akışı
- [ ] Q30. Arka planda çalışan scheduler bir eşleşme yakaladığında, kullanıcıya veya restoran sahibine nasıl bilgi verilecek? Sadece site içi bildirimler mi olsun, yoksa e-posta gönderimi eklensin mi? (Sunum için site içi bildirim daha pratik olabilir). <!-- YANIT: ... -->

## 14. Guest (Ziyaretçi) Akışı
- [ ] Q31. Ziyaretçilerin (guest) haritayı görebileceğini belirttiniz. Haritadaki bir restoranın "Askıdaki Yemekler" detayına tıkladıklarında, "Talep Et" butonuna basarlarsa onları doğrudan "Giriş Yap / Kayıt Ol" sayfasına yönlendirelim mi? <!-- YANIT: ... -->
