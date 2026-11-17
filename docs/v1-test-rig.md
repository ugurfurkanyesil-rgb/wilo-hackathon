# V1 Fiziksel Test Düzeneği

Durum: tasarım aşamasında, firmware yazılmadı. Tarih: 2026-11-17.

**İşaretler:** [K] kaynaklı · [V] varsayım · [T] türetilmiş (hesap bana ait).

**Amaç:** 12 V'luk küçük bir hidroforla bina hidroforunun aç-kapa döngüsünü taklit etmek. Bu düzenekte:
1. Simülasyonla **aynı CSV sütunlarında** veri üretmek.
2. Kaçak debisini **tartarak** gerçek değeriyle (ground truth) ölçmek.
3. `v1-simulation-design.md` §0'daki argümanı, yani "kaçak T_off'tan görülür", gerçek donanımda test etmek.

---

## 1. Ana bileşenlerin seçimi ve gerekçesi

### 1.1 Pompa: 12 V, dahili basınç şalterli diyafram pompa
Önerilen model: **SEAFLO SFDP1-012-035-21** (21 serisi).

| Özellik | Değer | Kaynak |
|---|---|---|
| Gerilim | 12 V DC | [K] [Jinbo Marine 21 serisi](https://www.jinbomarine.com/Diaphragm-Pump-21-Series-DC), [idefix ürün sayfası](https://www.idefix.com/seaflo-hidrofor-pompasi-12v-43-ldk-35-psi-p-21696730) |
| Açık debi | 4,3 L/dk | [K] aynı kaynaklar |
| Kapanma basıncı | 35 psi ≈ 2,41 bar | [K] |
| Yeniden kalkış basıncı | 25 ± 5 psi ≈ 1,72 ± 0,34 bar | [K] Jinbo Marine |
| Maksimum akım | 4,0 A | [K] |
| Sigorta | 6,0 A | [K] Jinbo Marine |
| Basınç şalteri | Dahili | [K] |

- Jinbo Marine sayfası SEAFLO'dan söz etmiyor. Model numarası ve değerler idefix'teki SEAFLO ürün sayfasıyla uyuşuyor.
- **Çalıştırma gücü:** 12 V × 4,0 A = **48 W** (maksimum) [T].
- **Histerezis:** 2,41 − 1,72 ≈ **0,69 bar** [T]. Bu, Modbus'taki 0,1 bar adımlarla yalnızca ~6–7 adım eder. Kuantizasyonun etkisini test etmek için iyi bir durum.
- Yeniden kalkış basıncında ±0,34 bar tolerans var [K]. Bu yüzden ΔV, ürün değerlerinden değil, **veriden kalibre edilmeli** (simülasyon dokümanı §5).

### 1.2 Basınç tankı (akümülatör)
Önerilen model: **SEAFLO 0,75 L membranlı akümülatör** (AT07512501).

| Özellik | Değer | Kaynak |
|---|---|---|
| Hacim | 0,75 L | [K] [Cactus Navigation](https://www.cactusnav.com/seaflo-at07512501-pressurised-accumulator-water-tank-075l-p-33915.html) |
| Fabrika ön dolumu | 10 psi (0,7 bar) | [K] |
| Maksimum basınç | 125 psi (8,6 bar) | [K] |
| Bağlantı | 1/2" MNPT, hava için oto lastik sibobu | [K] |

- Ön dolum, pompanın kalkış basıncının ~0,2 bar altına ayarlanacak [V]. Aramada "kalkış basıncının 3 psi altı" kuralı görüldü ama ürünün kendi talimatında doğrulayamadım.
- **Tanktan çekilebilen su (ΔV), Boyle yasasıyla** [T]: p0 = 1,5 bar(g), p_on = 1,72 bar(g), p_off = 2,41 bar(g) ve 1,013 bar atmosfer basıncı ile
  ΔV = 0,75 L × 2,513 × (1/2,733 − 1/3,423) ≈ **0,14 L**.
- **Beklenen durma süresi** T_off ≈ ΔV / Q_kaçak [T]:
  - 2 L/h → ~250 s
  - 5 L/h → ~100 s
  - 20 L/h → ~25 s
  - 50 L/h → ~10 s
- **Sonuç:** 1 s okuma aralığı küçük kaçaklarda yeterli. 50 L/h'te T_off ~10 s'ye iniyor ve hata büyüyor. Bu aralık için daha büyük bir tank (örn. 2 L) **seçenek** olarak tutulmalı [V].

### 1.3 Güç ölçümü: INA226 (INA219 ve ACS712 yerine)

| Seçenek | Kapasite | Bu pompa için | Kaynak |
|---|---|---|---|
| INA219 (Adafruit kartı) | ±3,2 A (0,1 Ω şönt), 26 V'a kadar, 12 bit | **Yetmez.** Pompanın maksimum akımı 4,0 A, sınırı aşıyor. | [K] [Adafruit](https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout), [TI INA219](https://www.ti.com/document-viewer/INA219/datasheet/specifications) |
| ACS712-05B | ±5 A, 185 mV/A, 5 V besleme | Akım aralığı yeter, ama **gerilim ölçmez**. Güç yalnızca P ≈ V_nom·I ile yaklaşık hesaplanır. Analog çıktı ayrıca bir ADC kanalı gerektirir. | [K] Allegro datasheet değerleri, arama özeti üzerinden; PDF'i açmadım ([kopya](https://components101.com/sites/default/files/component_datasheet/ACS712%2030a%20range%20current%20sensor%20datasheet.pdf)) |
| **INA226 + 10 mΩ şönt** | 0–36 V, 16 bit, ±81,92 mV şönt girişi, I²C, 16 adres | **Seçildi.** Gerilim ve akımı aynı anda ölçer, P = V·I doğrudan çıkar. | [K] [TI INA226](https://www.ti.com/product/INA226). ±81,92 mV ve 2,5 µV LSB: [K] TI datasheet tablosu (arama özeti üzerinden). |

10 mΩ şönt ile [T]:
- Tam skala akım 81,92 mV / 10 mΩ = **8,19 A**. Kalkış akımı için pay bırakıyor.
- Akım çözünürlüğü 2,5 µV / 10 mΩ = **0,25 mA**.
- 4 A'de şöntte harcanan güç 4² × 0,01 = **0,16 W**.

**Dikkat:** Piyasadaki INA226 kartlarının bir kısmı 0,1 Ω (R100) şöntle geliyor. Bu durumda tam skala ~0,82 A olur ve kart **yetmez** [T]. Alırken şöntün **R010 (10 mΩ)** olduğu kontrol edilmeli, gerekirse şönt değiştirilmeli [V].

**Simülasyonla eşleştirme:** INA226'dan gelen P = V_bus × I değeri `power_w` sütununa tam sayı W olarak yazılır. Böylece Modbus `powerInput` register'ının 1 W çözünürlüğü taklit edilir. Ham akım ve gerilim, yalnız düzeneğe ait sütunlarda saklanır (§4).

### 1.4 Basınç: analog sensör + ADS1115
**Sensör:** 0,5–4,5 V çıkışlı, 5 V beslemeli, G1/4 dişli analog sıvı basınç sensörü. Örnek: DFRobot SEN0257.

| Özellik | Değer | Kaynak |
|---|---|---|
| Aralık | 0–1,6 MPa (16 bar) | [K] [DFRobot wiki](https://wiki.dfrobot.com/Gravity__Water_Pressure_Sensor_SKU__SEN0257) |
| Çıkış | 0,5–4,5 V | [K] |
| Doğruluk | %0,5–1 FS (0–55 °C'de %0,5) | [K] |
| Yanıt süresi | < 2 ms | [K] |

**ADC: ADS1115.** 16 bit, 8–860 SPS, PGA ±0,256 V – ±6,144 V, besleme 2,0–5,5 V, 4 seçilebilir I²C adresi [K: [TI ADS1115](https://www.ti.com/product/ADS1115)].

**Çözünürlük karşılaştırması** [T]:

| Adım | Değer |
|---|---|
| Sensör eğimi | 4 V / 16 bar = 0,25 V/bar |
| Gerilim bölücü | 10 kΩ / 20 kΩ, ×0,667. 4,5 V çıkış 3,0 V'a iner, ADS1115 3,3 V'ta beslendiği için güvenli tarafta kalır [V: tasarım tercihi]. |
| ADS1115 LSB (PGA ±4,096 V) | 4,096 / 32768 = 125 µV |
| Sensör tarafında LSB | 125 µV / 0,667 = 187,5 µV, yani **≈ 0,00075 bar** |
| Modbus kuantizasyonu | **0,1 bar**, yani ~130 kat daha kaba |
| Sensörün mutlak doğruluğu | %0,5–1 × 16 bar = **±0,08–0,16 bar** |

**Sonuç:**
- ADC çözünürlüğü bir sorun değil. Sınırlayıcı olan, **sensörün mutlak doğruluğu**. Bu da Modbus'taki 0,1 bar adımla aynı mertebede.
- Düzenek ham basıncı yüksek çözünürlükle kaydeder, `pressure_bar` sütunu ise yazılımda 0,1 bar'a kuantize edilir. Böylece "gerçek Modbus" ile "ideal sensör" aynı veride karşılaştırılabilir.
- Düzenekte basınç 1,7–2,4 bar aralığında. 16 bar'lık sensör bu aralıkta tam skalanın ~%15'ini kullanıyor. Mümkünse 0–0,5 MPa aralıklı bir sensör tercih edilmeli [V: böyle bir modelin Türkiye'de bulunabildiğini doğrulamadım].
- Sensör oransal çalışıyor, yani çıktısı besleme gerilimine bağlı [V: datasheet'te doğrulanmadı]. Bu yüzden 5 V hattı da bir bölücüyle ADS1115'in A1 kanalından ölçülür ve okumalar buna göre düzeltilir.

### 1.5 Gerçek kaçak debisi: tartım
- Kaçak vanasından akan su bir kapta toplanır. Kap, **yük hücresi (load cell) + HX711** üzerinde durur.
- HX711: 24 bit, 10 veya 80 SPS, kazanç 32/64/128 [K: arama özeti; [Avia HX711 datasheet kopyası](https://e2e.ti.com/cfs-file/__key/communityserver-discussions-components-files/73/HX711.pdf), PDF'i açmadım].
- Yük hücresi 5 kg, kap 3–4 L [V].
- **Hesap:** Q_gerçek [L/h] = eğim(kütle [g], zaman [s]) × 3,6 / ρ. ρ ≈ 1 kg/L [V]. Eğim, kayan bir pencerede doğrusal regresyonla bulunur.
- **Duyarlılık** [T]:
  - 2 L/h = 0,56 g/s, 10 dakikada ~333 g.
  - 50 L/h = 13,9 g/s, 3 L'lik kap ~3,6 dakikada dolar. Uzun deneylerde kabın boşaltılması gerekir.
- **Kalibrasyon:** Bilinen ağırlıklarla, ya da mutfak terazisinde tartılmış su şişeleriyle.
- **Ucuz akış sensörü kullanılmıyor.** 2–50 L/h aralığında güvenilir değiller.

---

## 2. Kaçak ve kullanım senaryolarının donanımdaki karşılığı

| Senaryo (simülasyondaki kod) | Donanım | Gerçek değer |
|---|---|---|
| L0, kaçak yok | Bütün vanalar kapalı | Tartım eğimi ≈ 0 |
| LP, boru sızıntısı | **İğneli vana** (ince ayar). Her ayar için debi tartımla ölçülür. | Tartım eğimi |
| LR, sızan rezervuar | 12 V, normalde kapalı **solenoid vana S1**. ESP32 periyodik darbeler verir (V_trig / q_r periyodu, t_fill süre). Akan su teraziye gider. | Tartım eğimi + darbe zamanları |
| Gece meşru kullanımı (sifon) | **Solenoid vana S2**, rastgele zamanlarda kısa açılır. Akan su teraziye değil, giriş kovasına döner. | S2 açılma kaydı |
| Normal kullanım | Elle açılan küresel vana ("musluk"), giriş kovasına döner | Elle not |

`gt_leak_type` sütunu deney protokolünden doldurulur: none, pipe ya da reservoir.

---

## 3. Bağlantı şeması

### 3.1 Hidrolik
```
[Giriş kovası] → (süzgeç) → POMPA giriş
POMPA çıkış → T1 ─┬─ AKÜMÜLATÖR 0,75 L
                  └─ T2 ─┬─ BASINÇ SENSÖRÜ (G1/4)
                         └─ MANİFOLD ─┬─ İğneli vana ───────→ hortum → [TERAZİ KABI]   (LP)
                                      ├─ Solenoid S1 (NC) ──→ hortum → [TERAZİ KABI]   (LR)
                                      ├─ Solenoid S2 (NC) ──→ hortum → [Giriş kovası]  (sifon)
                                      └─ Küresel vana ──────→ hortum → [Giriş kovası]  (musluk)
```
- Pompa hortum bağlantısı 3/8" [K]. Akümülatör 1/2" MNPT [K]. Arada adaptör gerekir.
- Bütün bağlantılarda teflon bant kullanılmalı. Düzenek **kendi kaçağı olmadan** çalışmalı, bu ilk testte L0 ile doğrulanır.

### 3.2 Elektrik
```
12 V kaynağı (adaptör veya akü)
  (+) → SİGORTA 6 A → INA226 VIN+ ; INA226 VIN− → POMPA (+)
                                     INA226 VBUS → VIN− (yük tarafı gerilimi)
  (−) → POMPA (−) → ortak GND
  (+) → Buck dönüştürücü 12→5 V → 5V hattı
        5V → ESP32 VIN, basınç sensörü (kırmızı)
  (+) → S1 (+), S2 (+) ; S1 (−) → MOSFET Q1 drain ; S2 (−) → MOSFET Q2 drain
        Her solenoid bobinine ters paralel flyback diyot (1N4007 veya Schottky)

ESP32 3V3 → INA226 VCC, ADS1115 VDD, HX711 VCC
ESP32 GND → hepsinin GND'si (ortak)

I²C:   GPIO21 (SDA), GPIO22 (SCL) → INA226 (0x40) + ADS1115 (0x48, ADDR=GND)
ADS1115 A0 ← bölücü (10k üst / 20k alt) ← basınç sensörü sinyali (sarı)
ADS1115 A1 ← bölücü (10k / 20k) ← 5V hattı
HX711:  DT → GPIO16, SCK → GPIO17 ; E+/E−/A+/A− → yük hücresi
MOSFET: GPIO25 → 100 Ω → Q1 gate (100 kΩ ile GND'ye çekili)
        GPIO26 → 100 Ω → Q2 gate (100 kΩ ile GND'ye çekili)
        Q1, Q2 lojik seviyeli N-MOSFET, source → GND
```
- Pin seçimleri ve I²C adresleri [V]. Modül adresleri A0/A1/ADDR pinlerine bağlı, alınan modüle göre kontrol edilmeli.
- Akım yolu: 12 V kaynağının akımı, pompanın 4 A maksimumu ve solenoidler için pay bırakmalı (örn. ≥ 6 A) [V].
- **Güvenlik:**
  - Elektronik su tarafının üstünde ve damlama tepsisinin dışında olmalı.
  - Sigorta pompanın besleme hattında olmalı.
  - Islak elle 12 V hattına dokunulmamalı.

---

## 4. Örnekleme ve kayıt

| Kaynak | İç örnekleme | Not |
|---|---|---|
| INA226 (V, I) | 10 Hz [V] | Kalkış ve duruş anlarını hassas yakalamak için |
| ADS1115 (basınç, 5 V) | 10 Hz [V] (ADC 128 SPS'te, ortalama alınır) | |
| HX711 | 10 SPS [K: seçilebilir hız] | Daha düşük hızda 50/60 Hz şebeke gürültüsü bastırılır [K: Adafruit HX711 sayfası, arama özeti] |
| Kayıt (CSV satırı) | **1 Hz** [V] | Simülasyondaki Δt_poll = 1 s ile aynı |

- **Modbus taklidi:** Her saniye başında, ortalama değil **anlık** değerler yazılır.
  - `pump1_running` = power_w > P_eşik. P_eşik ≈ 5 W [V], L0 verisiyle ayarlanır.
  - Kalkış sayaçları, `pump1_running`'in 0'dan 1'e geçişlerinden **kümülatif** olarak türetilir.
  - `pump1_hours_total` = floor(toplam çalışma süresi / 3600 s). Kısa deneylerde 0 kalır, bu beklenen bir durum.
- **Zaman damgası:** Seri port üzerinden dizüstü bilgisayara gönderilir ve bilgisayardaki Python kaydedici zaman damgasını ekler. SD kart ve NTP İleri aşamaya bırakıldı [V].

### CSV şeması (simülasyonla aynı sütunlar)

| Sütun | Düzenekte nereden gelir |
|---|---|
| `timestamp` | Bilgisayar saati (ISO 8601) |
| `pressure_bar` | ADS1115 → bar → **0,1 bar'a kuantize** |
| `pump1_running` | power_w > P_eşik |
| `system_starts_total` | Kümülatif kalkış sayısı (tek pompada pump1 ile aynı) |
| `pump1_starts_total` | Kümülatif kalkış sayısı |
| `pump1_hours_total` | floor(çalışma süresi / 3600) |
| `power_w` | INA226 V × I, tam sayı W |
| `speed_rpm` | **Boş.** DC diyafram pompada hız ölçümü yok. |
| `flow_calc_m3h` | **Boş.** Ucuz debimetre kullanılmıyor, Wilo'nun hesapladığı debinin karşılığı yok. |
| `gt_leak_lph` | Tartım eğiminden (L/h) |
| `gt_leak_type` | Deney protokolünden: none / pipe / reservoir |
| `gt_demand_lph` | S2 açıkken kalibre edilmiş S2 debisi, kapalıyken 0 |

**Yalnız düzeneğe ait ek sütunlar** (`rig_` ön ekli, modele girdi olmaz):
`rig_pressure_raw_bar`, `rig_bus_v`, `rig_current_a`, `rig_mass_g`, `rig_v5_rail`, `rig_s1_open`, `rig_s2_open`, `rig_run_edge_ms` (10 Hz'de yakalanan kalkış/duruş anı).

---

## 5. Deney protokolü (taslak)

1. **Kalibrasyon:**
   - Terazi, bilinen ağırlıklarla.
   - Basınç sensörü, referans bir manometreyle [V].
   - INA226, multimetreyle.
   - Akümülatörün ön dolum basıncı, lastik manometresiyle.
2. **Sızdırmazlık (L0):** Bütün vanalar kapalıyken ≥ 30 dk [V]. Tartım eğimi sıfır olmalı ve beklenen davranış "kalkış yok ya da çok seyrek kalkış".
3. **LP:** İğneli vana 4–5 ayarda, her biri ≥ 30 dk [V]. Hedef aralık ~2–50 L/h.
4. **LR:** S1 darbeleri, 2–3 farklı periyotla.
5. **Gece kullanımı:** LP ve LR deneyleri, S2 rastgele açılırken tekrarlanır. Bu, çok gecelik kestiricinin dayanıklılığını test eder.
6. **Analiz:** Q̂ = ΔV / T_off,üst ile gt_leak_lph karşılaştırılır. Bunun için simülasyonla aynı kod kullanılır.

---

## 6. Malzeme listesi (Türkiye'de bulunabilen ürün türleri)

Fiyat yalnız doğrulanmış bir satıcı linki varsa yazıldı.

| # | Ürün türü | Adet | Not |
|---|---|---|---|
| 1 | 12 V basınç şalterli diyafram hidrofor pompası (karavan/tekne tipi), örn. SEAFLO SFDP1-012-035-21 | 1 | [idefix](https://www.idefix.com/seaflo-hidrofor-pompasi-12v-43-ldk-35-psi-p-21696730): 1.218,80 TL (2026-11-17'de sayfada görülen indirimli fiyat) |
| 2 | Membranlı basınç akümülatörü, 0,75 L (seçenek: 2 L) | 1 | Türkiye'den bir satıcı linki doğrulanmadı |
| 3 | ESP32 geliştirme kartı (DevKit) | 1 | |
| 4 | INA226 akım/gerilim/güç modülü, **R010 (10 mΩ) şönt** | 1 | Şönt değeri alırken kontrol edilmeli |
| 5 | ADS1115 16 bit ADC modülü | 1 | |
| 6 | Analog sıvı basınç sensörü 0,5–4,5 V, G1/4 (tercihen 0–0,5 MPa, yoksa 0–1,6 MPa) | 1 | |
| 7 | HX711 modülü + 5 kg yük hücresi (+ tartı plakası) | 1 | |
| 8 | 12 V normalde kapalı mini solenoid vana | 2 | |
| 9 | Lojik seviyeli N-MOSFET modülü (veya MOSFET + direnç), flyback diyot | 2 | |
| 10 | İğneli vana (1/4") | 1 | |
| 11 | Küresel vana (1/4" veya 3/8") | 1 | |
| 12 | T bağlantı, 3/8" hortum rakoru, 1/2"–G1/4 adaptörler, teflon bant, şeffaf hortum | Takım | |
| 13 | 12 V adaptör (≥ 6 A) veya 12 V akü + 6 A bıçak sigorta ve sigorta yuvası | 1 | |
| 14 | 12 V → 5 V buck dönüştürücü | 1 | |
| 15 | Dirençler (10 kΩ, 20 kΩ, 100 Ω, 100 kΩ), breadboard veya delikli plaket, jumper kablo | Takım | |
| 16 | Kova (giriş), 3–4 L toplama kabı, damlama tepsisi | Takım | |
| 17 | Lastik manometresi (ön dolum ayarı için), bilinen ağırlıklar | 1 | |

---

## 7. Riskler

- **Pompanın kendi basınç şalteri:** Histerezis ve ölü bant Wilo SC2.0 kontrolünden farklı. Düzenek SC (iki noktalı) modunu taklit ediyor, **SCe'nin sıfır debi testini taklit etmiyor.**
- **Kalkış akım darbesi:** Değerini bilmiyoruz. INA226'nın tam skalası 8,19 A, ama darbe bunu aşarsa okuma doyuma girer. 10 Hz örneklemede darbe zaten kaçabilir.
- **Küçük tank:** ΔV ≈ 0,14 L olduğu için büyük kaçaklarda T_off çok kısalıyor. 2 L'lik tank seçeneği bu yüzden tutuluyor.
- **Pompanın iç kaçağı:** Diyafram pompanın çek valfi tamamen sızdırmaz olmayabilir. L0 testi bunu ortaya çıkarır.
- **Sensör doğruluğu:** %0,5–1 FS, Modbus'un 0,1 bar adımıyla aynı mertebede. Mutlak basınca değil, zamanlamaya dayanan yöntemin avantajı burada.
