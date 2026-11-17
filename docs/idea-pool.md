# Fikir Havuzu

**Kurallar:**
- Veri referansları `docs/datasets.md`'deki kaynak numaralarıdır (#n).
- Wilo ürün bilgileri 2026-11-17'de ürün sayfaları açılarak doğrulandı. Sayfası doğrulanmayan yerlerde "genel pompa" yazıyor.
- Metrikler tanım olarak verildi. Hedef sayı yazılmadı, çünkü hedefin ancak bir baseline ölçüldükten sonra konması gerekiyor.

## Kullanılan Wilo ürünleri

| Ürün | Doğrulanan özellik | Kaynak |
|---|---|---|
| Wilo-SiBoost Smart Helix VE | Basınçlandırma ünitesi. 2–4 paralel Helix VE pompası, her pompada entegre frekans konvertörü (25–60 Hz). Basma tarafında 4–20 mA basınç sensörü, emme tarafında basınç sensörü, kuru çalışma algılama. | [wilo.com](https://wilo.com/gb/en/Products/en/application/wilo-siboost-smart-helix-ve?page=2) |
| Wilo-Rexa SUPRA | Dalgıç atıksu pompası. Conta ve sızıntı odasında kaçak algılama, opsiyonel titreşim ve yatak sıcaklığı izleme. Wilo-DDI ile Ethernet bağlantısı, ModBus/TCP ve OPC UA desteği. | [wilo.com](https://wilo.com/gb/en/Products/en/products-expertise/wilo-rexa-supra?t=0) |
| Wilo-Rexa SOLID | Akıllı atıksu pompası. Tıkanma algılama algoritması, kendini temizleme, harici Wilo-EFC frekans konvertörü. DDI üzerinden sargı sıcaklığı, kaçak ve titreşim izleme, veri kaydedici. | [wilo.com](https://wilo.com/ng/en/Catalogue/en/products-expertise/wilo-rexa-solid) |
| Wilo-Actun ZETOS | Ham su alma ve kuyu pompası. Kullanım alanları: şehir şebekesi, içme suyu, tarım ve sulama. Sayfada izleme veya sensör seçeneği geçmiyor. | [wilo.com](https://wilo.com/us/en_us/Products/en/products-expertise/wilo-actun-zetos) |

**Wilo bağı ölçeği:**
- **Doğrudan:** Fikir pompanın kendi sensör verisini kullanıyor ya da pompanın kontrolünü değiştiriyor.
- **Dolaylı:** Fikir pompa işletmesini etkileyen sistem verisini kullanıyor.
- **Yok.**

---

## 1. Su Temini

### A1. Baraj doluluk tahmini (İstanbul)
- **Problem:** Kuraklık dönemlerinde ham su alma ve pompalama planı geç yapılıyor.
- **Veri:** #9 (baraj bazında günlük doluluk, 2000–2024), #10 (günlük yağış ve tüketim, 2011–2024). Login yok.
- **AI yöntemi:** Gecikmeli (lag) yağış ve tüketim özellikleriyle LightGBM veya SARIMAX. 7 ve 30 gün sonrası için tahmin.
- **Wilo bağı:** Dolaylı. Ham su alma pompalarının işletme planına girdi olur, örneğin [Wilo-Actun ZETOS](https://wilo.com/us/en_us/Products/en/products-expertise/wilo-actun-zetos).
- **Metrik:** Test döneminde MAE (yüzde puan). Baseline olarak "bugünkü değer yarın da aynı kalır" (persistence) tahmini kullanılır.
- **Demo puanı: 5.** Veri küçük, temiz ve login gerektirmiyor. Klasik zaman serisi işi.
- **Riskler:**
  - İBB serileri **2024 Şubat'ta bitiyor**. Demo "geçmiş üzerinde backtest" olarak sunulmalı.
  - #9'daki iki dosyanın ölçeği farklı (0–1 oran ve %).

### A2. İstanbul günlük su talebi tahmini
- **Problem:** Talep zirveleri (yaz, bayram) önceden bilinmezse pompalar plansız çalışıyor.
- **Veri:** #10 (İstanbul günlük tüketimi, m³/gün). Aylık çapraz kontrol için #11.
- **AI yöntemi:** Gradient boosting. Özellikler: takvim (gün, ay, tatil) ve yağış lag'ları. Karşılaştırma için Prophet.
- **Wilo bağı:** Dolaylı. Basınçlandırma ve terfi pompalarının günlük çalışma çizelgesine girdi olur (genel pompa).
- **Metrik:** 1 ve 7 gün sonrası için MAPE. Baseline: geçen haftanın aynı günü.
- **Demo puanı: 5.** Tek bir seri, hızlı sonuç verir.
- **Riskler:**
  - İBB serileri **2024 Şubat'ta bitiyor**.
  - #11'de 2020 öncesi ve sonrası arasında **~1000 kat birim farkı** var, Aralık 2019 değeri de anormal. #11 kullanılırsa önce normalize edilmeli.
  - Sıcaklık verisi `datasets.md`'de yok, bu yüzden yaz zirvesini açıklayan önemli bir değişken eksik.

## 2. İçme Suyu Arıtımı

### B1. Su kalitesi parametrelerinden içilebilirlik sınıflandırması
- **Problem:** Laboratuvar sonucunu beklemeden riskli su erkenden işaretlenebilir.
- **Veri:** #19. Kaggle hesabı gerekiyor.
- **AI yöntemi:** Eksik değer doldurma (imputation) ve ardından gradient boosting, açıklanabilirlik için SHAP.
- **Wilo bağı:** Yok. Doğrulanmış bir arıtma ürünü bağlantısı bulamadım (genel pompa).
- **Metrik:** ROC-AUC ve F1.
- **Demo puanı: 4.** Teknik olarak kolay ama değeri zayıf.
- **Riskler:**
  - Verinin nereden ve nasıl toplandığı belli değil.
  - Sonradan eksik değer eklenmiş.
  - Jüri verinin güvenilirliğini sorgulayabilir.

## 3. Dağıtım / Basınçlandırma

### C1. Şebekede kaçak tespiti (SCADA basınç ve debi)
- **Problem:** Kaçaklar haftalar sonra fark ediliyor. Su kaybı ve gereksiz pompa enerjisi oluşuyor.
- **Veri:** #3 BattLeDIM. 2018–2019 basınç, debi ve seviye verisi ile kaçak etiketleri. CSV'ler yaklaşık 190 MB. Login yok.
- **AI yöntemi:** Her sensör için beklenen basıncı tahmin eden bir model (regresyon veya LSTM). Gerçek değerle tahmin arasındaki farka (residual) CUSUM uygulanarak alarm üretilir.
- **Wilo bağı:** Dolaylı. [Wilo-SiBoost Smart Helix VE](https://wilo.com/gb/en/Products/en/application/wilo-siboost-smart-helix-ve?page=2) basma tarafında zaten bir basınç sensörü taşıyor, bu sensör bir kaçak göstergesi olarak kullanılabilir. Ancak BattLeDIM'deki sensörler şebeke sensörleri, pompa sensörü değil.
- **Metrik:** Kaçak tespit F1'i ve tespite kadar geçen ortalama süre (saat). Doğruluk `2018/2019_Leakages.csv` dosyalarına göre ölçülür.
- **Demo puanı: 4.** Etiket hazır. Ancak sensör sayısı ve örnekleme aralığı henüz doğrulanmadı, README'nin okunması gerekiyor.
- **Riskler:**
  - Kaçağın yerini bulmak (lokalizasyon) 3 güne sığmaz. Kapsam yalnız tespitle sınırlı tutulmalı.

### C2. Basınç yönetimi için pompa hızı optimizasyonu
- **Problem:** Gece talep düşükken yüksek basınç hem kaçağı hem de enerji tüketimini artırıyor.
- **Veri:** #2 WNTR ile #1 veya #3'teki EPANET modeli (`L-TOWN.inp`) üzerinde simülasyon.
- **AI yöntemi:** Simülasyondan bir vekil (surrogate) model öğrenilir. Ardından minimum basınç kısıtı altında pompa hızı optimize edilir. Pekiştirmeli öğrenme (RL) bir alternatif.
- **Wilo bağı:** **Doğrudan.** SiBoost Smart Helix VE'deki her pompanın 25–60 Hz frekans konvertörü var. Fikir, bu pompaların hız ayarını belirliyor ([wilo.com](https://wilo.com/gb/en/Products/en/application/wilo-siboost-smart-helix-ve?page=2)).
- **Metrik:** Simüle edilen enerji (kWh/gün) ve kaçak hacmi. Sabit hız senaryosuyla karşılaştırılır. Minimum basınç kısıtı ihlal edilmemeli.
- **Demo puanı: 3.** Simülasyon, vekil model ve optimizasyon üç ayrı katman. 3 gün için riskli.
- **Riskler:**
  - L-TOWN modelinde pompa olup olmadığı doğrulanmadı.

## 4. Pompa sağlığı (tüm halkalarda geçerli)

### P1. Pompa anomali tespiti (titreşim, akım, basınç, debi)
- **Problem:** Pompa arızaları fark edildiğinde iş işten geçmiş oluyor. Plansız duruş ve servis maliyeti doğuyor.
- **Veri:** #5 SKAB. Su pompalı sirkülasyon düzeneğinden 8 sensör ile `anomaly` ve `changepoint` etiketleri. Login yok.
- **AI yöntemi:** Isolation Forest, LSTM autoencoder ve değişim noktası (changepoint) tespiti karşılaştırılır. Alarm eşiği normal çalışma verisinden kalibre edilir.
- **Wilo bağı:** **Doğrudan.**
  - [Wilo-Rexa SUPRA](https://wilo.com/gb/en/Products/en/products-expertise/wilo-rexa-supra?t=0) ve [Wilo-Rexa SOLID](https://wilo.com/ng/en/Catalogue/en/products-expertise/wilo-rexa-solid) DDI üzerinden titreşim, sıcaklık ve kaçak izliyor. Fikir, bu sinyaller üzerine kurulacak bir AI katmanı.
  - Gömülü sistem ve sensör bilgin burada doğrudan işe yarar.
- **Metrik:** Nokta anomaliler için F1, değişim noktaları için tespit gecikmesi (saniye) ve aylık yanlış alarm sayısı.
- **Demo puanı: 5.** Veri küçük ve etiketli, CSV olarak hazır. Canlı akış simülasyonu Streamlit'te kolay.
- **Riskler:**
  - **SKAB GPL-3.0 lisanslı.** Veri repoya konmamalı, `data/raw/` altında tutulup indirme scripti ile alınmalı.
  - Test düzeneği Wilo pompası değil. Gerçek saha verisine genellenmesi kanıtlanmış değil.

### P2. Pompa arıza öncesi uyarı (kestirimci bakım)
- **Problem:** Bir yılda 7 arıza yaşanmış, belirgin bir örüntü görülmüyor. Arızadan önce uyarı vermek gerekiyor.
- **Veri:** #18. 52 sensörlü gerçek su pompası verisi. Kaggle hesabı gerekiyor.
- **AI yöntemi:** Arızadan önceki N saati pozitif olarak etiketleyip sınıflandırma (gradient boosting) yapılır. Alternatif olarak sadece normal veriyle eğitilmiş autoencoder kullanılır.
- **Wilo bağı:** **Doğrudan** (pompa verisi), ama pompanın markası bilinmiyor (genel pompa).
- **Metrik:** Arızadan kaç saat önce uyarı verildiği (lead time), yakalanan arıza oranı (7 arızanın kaçı) ve yanlış alarm sayısı.
- **Demo puanı: 4.** Veri gerçek ve hikâyesi güçlü. Ancak etiket sütunu doğrulanmadı ve 7 olay istatistik için az.
- **Riskler:**
  - **Lisans "Unknown".**
  - Kaggle girişi gerekiyor.
  - Sütun adları ve etiket değerleri doğrulanmadı.

### P3. Pompa iç kaçağı derecelendirmesi
- **Problem:** Pompa iç kaçağı verimi düşürüyor ama dışarıdan görülmüyor.
- **Veri:** #6 UCI Hydraulic Systems. 2,205 döngü, `internal pump leakage` etiketi 0/1/2 seviyeli. Login yok.
- **AI yöntemi:** Basınç, motor gücü ve debi sinyallerinden istatistiksel ve FFT özellikleri çıkarılır, ardından random forest veya gradient boosting ile sınıflandırılır.
- **Wilo bağı:** **Doğrudan, ama kısmi.** Rexa SUPRA'da conta ve sızıntı odası için kaçak algılama var ([wilo.com](https://wilo.com/gb/en/Products/en/products-expertise/wilo-rexa-supra?t=0)). Ancak veri hidrolik yağ devresinden geliyor, su pompasından değil.
- **Metrik:** 3 sınıf için macro-F1 ve karışıklık matrisi.
- **Demo puanı: 5.** Veri temiz, CC BY 4.0 lisanslı, `ucimlrepo` ile tek satırda yükleniyor.
- **Riskler:**
  - Akışkan suyla aynı değil. Jüriye "yöntem transferi" olarak anlatılmalı.

## 5. Atıksu Transferi

### D1. Yağış tahminine dayalı terfi istasyonu pompa kontrolü
- **Problem:** Islak kuyu pompaları seviyeye tepki vererek çalışıyor. Yağmur başlamadan kuyuyu boşaltmadıkları için taşma ve enerji zirvesi oluşuyor.
- **Veri:** #8 SWMM/pyswmm simülasyonu, yağış girdisi olarak #10.
- **AI yöntemi:** Gelen debi tahmin edilir (gradient boosting). Pompa çalışma takvimi buna göre kurallarla veya MPC ile önceden ayarlanır. pyswmm ile kapalı döngüde test edilir.
- **Wilo bağı:** **Doğrudan.** Rexa SOLID harici Wilo-EFC ile hız kontrollü çalışıyor. Rexa SUPRA, DDI üzerinden ModBus/TCP ve OPC UA ile entegre olabiliyor ([SOLID](https://wilo.com/ng/en/Catalogue/en/products-expertise/wilo-rexa-solid), [SUPRA](https://wilo.com/gb/en/Products/en/products-expertise/wilo-rexa-supra?t=0)).
- **Metrik:** Taşma hacmi (m³) ve pompa enerjisi (kWh). Klasik seviye kontrolüyle karşılaştırılır.
- **Demo puanı: 3.** Hazır bir SWMM modeli `datasets.md`'de yok, örnek ıslak kuyu modelini sıfırdan kurmak gerekiyor.
- **Riskler:**
  - #10 **2024'te bitiyor**, ama simülasyon girdisi olarak yeterli.
  - Model sentetik olacak.

## 6. Atıksu Arıtımı

### E1. Arıtma tesisi çıkış kalitesi tahmini
- **Problem:** Çıkış BOİ ve KOİ değerleri geç ölçülüyor, deşarj limiti aşımı sonradan fark ediliyor.
- **Veri:** #7 UCI Water Treatment Plant. 527 gün, 38 değişken. Login yok. Bağlam için #14.
- **AI yöntemi:** Giriş ve ara aşama ölçümlerinden çıkış BOİ, KOİ ve AKM için regresyon. Tesis durumlarını bulmak için kümeleme.
- **Wilo bağı:** Yok veya dolaylı (genel pompa). Doğrulanmış bir arıtma ürünü bağlantısı yok.
- **Metrik:** Çıkış parametreleri için MAE ve R², limit aşımını yakalama oranı.
- **Demo puanı: 4.** Veri çok küçük ve hızlı çalışılır.
- **Riskler:**
  - Veri 1993 tarihli ve tek tesisten.
  - 527 örnek genelleme için az.

## 7. Sulama / Yeniden Kullanım

### F1. Park sulama suyu ihtiyacı analizi
- **Problem:** Yeşil alan sulaması, yağışa bakılmadan sabit bir planla yapılıyor.
- **Veri:** #15 (yıllık sulama suyu, 2017–2025, 9 satır) ve #10 (yağış).
- **AI yöntemi:** Basit regresyon veya kural tabanlı model.
- **Wilo bağı:** Dolaylı. [Wilo-Actun ZETOS](https://wilo.com/us/en_us/Products/en/products-expertise/wilo-actun-zetos) sayfasında tarım ve sulama kullanım alanı olarak geçiyor.
- **Metrik:** Yağışa göre ayarlanmış senaryoda tasarruf edilen su (m³).
- **Demo puanı: 2.** 9 yıllık nokta model eğitmeye yetmiyor. Günlük sulama verisi yok.
- **Riskler:**
  - Veri yetersiz.
  - #10 **2024'te bitiyor**.

## 8. Taşkın Önleme

### G1. Kentsel taşkın için hızlı vekil model (SWMM emülatörü)
- **Problem:** Fiziksel simülasyon yavaş olduğu için yağış anında hızlı risk haritası çıkarılamıyor.
- **Veri:** #8 SWMM ile yağış senaryoları üretilir, gerçekçi yağış profili için #10 kullanılır.
- **AI yöntemi:** Çok sayıda SWMM koşusundan yağış → düğüm taşkın hacmi eşlemesini öğrenen bir vekil model (gradient boosting veya MLP).
- **Wilo bağı:** Dolaylı (genel pompa). Yağmur suyu pompa istasyonu ürünü doğrulanmadı.
- **Metrik:** Vekil modelin SWMM'ye göre taşkın hacmi hatası (MAE) ve hızlanma katsayısı.
- **Demo puanı: 3.** SWMM modeli kurmak ve senaryo üretmek zaman alıyor.
- **Riskler:**
  - #10 **2024'te bitiyor**.
  - Model sentetik.

---

## En güçlü 3 fikir

**Seçim kriteri:**
- Demo puanı ≥4 ve Wilo bağı "Doğrudan" olmalı.
- Eşitlik olursa Türkiye verisi kullanan fikir tercih edilir.
- Kriterlere uyan tam olarak 3 fikir var. Hiçbiri Türkiye verisi kullanmıyor.

| | P1. Pompa anomali tespiti | P3. Pompa iç kaçağı | P2. Arıza öncesi uyarı |
|---|---|---|---|
| Veri | #5 SKAB | #6 UCI Hydraulic | #18 Kaggle pump |
| Login | Yok | Yok | **Kaggle hesabı** |
| Etiket | anomaly + changepoint | pompa kaçağı 0/1/2 | 7 arıza (sütun doğrulanmadı) |
| Lisans | GPL-3.0 (veri repo dışında tutulmalı) | CC BY 4.0 | **Unknown** |
| Akışkan | Su | Hidrolik yağ | Su |
| AI | Isolation Forest / AE / changepoint | Özellik çıkarımı + sınıflandırma | Arıza öncesi pencere sınıflandırma |
| Wilo ürünü | Rexa SUPRA / SOLID (DDI: titreşim, sıcaklık, kaçak) | Rexa SUPRA (conta kaçak algılama) | genel pompa |
| Metrik | F1, tespit gecikmesi, yanlış alarm | macro-F1 | Uyarı süresi, yakalanan arıza oranı, yanlış alarm |
| Demo puanı | 5 | 5 | 4 |
| Ana risk | Test düzeneği gerçek saha değil | Su değil yağ | Lisans belirsiz, 7 olay az |

**Not:** Kriterlerin sonucunda üç fikrin üçü de pompa sağlığı üzerine. Daha çeşitli bir set istersen kriter dışında kalan en iyi iki aday şunlar:
- **A2 (talep tahmini):** Puanı 5, Türkiye verisi kullanıyor, ama Wilo bağı dolaylı.
- **C1 (kaçak tespiti):** Puanı 4, ama Wilo bağı dolaylı.
