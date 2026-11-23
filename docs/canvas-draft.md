# Proje Fikri Kanvası — NABIZ

**Tarih:** 2026-11-23 · **Alan:** Binalar · **Durum:** 24 Kasım ara teslim taslağı · **Simülasyon:** `results/summary.md`

> **NABIZ — Bodrumdaki hidrofor binanın su nabzını zaten tutuyor.**
> Bu sinyali yapay zekâyla okuyup apartman deposundaki suyu taze, tesisatı sızdırmaz tutuyoruz.

**Karar notu:** 2026-11-23'te ana fikir **birleşik versiyon** (Taze Depo + V1 kaçak) olarak seçildi. Gerekçe:
- Taze Depo'nun problem kanıtı daha güçlü ve güncel (kesintiler).
- V1 ise doğrudan su miktarı etkisini ve en güçlü YZ argümanını getiriyor.
- İkisi de aynı veriden ve aynı modelden (binanın tüketim parmak izi) besleniyor. Böylece hikâye tek kullanıcıda (apartman yöneticisi), tek noktada (bodrumdaki depo + hidrofor) kalıyor.

**Kanıt durumu:** Mülakat yapılmadı. Problem kanıtı yalnız yayımlanmış saha çalışmalarına ve resmî kaynaklara dayanıyor. Kullanıcı ihtiyacına dair iddialar **(varsayım)** diye işaretli. Mülakatlar final öncesine bırakıldı (`docs/interview-guide.md`).

---

## 1. Problem
Kuraklık kesintileri (İzmir'de 13 ilçede Ağustos 2025–Şubat 2026 arası gece kesintisi [1], Ankara'da kontrollü su [2]) apartmanları bodrum deposu + hidrofor düzenine bağımlı yaptı. Bu düzen iki kör nokta yaratıyor:
- **Depo ikilemi.** Dolu tutulan depoda su bayatlıyor. Diyarbakır'da 200 konutta koliform depo girişinde %35, depo çıkışında %52 [3]. Adana'da 53 apartmanın yalnız 4'ünün deposunda bakiye klor ölçülebildi [4]. Tayvan'da 178 binada depolar kesinti korkusuyla gereğinden büyük yapılıyor ve klor hızla düşüyor [5]. Az tutulan depo ise kesintide binayı susuz bırakıyor.
- **Gece sızıntısı.** Aynı tesisatta sızan rezervuar ve boru kaçakları fark edilmeden ortak faturaya yansıyor. 5 L/saatlik bir kaçak ayda 3,6 m³, İSKİ Kasım 2026 tarifesiyle ≈241 TL/ay eder [6]. Türkiye'de bina içi kaçak sıklığına dair veri bulamadık **(varsayım)**.

## 2. Hedef kullanıcı ve ihtiyaç
- **İlk kullanıcı:** Depo + hidrofor bulunan 10–50 daireli apartmanların yöneticisi ve bu binaları yöneten site yönetim firmaları.
- **Zorlandığı anlar (varsayım):**
  - Kesinti duyurulduğunda ya da takvim değiştiğinde depoyu ne kadar dolu tutacağına karar vermek.
  - Depoyu ne zaman temizleteceğini bilmek.
  - Ortak su faturası arttığında nedenini bulmak.
- Üçünü de bugün veri olmadan veriyor.

## 3. Mevcut yaklaşım ve eksikliği
- **Depo seviyesi:** Şamandıra depoyu her zaman tam doldurur, ortada bir seviye kararı yok. Elektronik seviye yönetimi yapan Keraflo Tanktronic seviyeyi **elle girilen takvime** göre ayarlıyor. Kesinti riski ve su yaşı hesabı yok [7].
- **Temizlik:** Adana'da depoyu temizleyenlerin %55,1'i kapıcı. Depoların yalnız %22,5'i önerilen sıklıkta temizleniyor [8]. Konutlar için bağlayıcı bir temizlik periyodu bulamadık (Lejyoner Yönetmeliği konutu kapsamıyor) [9].
- **Kaçak:** Grundfos SCALA2 ve DAB Esybox gibi ev tipi pompalar kaçakta yalnız evet/hayır alarmı veriyor ve pompayı durduruyor. Debi, maliyet ve kaçak türü vermiyorlar, çok daireli bina ünitesine yönelik değiller [10][11].

## 4. Çözüm önerisi
- **Donanım:** Bodrumdaki pompa kontrol ünitesine Modbus TCP ile bağlanan küçük bir uç cihaz. Depoya seviye sensörü, depo girişine normalde açık motorlu vana.
- **Otomatik iş:** NABIZ depo hedef seviyesini kendisi ayarlar. Kesinti riski yükselince depoyu doldurur, risk düşükken depoyu yaklaşık 1 günlük tüketime indirir. Bu, İngiltere HSE'nin önerisiyle uyumlu [12].
- **Yöneticinin gördüğü:** Telefonda haftalık **"bina su karnesi"**: depodaki suyun yaşı, kesinti yedeği (saat), gece kaçağı (L/saat, TL/ay, boru mu rezervuar mı), temizlik önerisi.
- **Emniyet:** Mevcut şamandıra yerinde kalır. Cihaz arızalanırsa vana açık kalır ve sistem bugünkü gibi çalışır.

## 5. Yapay zekânın rolü
- **Tüketim parmak izi:** Debimetre olmadan; pompanın kalkış/duruş zamanlarından, basınçtan ve depo seviyesinden binanın saatlik tüketimini öğrenir.
- **Karar 1 — depo:**
  - Saatlik tüketimi tahmin eder (son 28 günün aynı saatindeki 90. yüzdelik).
  - Binanın kendi kesinti kaydını tutar: vana açık ama depoya su girmiyorsa şebekede kesinti var demektir. Kesinti desenini öğrenir.
  - Bunlarla beklenen bir sonraki kesintiyi köprüleyecek kadar su tutar, fazlasını tutmaz. Habersiz kesintiler için ayarlanabilir bir taban yedek bırakır.
- **Karar 2 — kaçak:**
  - Gece pompa duruş aralıklarının (T_off) dağılımından kaçak debisini çıkarır (Q ≈ ΔV / T_off).
  - Meşru gece kullanımını (sifon, musluk) ayıklar.
  - **Simülasyon sonucu (260 test koşusu):** ≥20 L/saat kaçakların tamamı, 10 L/saat kaçakların %85–90'ı bulundu. Tespit edilen kaçaklarda debi hatası %10, yanlış alarm %5. "Pompalanan hacim / süre" gibi basit bir yöntemin hatası ise %131, çünkü gece kullanımını da kaçak sayıyor.
  - Kaçak türünü iki fiziksel imzadan ayırır:
    - Boru kaçağının debisi basınca bağlıdır (Q ∝ √p). Bu yüzden boru kaçağı tankı döngünün yüksek basınçlı ilk yarısında daha hızlı boşaltır.
    - Rezervuar kaçağı ise suyu darbelerle çeker.
  - Simülasyonda tür doğruluğu **%97**. Rezervuar çok küçük darbelerle doluyorsa (0,3 L) bu oran %63'e düşüyor, bu yüzden düzenekte doğrulanacak.
- **Neden basit kural yetmez:**
  - İzmir'in kesinti takvimi 6 ayda en az 3 kez değişti: 3 günde 1, sonra 2 günde 1, sonra her gün [13]. Sabit zamanlayıcı ya fazla doldurup suyu bayatlatır ya binayı susuz bırakır.
  - Gece sifonları T_off'u kısaltır, sabit eşik yanlış alarm üretir.
  - Rakipler eşikle zaten evet/hayır veriyor, biz debi, maliyet ve tür veriyoruz.
  - Simülasyonda kurulumda girilen sabit takvim, takvim değişince aynı tazelikte 6 kat daha fazla susuz saate yol açtı (38'e karşı 6 saat).
  - Her binanın profili farklı, kural bina bina elle ayarlanamaz.
- **Dürüst not:** Su yaşı hesabı fiziktir (yaş ≈ hacim / tüketim). YZ'nin işi tahmin ve karar kısmında.

## 6. Veri ve uygulanabilirlik
- **Erişilebilir (kılavuzdan doğrulandı):**
  - Wilo SC2.0/SCe2.0 kontrol ünitesi Modbus TCP'yi standart olarak veriyor: sistem basıncı (0,1 bar), pompa çalışıyor biti, kalkış sayaçları [14].
  - CIF modülü takılı Helix2.0-VE pompadan ek olarak güç (W), hız (1/dk) ve hesaplanmış debi okunabiliyor [15].
- **Gereken ek donanım:** Seviye sensörü ve motorlu vana. Bileşenler olgun, Tanktronic aynı donanımı ticari olarak kullanıyor [7].
- **Araçlar:**
  - Çalışan simülasyon: kaçak (260 test koşusu) ve depo (20 senaryo × 180 gün). Kod repoda: `scripts/run_leak.py`, `scripts/run_tank.py`.
  - Tarayıcıda çalışan prototip sayfası: `site/index.html`.
  - 12 V hidrofor test düzeneği tasarlandı. Malzeme listesi hazır, pompa ≈1.219 TL [16].
- **Doğrulanmadı (varsayım):**
  - SCe sıfır debi testinin eşiği (fabrika ayarı). Simülasyonda eşiğin altındaki kaçaklar ölçüldü (10 L/sa ve üstü %100), üstündekiler "gece durmadı" diye büyük kaçak olarak işaretlendi; tür için SCe'ye ayrı model gerekti (%99).
  - Basınç tankının standart donanım olup olmadığı.
  - Wilo-Smart Gateway'in buluta gönderdiği veriler.
  - Türk apartman depolarında suyun nasıl karıştığı.
  - Kaçak türü ayrımının gerçek rezervuarlarda çalışması (simülasyonda %97, küçük darbede %63).
  - Gerçek bina verisine henüz erişimimiz yok.

## 7. Beklenen su etkisi
- **Kalite (simülasyon):** Musluğa gelen suyun ortalama depo yaşı şamandıraya göre 39 saatten 25 saate iniyor. Bunun karşılığında 166 günde yaklaşık 6 susuz saat var, şamandırada 1'in altında. Kesinti senaryosu ve bina varsayım, karışım modeli tam karışım [17].
- **Miktar:** Bulunan her 5 L/saatlik kaçak ayda 3,6 m³ su ve ≈241 TL demek [6].
- **Göstergeler:**
  - Depo su yaşı (saat) ve yaş sınırını aşan süre (%).
  - Kesintide susuz kalınan saat (hedef: 0).
  - Tespit edilen en küçük kaçak (L/saat).
  - Tespit gecikmesi (gece sayısı).
  - Yanlış alarm (ay başına).
- **Gelişim:**
  - Wilo break tank + SiBoost paketine yazılım katmanı [18].
  - Site yönetim firmaları için çok binalı pano.
  - Aynı "pompa = sensör" yaklaşımıyla kuyu pompasından akifer seviyesi izleme.

## 8. İlk test
- **Doğru olması gereken varsayımlar:**
  1. Küçük kaçak, 0,1 bar basınç çözünürlüğü ve gece kullanımı altında bile T_off'tan ölçülebilir.
  2. Tüketim, pompa ve seviye verisinden yeterli doğrulukta tahmin edilebilir.
  3. Yöneticiler bu kararları bugün veri olmadan veriyor ve çözüme değer biçiyor.
- **Hackathon günü:**
  - 12 V düzenekte iğneli vanayla 2–50 L/saat kaçak açılır, gerçek debi teraziyle ölçülür ve model tahmini canlı gösterilir. Metrikler: ortalama mutlak hata (MAE) ve tespit edilen en küçük kaçak.
  - Simülasyon yapıldı (`results/summary.md`). Finalde gerçek bir binanın kesinti kaydıyla tekrarlanır.
- **Ek sağlamlık testleri (yapıldı, `scripts/run_checks.py`):**
  - Tank havasını kaybedince debi hatası %34'e kadar çıkıyor. Pompa çalışma süresinden yeniden kalibrasyonla %3'e iniyor.
  - Kalabalık gecelerde (saatte 3–5 kullanım) tespit %73'e düşüyor, yanlış alarm %10'a çıkıyor.
  - Pompanın çek valf sızıntısı "boru kaçağı" gibi görünüyor ve ayrılamıyor; raporda tesisatçıya ilk kontrol noktası olarak yazılacak.
- **Final öncesi:** 3 mülakat (yönetici, sakin, tesisatçı). Rehber hazır.

---

## Kaynaklar
1. İZSU, 06.02.2026 — https://izsu.gov.tr/haberler/tahtali-yukselise-gecti-gece-kesintileri-sona-erdi
2. Habertürk / AA, 04.12.2025 — https://www.haberturk.com/baskentte-kontrollu-su-donemi-3842844
3. Çalık O., tıpta uzmanlık tezi, Diyarbakır (özet; tam metin açılamadı) — https://acikbilim.yok.gov.tr/handle/20.500.12812/292765
4. Aydın, Atakav, Ç.Ü. Müh.-Mim. Fak. Dergisi 33(1), 2018 — https://dergipark.org.tr/en/pub/cukurovaummfd/article/420689
5. Wang & Chen, Water Sci. & Tech.: Water Supply 6(2), 2006 — doi:10.2166/ws.2006.046
6. İSKİ konut 1. kademe, Kasım 2026: su 44,63 + atıksu 22,28 = 66,91 TL/m³ (KDV hariç; tarife her ay güncelleniyor) — https://www.endeks24.com/istanbul-da-suya-her-ay-zam-2027-de-de-surecek-tavan-yuzde-2 (19.11.2026). Resmî Ocak 2026 tablosu: https://iskiapi.iski.gov.tr/uploads/2026_aylik_su_ve_atiksu_birim_fiyatlari_KLAS_Oe_R_d363120d24.pdf · Hesap: 5 L/h × 720 h = 3,6 m³ × 66,91 TL ≈ 241 TL
7. Keraflo Tanktronic broşürü — https://cdn.shopify.com/s/files/1/0620/6219/8980/files/Tanktronic-6p-Flyer-2022-ID-42803.pdf
8. Aydın, Atakav, Ceylan, Ç.Ü. Müh.-Mim. Fak. Dergisi 31(ÖS 2), 2016 — https://dergipark.org.tr/en/download/article-file/307763
9. Lejyoner Hastalığı Kontrol Usul ve Esasları Hakkında Yönetmelik, RG 29354 (Md. 5 kapsam, Md. 8) — https://hsgm.saglik.gov.tr/depo/birimler/mikrobiyoloji-referans-laboratuvarlari-ve-biyolojik-urunler-db/Dokumanlar/LEJYONER_HASTALIGI_KONTROL_USUL_VE_ESASLARI_YONETMELIK.pdf
10. Grundfos SCALA2 kılavuzu, 10.3.4 — https://api.grundfos.com/literature/Grundfosliterature-5769057.pdf
11. DAB Esybox Pop kılavuzu, 7.2.3.10 — https://www.dabpumps.com/sites/default/files/document/esybox_pop_dab_instruction_manual_web_version_multi_60231842.pdf
12. HSE, Legionnaires' disease — https://www.hse.gov.uk/Legionnaires/things-to-consider.htm
13. Yeni Şafak ve Milliyet haberleri (arama özetleri, kısmen doğrulandı) — `docs/taze-depo-validation.md` §a
14. Wilo-Control SC2.0-Booster kılavuzu, s.17, s.55–59 — https://cms.media.wilo.com/dcidocpfinder/wilo629451/7984526/wilo629451.pdf
15. Wilo Modbus veri noktası listesi — https://cms.media.wilo.com/cdndoc/wilo194406/11516106/wilo194406.html
16. `docs/v1-test-rig.md` (SEAFLO SFDP1-012-035-21, idefix, 2026-11-17)
17. EPANET 2.2 depo karışım modelleri — https://usepa.github.io/EPANET2.2/3_network_model.html
18. Wilo break tank — https://wilo.com/gb/en/Products/en/accessory/break-tank-for-sanitary-water-application-rectangular-version
