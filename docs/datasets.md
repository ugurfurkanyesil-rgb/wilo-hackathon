# Veri Setleri ve Simülasyon Araçları

Doğrulama tarihi: 2026-11-17. Her kaynağın sayfası açılarak kontrol edildi. Türkiye kaynaklarının dosyaları indirilip sütunlarına bakıldı.
"Bilmiyorum" yazılan alanlar kaynak sayfasında yer almıyor.

## Özet

Sıralama: önce login gerektirmeyenler, sonra hesap gerektirenler.

| # | Kaynak | Halka | Tür | Lisans | Boyut | Login |
|---|---|---|---|---|---|---|
| 1 | EPANET 2.2 | Dağıtım/Basınçlandırma | Simülatör | Public domain (EPA) | 3.5 MB | Hayır |
| 2 | WNTR | Dağıtım/Basınçlandırma | Simülatör (Python) | Revised BSD | bilmiyorum | Hayır |
| 3 | BattLeDIM | Dağıtım (kaçak) | Veri, SCADA | CC BY 4.0 | 550.5 MB | Hayır |
| 4 | LeakDB | Dağıtım (kaçak) | Veri, simülasyon | CC BY 4.0 | 13.9 GB | Hayır |
| 5 | SKAB | Pompa (çapraz) | Veri, test düzeneği | GPL-3.0 | repo 34 MB | Hayır |
| 6 | UCI Hydraulic Systems | Pompa (çapraz) | Veri, test düzeneği | CC BY 4.0 | 73.1 MB | Hayır |
| 7 | UCI Water Treatment Plant | Atıksu Arıtımı | Veri, gerçek tesis | CC BY 4.0 | 38.5 KB | Hayır |
| 8 | SWMM + pyswmm | Atıksu Transferi, Taşkın | Simülatör | Public domain / BSD2 | bilmiyorum | Hayır |
| 9 | İBB Baraj Doluluk | Su Temini | Veri, günlük | İBB Açık Veri Lisansı | 851 KB + 121 KB | Hayır |
| 10 | İBB Baraj Yağış + Günlük Tüketim | Su Temini, Taşkın | Veri, günlük | İBB Açık Veri Lisansı | 313 KB | Hayır |
| 11 | İBB İstanbul'a Verilen Temiz Su | Dağıtım | Veri, aylık | İBB Açık Veri Lisansı | 14 KB | Hayır |
| 12 | İBB İlçe Bazında Su Tüketimi | Dağıtım | Veri, yıllık | İBB Açık Veri Lisansı | 13 KB (2015–22) | Hayır |
| 13 | İBB Yıllık Su Tüketimi | Dağıtım | Veri, yıllık | İBB Açık Veri Lisansı | 9 KB | Hayır |
| 14 | İBB Şebekeden Deşarj Edilen Atıksu | Atıksu Arıtımı | Veri, yıllık | İBB Açık Veri Lisansı | 11 KB | Hayır |
| 15 | İBB Yeşil Alanlar İçin Harcanan Su | Sulama/Yeniden Kullanım | Veri, yıllık | İBB Açık Veri Lisansı | 9 KB | Hayır |
| 16 | İzmir (İZSU) Baraj Doluluk | Su Temini | Veri, anlık + API | İzmir BB Açık Veri Lisansı | 1 KB | Hayır |
| 17 | İzmir (İZSU) Günlük Su Üretimi | Su Temini | Veri, anlık + API | İzmir BB Açık Veri Lisansı | 0.4 KB | Hayır |
| 18 | Kaggle pump_sensor_data | Pompa (çapraz) | Veri, gerçek pompa | Unknown | 124 MB | **Kaggle hesabı** |
| 19 | Kaggle Water Potability | İçme Suyu Arıtımı | Veri | CC0 | 525 KB | **Kaggle hesabı** |

Not: Türkiye kaynaklarında (#9–17) boyut, indirilen dosyanın bayt değeridir.

---

## Simülasyon araçları

### 1. EPANET 2.2
- **Link:** https://www.epa.gov/water-research/epanet · https://github.com/USEPA/EPANET2.2
- **Lisans:** EPA sayfasında "public domain software". GitHub reposunda MIT lisansı (LICENSE.txt) yazıyor.
- **Boyut:** Kurulum dosyası (EXE) 3.5 MB, ZIP 2.84 MB ([EPA](https://www.epa.gov/water-research/epanet)).
- **İçerik:** İçme suyu şebekesinde hidrolik ve su kalitesinin zamana yayılmış simülasyonu. Boru, düğüm, **pompa**, vana, tank ve rezervuar modellenebiliyor. Pompa ve tank işletmesini optimize ederek enerji tasarrufu amacıyla da kullanılıyor ([GitHub](https://github.com/USEPA/EPANET2.2)).
- **Halka:** Dağıtım/Basınçlandırma.
- **İndirme:** https://github.com/USEPA/EPANET2.2/releases/download/2.2.0/epanet2.2.zip (yalnız Windows GUI).

### 2. WNTR (Water Network Tool for Resilience)
- **Link:** https://github.com/USEPA/WNTR
- **Lisans:** Revised BSD.
- **Boyut:** Bilmiyorum (pip paketi).
- **İçerik:** EPANET uyumlu bir Python paketi.
  - Simülasyon türleri: talebe bağlı (demand-driven) ve basınca bağlı (pressure-dependent) hidrolik, su kalitesi.
  - Senaryolar: boru kaçağı gibi bozucu olaylar ve onarım stratejileri.
  - Pompa arızası senaryosu sayfada açıkça geçmiyor.
- **Halka:** Dağıtım/Basınçlandırma. Sentetik etiketli veri üretmek için kullanılır (EPANET `.inp` dosyası + kaçak senaryosu → basınç ve debi zaman serisi).
- **İndirme:** `pip install wntr`

### 8. SWMM 5.2.4 + pyswmm
- **Link:** https://www.epa.gov/water-research/storm-water-management-model-swmm · https://github.com/USEPA/Stormwater-Management-Model · https://github.com/pyswmm/pyswmm
- **Lisans:** SWMM public domain ([GitHub](https://github.com/USEPA/Stormwater-Management-Model)). pyswmm BSD2 ([GitHub](https://github.com/pyswmm/pyswmm)).
- **Boyut:** Bilmiyorum.
- **İçerik:** Yağmur suyu, atıksu ve birleşik kanalizasyon sistemleri için hidroloji, hidrolik ve su kalitesi simülasyonu ([EPA](https://www.epa.gov/water-research/storm-water-management-model-swmm)).
  - **Pompalar** modellenebiliyor ve kontrol kurallarıyla işletilebiliyor.
  - Taşma (surcharge) ve yüzeyde göllenme simüle ediliyor.
  - Taşkın kontrolü ve birleşik kanal taşkını (CSO) azaltma senaryolarında kullanılıyor.
  - pyswmm ile simülasyon sırasında Python'dan kontrol mantığı yazılabiliyor.
- **Halka:** Atıksu Transferi (terfi istasyonu pompaları), Taşkın Önleme.
- **İndirme:** `pip install pyswmm` (SWMM motoru pakete dahil; motor sürümü 5.1.14–5.2.4 arası seçilebiliyor).

---

## Etiketli benchmark veri setleri

### 3. BattLeDIM (Battle of the Leakage Detection and Isolation Methods)
- **Link:** https://zenodo.org/records/4017659 (DOI 10.5281/zenodo.4017659)
- **Lisans:** CC BY 4.0.
- **Boyut:** Toplam 550.5 MB.
  - Yıl başına SCADA CSV dosyaları: Pressures 22.6 MB, Flows 4 MB, Levels 2.7 MB, Demands 56.5 MB.
  - `L-TOWN_Real.inp` 177.2 MB.
- **İçerik:** L-TOWN şebekesinin 2018 ve 2019 SCADA verileri: basınç, debi, tank seviyesi ve talep.
  - **Etiketler:** `2018_Leakages.csv` ve `2019_Leakages.csv` dosyalarında kaçak debileri, ayrıca 2018 onarılmış kaçak raporu var.
  - EPANET modeli (`L-TOWN.inp`) dahil.
  - Sensör sayısı ve örnekleme aralığı Zenodo sayfasında yok. README.txt'de olabilir, bilmiyorum.
- **Halka:** Dağıtım. Kaçak tespiti ve yerinin bulunması.
- **İndirme:** Zenodo'dan doğrudan, login gerekmez. Sadece CSV'ler indirilirse yaklaşık 190 MB.

### 4. LeakDB
- **Link:** https://zenodo.org/records/13985057 (DOI 10.5281/zenodo.13985057) · kod: https://github.com/KIOS-Research/LeakDB
- **Lisans:** Veri CC BY 4.0 ([Zenodo](https://zenodo.org/records/13985057)), kod EUPL-1.2 ([GitHub](https://github.com/KIOS-Research/LeakDB)).
- **Boyut:** `LeakDB.zip` 13.9 GB.
- **İçerik:** Farklı şebekelerde (örneğin Hanoi) yapay ama gerçekçi kaçak senaryoları. Algoritmaları puanlamak için MATLAB skorlama aracı da var. Senaryo sayısı, sensör türleri ve zaman çözünürlüğü sayfalarda yok, bilmiyorum.
- **Halka:** Dağıtım (kaçak).
- **İndirme:** Zenodo'dan doğrudan. Boyutu nedeniyle 3 günlük demo için **önerilmez**. Bunun yerine BattLeDIM veya WNTR ile kendi senaryolarımızı üretmek daha pratik.

### 5. SKAB (Skoltech Anomaly Benchmark)
- **Link:** https://github.com/waico/SKAB (Kaggle aynası: kaggle.com/yuriykatser/skoltech-anomaly-benchmark-skab)
- **Lisans:** GPL-3.0.
- **Boyut:** GitHub reposunun tamamı 34,084 KB ([GitHub API](https://api.github.com/repos/waico/SKAB)).
- **İçerik:** Elektrik motoru ve **su pompası** ile çalışan bir su sirkülasyon düzeneği.
  - **Sensörler:** 2 ivmeölçer RMS (titreşim), motor akımı, pompa çıkışı basıncı, motor gövde sıcaklığı, akışkan sıcaklığı, gerilim, debi (L/min).
  - **Etiketler:** `anomaly` (0/1) ve `changepoint` (0/1).
  - **Dosya sayısı:** v0.9 sürümünde her biri tek anomali içeren 34 veya 35 CSV (sayfada iki farklı sayı geçiyor).
  - Örnekleme hızı sayfada yok.
- **Halka:** Pompa durumu izleme. Bütün halkaları kesiyor ve **Wilo pompalarına en doğrudan bağlanan kaynak**.
- **İndirme:** `git clone https://github.com/waico/SKAB` (veri `data/` klasöründe). Not: GPL-3.0 lisansı, veriyi koda gömüp dağıtırsak kodu da etkileyebilir. Veriyi ayrı tutmak gerekir.

### 6. UCI Condition Monitoring of Hydraulic Systems
- **Link:** https://archive.ics.uci.edu/dataset/447/condition+monitoring+of+hydraulic+systems (DOI 10.24432/C5CW21)
- **Lisans:** CC BY 4.0.
- **Boyut:** ZIP 73.1 MB.
- **İçerik:** Hidrolik test düzeneğinde 60 saniyelik 2,205 yük döngüsü.
  - **Sensörler:** 6 basınç (100 Hz), motor gücü (100 Hz), 2 debi (10 Hz), 4 sıcaklık (1 Hz), titreşim (1 Hz) ve 3 sanal sensör.
  - **Etiketler** (döngü başına): soğutucu durumu, vana durumu, **dahili pompa kaçağı** (0, 1, 2), akümülatör basıncı, kararlılık bayrağı.
- **Halka:** Pompa durumu izleme. Not: düzenek hidrolik yağla çalışıyor, su pompası değil.
- **İndirme:** `pip install ucimlrepo` → `fetch_ucirepo(id=447)` veya sayfadan ZIP.

### 7. UCI Water Treatment Plant
- **Link:** https://archive.ics.uci.edu/dataset/106/water+treatment+plant (DOI 10.24432/C5FS4C)
- **Lisans:** CC BY 4.0.
- **Boyut:** ZIP 38.5 KB.
- **İçerik:** Kentsel bir atıksu arıtma tesisinden 527 günlük ölçüm, 38 sürekli değişken.
  - Değişkenler giriş, ön çöktürme, son çöktürme ve çıkış aşamalarında ölçülüyor: debi, pH, BOİ, KOİ, AKM, iletkenlik vb.
  - Giderim verimleri de var.
  - Hazır etiket yok, kümeleme ile tesis durumu sınıflandırması için hazırlanmış.
  - Veri 1993'te yayımlanmış.
- **Halka:** Atıksu Arıtımı.
- **İndirme:** `fetch_ucirepo(id=106)`.

---

## Türkiye kaynakları

Lisans notları:
- **İBB Açık Veri Lisansı** ([metin](https://data.ibb.gov.tr/license)): Ticari ve ticari olmayan kullanım serbest, **atıf zorunlu**. Veriyi resmî onay ima edecek şekilde kullanmak yasak.
- **İzmir BB Açık Veri Lisansı** ([metin](https://acikveri.bizizmir.com/tr/license)): Ticari kullanım dahil serbest, **atıf zorunlu**.

### 9. İBB / İSKİ Baraj Doluluk Oranları
- **Link:** https://data.ibb.gov.tr/dataset/istanbul-barajlari-gunluk-doluluk-oranlari · https://data.ibb.gov.tr/dataset/istanbul-dam-occupany-rates-data
- **Boyut:** XLSX 871,515 B · CSV 124,111 B.
- **İçerik:**
  - **XLSX:** 10 barajın (Ömerli, Darlık, Elmalı, Terkos, Alibey, Büyükçekmece, Sazlıdere, Kazandere, Pabuçdere, Istrancalar) günlük doluluğu, 0–1 oranı olarak. 2000-10-23 ile 2024-02-19 arası, 8,520 satır.
  - **CSV:** Genel doluluk (%) ve rezerv su. 2005-01-01 ile 2021-04-07 arası, 5,941 satır. Rezerv su sütununun birimi dosyada yok.
- **Halka:** Su Temini.
- **İndirme:** Doğrudan link, login gerekmez. CKAN API: `https://data.ibb.gov.tr/api/3/action/package_search?q=baraj`

### 10. İBB / İSKİ Barajlarda Yağış ve Günlük Tüketim
- **Link:** https://data.ibb.gov.tr/dataset/istanbul-barajlarina-dusen-gunluk-toplam-yagis-miktari
- **Boyut:** XLSX 320,750 B.
- **İçerik:**
  - Kapsam: 2011-01-01 ile 2024-02-18 arası, 4,797 satır.
  - Sütunlar: 10 barajın günlük yağışı ve **İstanbul günlük tüketimi (m³/gün)**.
  - Yağışın birimi dosyada yazmıyor.
- **Halka:** Su Temini (talep tahmini), Taşkın (yağış).
- **İndirme:** Doğrudan link.

### 11. İBB / İSKİ İstanbul'a Verilen Temiz Su Miktarları
- **Link:** https://data.ibb.gov.tr/dataset/istanbul-a-verilen-temiz-su-miktarlari
- **Boyut:** XLSX 13,903 B.
- **İçerik:** Aylık verilen su miktarı, 2009–2024 (2024 yalnız Ocak).
  - Metadata'daki birim "(m³·1000)/Ay".
  - **Uyarı:** 2009–2019 değerleri ~10⁴–10⁵, 2020 sonrası değerleri ~10⁷ büyüklüğünde. Birim tutarsız görünüyor. Aralık 2019 değeri (51,278) diğer aylardan belirgin şekilde düşük.
- **Halka:** Dağıtım.

### 12. İBB / İSKİ İlçe Bazında Su Tüketimi
- **Link:** https://data.ibb.gov.tr/dataset/ilce-bazinda-su-tuketim-miktari
- **Boyut:** 2015–2022 dosyası 13,006 B. Ayrıca 2000–2015 ve 2023 dosyaları var, onların boyutunu bilmiyorum.
- **İçerik:** 39 ilçenin yıllık tüketimi (m³).
- **Halka:** Dağıtım.

### 13. İBB / İSKİ Yıllık Su Tüketimi
- **Link:** https://data.ibb.gov.tr/dataset/istanbul-yillik-su-tuketimi-verileri
- **Boyut:** XLSX 9,270 B.
- **İçerik:** 1991–2023 arası toplam yıllık tüketim (m³), 33 satır.
- **Halka:** Dağıtım.

### 14. İBB / TÜİK Alıcı Ortamlara Göre Şebekeden Deşarj Edilen Atıksu
- **Link:** https://data.ibb.gov.tr/dataset/alici-ortamlara-gore-sebekeden-desarj-edilen-atiksu-miktari-bin-m3-yil
- **Boyut:** XLSX 11,558 B.
- **İçerik:** Atıksuyun deşarj edildiği ortama (akarsu, deniz, göl, arazi vb.) ve arıtılıp arıtılmadığına göre yıllık miktar (bin m³/yıl). 2001–2022 arası, düzensiz yıllar, 14 satır.
- **Halka:** Atıksu Arıtımı. Bağlam ve sunum için uygun, model eğitmek için uygun değil.

### 15. İBB Yeşil Alanlar İçin Harcanan Su
- **Link:** https://data.ibb.gov.tr/dataset/yillara-gore-park-ve-bahce-gibi-yesil-alanlar-icin-harcanan-su-miktari
- **Boyut:** XLSX 9,615 B.
- **İçerik:** 2017–2025 arası yıllık sulama suyu (m³), 9 satır.
- **Halka:** Sulama/Yeniden Kullanım. Yalnız bağlam ve sunum için uygun.

### 16. İzmir / İZSU Barajların Doluluk Oranları
- **Link:** https://acikveri.bizizmir.com/dataset/barajlarin-doluluk-oranlari
- **Boyut:** CSV 942 B.
- **İçerik:** **Anlık durum, tarihsel seri değil.** İndirilen dosyada 5 baraj vardı, tarih 2026-10-14.
  - Sütunlar: doluluk oranı, su yüksekliği, kullanılabilir/maksimum/minimum kapasite, enlem/boylam.
  - API var (`https://acikveriwapi.izmir.bel.tr/AcikVeriIzsuApi/DamWaterStatus`). API'nin geçmiş veri verip vermediğini bilmiyorum.
- **Halka:** Su Temini.
- **İndirme:** https://openfiles.izmir.bel.tr/309436/docs/izsu-baraj-doluluk-oranlari.csv

### 17. İzmir / İZSU Günlük Su Üretimi
- **Link:** https://acikveri.bizizmir.com/dataset/gunluk-su-uretimi
- **Boyut:** CSV 405 B.
- **İçerik:** **Anlık durum.** 10 baraj ve kuyu için tür, ad ve üretim miktarı. Dosyada tarih sütunu yok, birim yazmıyor.
- **Halka:** Su Temini.
- **İndirme:** https://openfiles.izmir.bel.tr/309436/docs/izsu-gunluk-su-uretimi.csv

---

## Hesap gerektiren kaynaklar

### 18. Kaggle pump_sensor_data
- **Link:** https://www.kaggle.com/datasets/nphantawee/pump-sensor-data
- **Lisans:** Kaggle'da "Unknown". Yarışmada kullanmadan önce bu riski not etmek gerekir.
- **Boyut:** 124,058,460 B (~124 MB).
- **İçerik:** Uzak bir bölgeye hizmet eden bir su pompasının 52 sensörünün ham değerleri. Pompa son bir yılda 7 kez arızalanmış ve amaç bir sonraki arızayı tahmin etmek. Son güncelleme 2019-03-04. Sütun adları ve etiket değerleri API yanıtında yok, doğrulanmadı.
- **Halka:** Pompa kestirimci bakımı.
- **İndirme:** **Kaggle hesabı gerekli.** Web arayüzünden ya da `kaggle datasets download nphantawee/pump-sensor-data` ile indirilir (API token ister).

### 19. Kaggle Water Potability
- **Link:** https://www.kaggle.com/datasets/adityakadiwal/water-potability
- **Lisans:** CC0 Public Domain.
- **Boyut:** 525,187 B.
- **İçerik:** 3,276 su kütlesi için 9 kalite parametresi (pH, sertlik, TDS, kloramin, sülfat, iletkenlik, organik karbon, THM, bulanıklık) ve `Potability` (0/1) etiketi.
  - **Uyarı:** Verinin nereden ve nasıl toplandığı açıklamada yok.
  - Açıklamaya göre bazı sütunlara sonradan eksik değer eklenmiş.
  - Güvenilirliği düşük, yalnız prototip için kullanılabilir.
- **Halka:** İçme Suyu Arıtımı.
- **İndirme:** **Kaggle hesabı gerekli.**

---

## Doğrulanamadı

| Kaynak | Durum |
|---|---|
| **DSİ akım gözlem (AGİ) verileri** | İndirilebilir açık veri sayfası bulunamadı. Aramada yalnız [DSİ metaveri belgesi](https://cdniys.tarimorman.gov.tr/api/File/GetGaleriFile/425/DosyaGaleri/8848/dsi_metaveri_11.12.2025.doc) ve USBS'den söz eden bir [makale](https://dergipark.org.tr/en/download/article-file/806118) çıktı. |
| **Ankara ASKİ baraj doluluk** | Makine tarafından okunabilir bir veri seti bulunamadı. Arama sonuçlarının tamamı haber sitesiydi. |
| **SWaT / WADI (iTrust, SUTD)** | [Veri sayfası](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/) ücretsiz paylaşım yapıldığını söylüyor ama **talep formu** gerekiyor (işlem süresi 3 iş gününe kadar). İçerik (sensör, aktüatör, saldırı etiketi) sayfada yok, doğrulanamadı. |
| **Diğer büyükşehirler** (Ankara, Bursa, Antalya, Konya vb. açık veri portalları) | Taranmadı. İhtiyaç olursa aynı CKAN API yöntemiyle bakılabilir. |
