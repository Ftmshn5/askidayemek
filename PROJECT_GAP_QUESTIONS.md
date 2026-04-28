# Askida Yemek - Eksikler ve Sorular

Amac: Eksik gereksinimleri ve karar noktalarini netlestirmek. Lutfen her sorunun altindaki Answer alanini doldurun.

---

## 1. Kapsam ve Platform

Q1. Proje sadece web olacak mi (masaustu uygulama yok)?
Answer: Web kalacak.

Q2. Mobil web uyumlulugu gerekli mi, yoksa sadece masaustu mu?
Answer: Gerekli değil masaüstü yeter.

Q3. Flask + Jinja devam mi, yoksa ileride bir frontend framework planli mi?
Answer: Devam edelim böyle değişmeye gerek yoksa.

---

## 2. Temel Akis ve Roller

Q4. Su an hangi roller kapsamda? (owner, user, admin, guest)
Answer: Hepsini ekleyelim rapordaki.

Q5. Uygulama icinden kayit (user/owner) gerekli mi, yoksa demo yeterli mi?
Answer: Kayıt da olsun.

Q6. Bir owner birden fazla restoran yonetebilmeli mi?
Answer: Evet yönetebilmeli.

---

## 3. Eslestirme Mantigi (Rapordan)

Q7. Raporda 15 dakikalik talep penceresi var. 15 dk kalsin mi, degissin mi?
Answer: Kalsın.

Q8. Pencere baslangic zamanini nasil tanimlayalim? (ilk talep anindan, urun bazli, global batch)
Answer: Urun bazli; ilgili urune gelen ilk talep aninda baslasin.

Q9. Zaman agirligi pencerede gercekten azalmali mi? (Evet/Hayir)
Answer: Evet.

Q10. Talep basina maksimum 3 urun secimi zorunlu mu?
Answer: Evet. Maksimum 4 urun secimi olsun.

---

## 4. Miktar ve Envanter

Q11. Talep eslestiginde urun miktari dusmeli mi?
Answer: Evet.

Q12. Miktar > 1 ise ayni urune birden fazla kullanici eslesebilsin mi?
Answer: Hayir. Ayni kullanici ayni urun icin birden fazla talep olusturamasin.

Q13. Kismi karsilama gerekli mi? (ornegin 5 porsiyondan 2 talep)
Answer: Secenek A. Bir kullanici en fazla 1 porsiyon alir; eslesme olunca miktar 1 azalir.

---

## 5. Zamanlayici ve Otomasyon

Q14. SKT otomatik askilama ve batch matching arkaplanda (scheduler) calissin mi?
Answer: Çalışsın.

Q15. Evetse APScheduler mi, yoksa basit cron mu tercih edelim?
Answer: Basit olan (sunum icin hafif cozum).

---

## 6. Raporlama

Q16. Hangi metrikler gerekli? (gida kurtarma, co2, mutlu kullanici, gunluk istatistik)
Answer: Hepsi olsun rapordakilerin.

Q17. “En cok bagis yapilan gun” veriden dinamik hesaplansin mi?
Answer: Evet.

Q18. CSV export sadece user/owner icin mi, admin da olsun mu?
Answer: Admin da dahil olsun.

---

## 7. Harita ve Lokasyon

Q19. Restoranlar kullanicinin konumuna gore filtrelensin mi?
Answer: Evet. 5 km yaricap yeterli.

Q20. Sadece askida urun olan restoranlar mi gosterilsin?
Answer: Bunun için bir filtreleme olsun. Yani bir filtre aktifken kayıtlı tüm restoranlar, filtre değişince de sadece askıda yemek olan restoranlar.

---

## 8. Guvenlik ve Erisim

Q21. Formlar icin CSRF korumasi gerekli mi?
Answer: Evet.

Q22. Rate limit veya kotuye kullanim onlemi gerekli mi?
Answer: Evet. Ayni kullanici gunde en fazla 3 talep olusturabilsin.

---

## 9. Test ve Teslim

Q23. Otomatik test ister misiniz? (unit/integration)
Answer: Unit test yeterli (sunum icin hafif tutalim).

Q24. Calistirma adimlari icin README gerekli mi?
Answer: Evet.

---

## 10. UI ve Icerik

Q25. Mevcut UI kalsin mi, yoksa teknik rapordaki gorunume yaklastiralim mi?
Answer: Tum alanlarda (login, harita, owner panel, raporlar) iyilestirme olsun.

Q26. Dil gereksinimi var mi? (TR/EN, lokalizasyon)
Answer: TR/EN olsun sadece yeterli.

---

## 11. Veri ve Seed

Q27. Seed veriler kalsin mi, yoksa sadece gelistirme icin opsiyonel mi?
Answer: Kalsın

Q28. Veri saklama sqlite ile mi kalsin, yoksa Postgres planlaniyor mu?
Answer: Sqlite daha uyumluysa o kalsın.

---

## Notlar

Serbest notlar: Soruları tamamen anlamadan, hepsini tamamlamadan geliştirmeye başlama. Önce analizi %100 tamamlayalım. Her şeyi tamamladıktan sonra adım adım soruları güncelleyerek geliştirmeye devam edelim.
Ek not: Guest haritayi gorebilsin.

