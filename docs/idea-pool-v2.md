# Fikir Havuzu v2: problemden başlayarak

**Ana kriter:** Jüri en çok özgünlüğe bakacak.
- P1 (SKAB ile pompa anomali tespiti, bkz. `idea-pool.md`) teknik yedek olarak kalıyor.
- Linklerin hepsi 2026-11-17'de açılıp doğrulandı. Açamadığım kaynaklar "doğrulanamadı" diye işaretli.
- `#n` numaraları `docs/datasets.md`'deki kaynakları gösteriyor.

**Puanların anlamı:**
- **Özgünlük (1–5):** Arama sonuçlarında ne kadar benzer çalışma veya ürün çıktığına göre verildi. 5, benzerini bulamadım demek. "Bulamadım", hiç yok anlamına gelmiyor.
- **Wilo bağı:**
  - Doğrudan: fikir, pompanın kendi verisini ya da kontrolünü kullanıyor.
  - Dolaylı: fikir pompa işletmesini etkiliyor.
- **Demo (1–5):** 3 günde çalışan bir demo çıkarılabilir mi.

---

## 1. Türkiye'de gerçek ama gözden kaçan su problemleri

| # | Problem | Kanıt |
|---|---|---|
| T1 | **Şebekedeki su kaybı yasal hedefin çok üstünde.** *(Güncelleme 2026-11-17: %46 TÜİK bülteninden doğrulanamadı. Resmi rakam Bakanlık'ın %33,54 su kaybı oranı, bkz. `v1-validation.md` c.)* Faturalanamayan su 2024'te %46 (2023'te %47.9). Bu oran 1,391 belediyeyi kapsayan TÜİK anketine dayanıyor. Yasal hedef ise büyükşehir ve il belediyeleri için 2023'e kadar en fazla %30, 2028'e kadar en fazla %25. | %46: TÜİK 2024 verisine atıf yapan bir köşe yazısı, TÜİK bülteninin kendisini açamadım ([İstiklal, 22.09.2025](https://www.istiklal.com.tr/yazarlar/kentsel-su-sisteminde-kayip-ve-kacaklari-1063570h)). Hedefler: [Tarım ve Orman Bakanlığı Genelge 2021/47](https://www.tarimorman.gov.tr/Duyuru/1461/Icme-Suyu-Sistemlerinde-Su-Kayiplarinin-Azaltilmasina-Yonelik-Is-Termin-Plani-Genelgesi-Yururluge-Girmistir) |
| T2 | **Apartman içi kaçaklar sahipsiz kalıyor.** Hidrofor tesisatı ortak alan sayılabiliyor. Kaçağın ortak mı yoksa daireye ait tesisattan mı geldiği önce belirlenmeli. Anlaşmazlıkta mahkeme yoluyla bilirkişi incelemesine gidiliyor. | [FFK Partner Hukuk, 2026 rehberi](https://www.ffkpartnerhukuk.com.tr/apartmanda-surekli-su-kacagi-sorunundan-yonetim-sorumlu-mudur-2026-guncel-rehber/) |
| T3 | **Pompalar elektriğin pahalı saatlerinde çalışıyor.** Çok zamanlı tarifede saat dilimleri: gündüz 06–17, puant 17–22, gece 22–06. Nisan 2022 mesken fiyatlarına göre puant fiyatı gece fiyatının ~2.33 katı (hesaplama bana ait). Aynı haber, "gece tüketiminin de artık yüksek kademeden fiyatlandırıldığını" yazıyor. | [Türkiye Gazetesi, 21.04.2022](https://www.turkiyegazetesi.com.tr/ekonomi/tek-zamanli-tarife-ile-faturanizi-dusurebilirsiniz-850959). Fiyatlar eski, güncel EPDK tablosunu doğrulayamadım. |
| T4 | **Kentsel ani sel ve kanalizasyon taşması.** 4 Temmuz 2026'da İstanbul'da sağanak oldu. Kağıthane'de rögarlar taştı ve bir kanalizasyon borusu patladı. Zincirlikuyu alt geçidi su doldu, Üsküdar Sahaflar Çarşısı yaklaşık 1 m su altında kaldı. | [Gazete Oksijen, 04.07.2026](https://gazeteoksijen.com/turkiye/istanbulda-saganak-etkili-oluyor-caddeler-su-icinde-kaldi-trafik-durdu-281275) |
| T5 | **Kuraklık nedeniyle dönüşümlü kesinti.** İzmir'de 6 Ağustos 2025 ile 6 Şubat 2026 arasında 23:00–05:00 saatlerinde dönüşümlü kesinti yapıldı, 13 ilçe etkilendi. Tahtalı Barajı'nın aktif doluluğu 30 Aralık 2025'te %0.13'e düştü. | [İZSU, 06.02.2026](https://izsu.gov.tr/haberler/tahtali-yukselise-gecti-gece-kesintileri-sona-erdi), [BirGün, 06.08.2025](https://www.birgun.net/haber/izmirde-su-krizi-11-ilcede-uygulanacak-donusumlu-su-kesintisi-ne-zaman-basliyor-643774) |
| T6 | **Konya'da yeraltı suyu çöküşü ve obruklar.** Bazı bölgelerde bir yılda 7–10 m, kimi yerlerde 20 m'nin üzerinde düşüş görüldü. 1 m'den derin kayıtlı obruk sayısı 604. | [Habertürk, 19.08.2024 (Prof. Dr. Fetullah Arık)](https://www.haberturk.com/uzmani-uyardi-iste-obrugun-belirtileri-3712664) |
| T7 | **Depremden sonra şebeke kör kalıyor.** Hatay'da belediye "akut içme suyu probleminin artarak sürdüğünü" açıkladı ve analizler bitene kadar şebeke suyunun içilmemesini önerdi. Sağlık Bakanı da şebeke suyunun içme suyu olarak kullanılmamasını söyledi. | [Yetkin Report, 04.03.2023](https://yetkinreport.com/2023/03/04/hatayda-icme-suyu-problemi-buyuyor/), [Cumhuriyet, 22.02.2023](https://www.cumhuriyet.com.tr/turkiye/bakan-kocadan-deprem-bolgesi-icin-sebeke-suyu-uyarisi-asla-icme-suyu-olarak-kullanmayin-2054270) |

---

## 2. Fikirler

### V1. Hidrofor bir kaçak sensörü olarak (yön a)
- **Problem:** T2 ve T1. Apartmanlardaki gizli kaçaklar fatura gelene kadar fark edilmiyor. Fark edildikten sonra da kaçağın kaynağı tartışmalı oluyor.
- **Fikir:** Ek bir sensör takmadan, pompanın kendi davranışından gece kaçağının debisini (L/h) tahmin etmek.
  - **Basınç anahtarlı (sabit hızlı) hidroforlarda** bakılacak sinyaller: gece kalkış sayısı, duruş aralıkları, çalışma süresi ve motor akımı.
  - **Frekans konvertörlü (VFD) ünitelerde** pompa sürekli düşük hızda çalıştığı için aç-kapa döngüsü olmuyor. Bunun yerine gece minimum güç ve frekans seviyesine bakılır.
- **Neden özgün:**
  - Benzeri var: [Grundfos SCALA](https://grundfos.com/uk/learn/research-and-insights/operational-risks-in-a-pressure-boosting-system) ev tipi booster pompasının bir "anti-cycling" özelliği var. Küçük bir kaçak ya da açık kalmış bir musluk algılayınca pompayı durduruyor.
  - Fark 1: SCALA tek bir evde kaçağı algılayıp pompayı kapatıyor. Bizim fikir **çok daireli bir binada kaçağın debisini sayısal olarak tahmin ediyor**, gece kullanımını kaçaktan ayırıyor ve yöneticiye kanıt niteliğinde bir rapor veriyor.
  - Fark 2: Kaçağın pompa döngüsünden nicel olarak tahmin edildiği bağımsız bir akademik çalışma bulamadım. Bulduğum kaynaklar üretici ve tesisatçı yazılarıydı.
  - **Özgünlük: 4.**
- **Veri:** Sentetik fizik simülasyonu (Python, ~150 satır).
  - **Basınç tankı:** Boyle yasasıyla modellenir.
  - **Pompa:** Pompa eğrisi H(Q), basınç anahtarı ya da VFD için PI kontrol.
  - **Talep:** N daire, günün saatine göre Poisson dağılımlı musluk açma olayları.
  - **Kaçak:** Sabit küçük bir debi. Etiketler bilindiği için doğruluk ölçülebilir.
  - **Akım:** Hidrolik güç / verimden hesaplanır.
  - Parametreler gerçek bir binadan değil, benim varsayımlarım.
- **AI yöntemi:**
  - Her gece için özellik çıkarımı (02–05 penceresi): döngü istatistikleri, minimum güç.
  - Gradient boosting ile kaçak debisi regresyonu.
  - Sahada etiket olmayacağı için her binanın kendi geçmişine göre değişim noktası (changepoint) tespiti.
- **Wilo bağı: Doğrudan.** [Wilo-SiBoost Smart Helix VE](https://wilo.com/gb/en/Products/en/application/wilo-siboost-smart-helix-ve?page=2) konut binaları için tasarlanmış. Her pompada frekans konvertörü ve basma tarafında 4–20 mA basınç sensörü var. Tek pompalı küçük hidroforlar için genel pompa.
- **Metrik:**
  - Sabit yanlış alarm oranında (örn. ayda en fazla 1) tespit edilebilen en küçük kaçak (L/h).
  - Kaçak debisi tahmininde MAE (L/h).
  - Kaçak başladıktan sonra tespite kadar geçen gece sayısı.
- **Demo: 4.** Fizik basit ve senin elektrik-elektronik bilginle örtüşüyor. Streamlit'te "kaçak kaydırıcısı → gece imzası değişiyor" gösterimi etkileyici olur.
- **Riskler:**
  - "Ek donanım yok" iddiası, kontrol ünitesinin verisine erişilebiliyorsa geçerli. SiBoost'un dışarıya veri verip vermediğini doğrulamadım. Erişilemiyorsa akım pensi gibi basit bir sensör gerekir.
  - Gece meşru kullanımı (sifon, yaşlı sakinler) kaçakla karışabilir.

### V2. Su deposunu batarya gibi kullanmak (yön b)
- **Problem:** T3. Depo dolumu tarifeden bağımsız yapılıyor, pompalar puant saatlerinde de çalışıyor.
- **Fikir:** Talep tahmini ile çok zamanlı tarifeye göre bir pompa takvimi optimizasyonunu birleştirmek: depo gece dolsun, puantta pompa mümkün olduğunca dursun.
- **Neden özgün:**
  - Şebeke ölçeğinde **ticari ürünler var**. Örneğin [SUEZ Aquadvanced](https://suez.com/en/uk/water-network-management/real-time-management-and-optimisation/real-time-energy-management) "spot fiyat dahil her tarifeyi yönetebildiğini" söylüyor.
  - Aramada çok sayıda akademik LP/MILP çalışması da çıktı (tam metinlerini açmadım).
  - Özgün olabilecek tek açı **apartman ölçeği** (çatı deposu ve hidrofor). Bu ölçekte benzer çalışma aramadım, bilmiyorum.
  - **Özgünlük: 2** (şebeke ölçeğinde) / **3?** (bina ölçeğinde).
- **Veri:**
  - Günlük talep seviyesi için #10 (İBB günlük tüketim).
  - Saatlik profil sentetik olacak, çünkü `datasets.md`'de saatlik talep verisi yok.
  - Depo ve pompa modeli için #2 WNTR ya da basit bir kütle dengesi.
- **AI yöntemi:** Gradient boosting ile talep tahmini, ardından MILP ile pompa takvimi (PuLP veya scipy). Tahmin belirsizliği için güvenlik payı bırakılır.
- **Wilo bağı: Doğrudan.** SiBoost Smart Helix VE'deki frekans konvertörlü pompalar ve [Wilo-Actun ZETOS](https://wilo.com/us/en_us/Products/en/products-expertise/wilo-actun-zetos) (sayfasında belediye şebekesi ve basınçlandırma kullanımı geçiyor).
- **Metrik:**
  - Günlük enerji maliyeti (TL). Karşılaştırma: "depo seviyesi düşünce pompala" kuralı.
  - Depo minimum seviye ihlali sayısı 0 olmalı.
  - Puant saatlerinde pompalanan su (m³).
- **Demo: 4.**
- **Riskler:**
  - Tarife fiyatları 2022'den kalma.
  - Meskende gece fiyatı avantajı kalmamış olabilir (T3).
  - İBB serileri **2024'te bitiyor**.
  - Saatlik profil sentetik.

### V3. Yağış tahminiyle terfi istasyonu kuyusunu önceden boşaltmak (yön c)
- **Problem:** T4. Islak kuyu pompaları seviyeye tepki vererek çalışıyor. Sağanak başladığında kuyu zaten dolu olduğu için taşma ve rögar taşması oluyor.
- **Fikir:** Yağış tahmini, her kuyu için ayrı bir "önceden boşaltma" kararını tetikliyor. Kuru hava dönemindeki normal debi de tahmin edilerek kuyunun gereksiz yere boş kalması önleniyor.
- **Neden özgün:**
  - **Benzeri var.** [Icke ve ark., 2017 (DWES)](https://dwes.copernicus.org/articles/10/69/2017/) Hollanda'daki Bennekom atıksu arıtma tesisinde yağış ve kuru hava debisi tahminiyle prediktif kontrol uyguladı ve ön arıtmayı atlayan (bypass) hacmin yaklaşık %50'sinin önlenebileceğini gösterdi.
  - Fark: Bu çalışma tesis girişini merkezî olarak kontrol ediyor. Bizim fikir **istasyon bazında**, pompanın kendi verisi ve herkese açık yağış tahminiyle çalışıyor ve Türkiye bağlamında.
  - **Özgünlük: 3.**
- **Veri:** #8 SWMM/pyswmm ile ıslak kuyu, toplama alanı ve pompa modeli. Gerçekçi yağış serisi için #10 (İBB baraj yağışları).
- **AI yöntemi:**
  - Yağıştan kuyuya gelecek debinin tahmini (gradient boosting).
  - Basit model öngörülü kontrol (MPC) ya da kural tabanlı ön boşaltma.
  - pyswmm ile kapalı döngü test.
- **Wilo bağı: Doğrudan.**
  - [Wilo-Rexa SOLID](https://wilo.com/ng/en/Catalogue/en/products-expertise/wilo-rexa-solid) harici Wilo-EFC ile hız kontrollü çalışıyor.
  - [Wilo-Rexa SUPRA](https://wilo.com/gb/en/Products/en/products-expertise/wilo-rexa-supra?t=0) DDI üzerinden ModBus/TCP ve OPC UA destekliyor.
- **Metrik:** Taşma hacmi (m³), pik pompa gücü (kW) ve pompa kalkış sayısı. Karşılaştırma: klasik seviye kontrolü.
- **Demo: 3.** SWMM ıslak kuyu modelini sıfırdan kurmak gerekiyor.
- **Riskler:**
  - #10 **2024'te bitiyor**.
  - Model sentetik.
  - Tahmin yanlışsa kuyu boşuna boşaltılır ve fazladan enerji harcanır. Bu durum metrikte ayrıca gösterilmeli.

### V4. Kuyu pompası bir akifer sensörü olarak (yeni yön)
- **Problem:** T6. Yeraltı suyu seviyesi hızla düşüyor ama binlerce sulama kuyusunun büyük çoğunluğunda seviye ölçülmüyor.
- **Fikir:** Kuyu pompasının akım, gerilim ve (varsa) frekans verisinden **dinamik su seviyesini** tahmin etmek.
  - Seviye düştükçe basma yüksekliği artar, pompanın çalışma noktası kayar ve güç ile debi değişir.
  - Ek sensör gerekmez. Bütün kuyulardan toplanan veri bölgesel bir "akifer haritası" verir.
- **Neden özgün:**
  - Aramada motor akımından kuyu seviyesini çıkaran bir ABD patenti ("Non-invasive well level monitoring", US 12066313) ve bir IoT kuyu izleme çalışması çıktı. İkisini de açıp doğrulayamadım.
  - Konya ölçeğinde, pompa filosunu ortak bir sensör ağı olarak kullanan bir çalışma bulamadım.
  - **Özgünlük: 4** (patent doğrulanırsa 3'e iner).
- **Veri:** Sentetik gri-kutu model. Bileşenler:
  - **Pompa:** Pompa eğrisi H(Q) ve hız değişimi için afinite yasaları.
  - **Motor:** Motor verimi.
  - **Kuyu seviyesi:** Yıllık düşüş trendi, mevsimsellik ve pompalama sırasındaki düşüm (drawdown).
  - Parametreler varsayım. T6'daki gerçek düşüş değerleri senaryo aralığı olarak kullanılabilir.
- **AI yöntemi:**
  - Fizik bilgili regresyon: pompa eğrisi parametreleri öğrenilir.
  - Seviye trendi için Kalman filtresi.
  - Karşılaştırma için sadece veriye dayalı gradient boosting.
- **Wilo bağı: Doğrudan.** [Wilo-Actun ZETOS](https://wilo.com/us/en_us/Products/en/products-expertise/wilo-actun-zetos) ham su alma ve kuyu pompası, sayfasında tarım ve sulama kullanımı da geçiyor. Ürün sayfasında izleme seçeneği geçmediği için bu fikir doğrudan bir **eksikliği dolduruyor**.
- **Metrik:** Dinamik seviye tahmininde MAE (m), yıllık düşüş trendi hatası (m/yıl) ve pompa aşınması gibi karıştırıcı etkiler altında sağlamlık.
- **Demo: 4.** Fizik basit ve senin elektrik-elektronik bilginle örtüşüyor. Harita ile zaman serisi görselleştirmesi güçlü bir sunum çıkarır.
- **Riskler:**
  - Kum, aşınma ve filtre tıkanması da akımı değiştirir. Seviye etkisini bunlardan ayırmak için dönemsel bir manuel seviye ölçümüyle kalibrasyon gerekebilir.
  - Gerçek veriyle doğrulanmamış olacak.

### V5. Deprem sonrası hasarlı bölgeyi hızla bulmak ve önceliklendirmek (yeni yön)
- **Problem:** T7. Depremden sonra şebekenin neresinin hasarlı olduğu bilinmiyor. Su verilmeye devam ettikçe hem su kaçıyor hem de kirlenme riski büyüyor.
- **Fikir:** Az sayıdaki basınç sensörü ile pompa istasyonlarının debi ve güç verisinden hasarlı bölgeleri dakikalar içinde sıralamak. Ardından hangi vanaların kapatılacağına ve hangi pompaların çalışacağına karar vermek.
- **Neden özgün:**
  - [WNTR'de deprem modülü](https://usepa.github.io/WNTR/disaster_models.html) var: PGA, PGV, onarım oranı, kırılganlık (fragility) eğrileri.
  - Derin öğrenmeyle afet sonrası onarım sıralaması üzerine çalışmalar var, örneğin [Alemzadeh ve ark., 2020](https://arxiv.org/abs/2007.05880). Bu çalışma birbirine bağımlı altyapılar üzerine, doğrudan su şebekesi değil.
  - Aramada su şebekesi için GNN veya DRL ile onarım sıralaması çalışmaları da görüldü, açamadım.
  - **Özgünlük: 3.**
- **Veri:** #2 WNTR deprem senaryoları (Monte Carlo) #3 L-TOWN ya da WNTR'nin örnek ağı üzerinde. Etiketler simülasyondan gelir.
- **AI yöntemi:** Sensör desenlerinden hasarlı bölgeyi sınıflandırma (gradient boosting veya GNN). Vana izolasyonu için açgözlü (greedy) arama.
- **Wilo bağı: Dolaylı** (genel pompa). Pompa istasyonu verisi ek bir sensör olarak kullanılıyor.
- **Metrik:** Hasarlı bölgeyi ilk 3 tahminde bulma oranı (top-3 accuracy) ve ilk 72 saatte hizmet verilen nüfus oranı (simülasyonda).
- **Demo: 3.**
- **Riskler:**
  - WNTR deprem modülü düğüm koordinatlarının metre cinsinden olmasını istiyor. L-TOWN modelinin koordinat birimini doğrulamadım.
  - Kapsamı büyük.

### V6. Kuraklıkta adil dönüşümlü kesinti planı (yeni yön)
- **Problem:** T5. Kesinti takvimi elle hazırlanıyor. Yüksek bölgeler ve şebeke sonundaki aboneler daha az su alıyor. Kesinti bitince bütün bölgeler aynı anda dolmaya çalıştığı için pompalarda pik oluşuyor.
- **Fikir:** Hangi bölgenin hangi gece kesileceğini optimize etmek. Amaçlar: verilen su hacminde eşitlik ve dolum sırasındaki pompa pikini bölgeleri sırayla açarak düşürmek.
- **Neden özgün:**
  - **Benzeri var.** [Kurian ve ark., 2023 (Water Supply)](https://rbcdsai.iitm.ac.in/publications/equitable-supply-in-intermittently-operated-rural-water-networks) MINLP ile eşitliği optimize ediyor ve takvimin ölçümlerden de çıkarılabileceğini gösteriyor.
  - Fark: Kesinti sonrası yeniden dolumda pompa pikini de hesaba katıyor ve büyükşehir ölçeğinde.
  - **Özgünlük: 2.**
- **Veri:** #2 WNTR, basınca bağlı talep (pressure-dependent demand) simülasyonuyla, #3 L-TOWN üzerinde.
- **AI yöntemi:** Vekil (surrogate) model ile genetik algoritma veya Bayesian optimizasyon.
- **Wilo bağı: Dolaylı** (genel pompa).
- **Metrik:** Bölgelere verilen hacmin Gini katsayısı, tasarruf edilen su (m³) ve dolum sırasındaki pik pompa gücü (kW).
- **Demo: 3.**
- **Riskler:**
  - EPANET ve WNTR sürekli besleme için tasarlandı. Kesintili beslemeyi modellemek için ek modelleme gerekebilir.

### Elenen yön
- **Atıksu pompasında tıkanma tahmini (ıslak mendil):** [Wilo-Rexa SOLID](https://wilo.com/ng/en/Catalogue/en/products-expertise/wilo-rexa-solid)'in zaten tıkanma algılama algoritması var, bu yüzden özgünlüğü düşük.

---

## 3. Karşılaştırma

| Fikir | Özgünlük | Wilo bağı | Demo | Veri | Türkiye bağlamı |
|---|---|---|---|---|---|
| **V1** Hidrofor = kaçak sensörü | **4** | Doğrudan (SiBoost Smart Helix VE) | **4** | Sentetik fizik | T1, T2 |
| **V4** Kuyu pompası = akifer sensörü | **4** (3?) | Doğrudan (Actun ZETOS) | **4** | Sentetik fizik | T6 (Konya) |
| **V3** Yağış tahminli ön boşaltma | 3 | Doğrudan (Rexa SOLID / SUPRA) | 3 | pyswmm + İBB yağış | T4 (İstanbul) |
| V5 Deprem sonrası hasar bölgesi | 3 | Dolaylı | 3 | WNTR deprem | T7 (Hatay) |
| V2 Depo = batarya | 2 / 3? | Doğrudan (SiBoost, Actun ZETOS) | 4 | İBB tüketim + sentetik | T3 |
| V6 Adil kesinti planı | 2 | Dolaylı | 3 | WNTR | T5 (İzmir) |

**Önerilen ilk 3** (önce özgünlük, sonra Wilo bağı, sonra demo puanına göre):
1. **V1, Hidrofor = kaçak sensörü.**
2. **V4, Kuyu pompası = akifer sensörü.**
3. **V3, Yağış tahminli ön boşaltma.** Puanları V2'ye yakın, ama V2'nin şebeke ölçeğinde ticari karşılığı olduğu için özgünlükte geride kaldı.

**Not:** V1 ve V4 aynı tezi paylaşıyor: *"Pompa zaten bir sensör."* İkisi tek bir sunumda "Wilo pompası = sahadaki sensör ağı" olarak birleştirilebilir. Bu da Wilo'nun "Connecting" ayağına doğrudan oturur.
