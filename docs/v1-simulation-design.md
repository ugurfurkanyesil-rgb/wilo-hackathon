# V1 Simülasyon Tasarımı: Hidrofor = Kaçak Sensörü

Durum: tasarım aşamasında, kod yok. Tarih: 2026-11-17.

**İşaretler:**
- **[K]**: kaynaklı.
- **[V]**: varsayım (kaynak yok, gerçek veya düzenekle doğrulanmalı).
- **[T]**: türetilmiş (kaynaklı değerlerden hesaplanmış).

Sinyaller ve register'lar `docs/v1-validation.md` dosyasında doğrulananlarla birebir aynı.

---

## 0. Ana argüman: kaçak neden pompanın debisinden değil, döngü deseninden çıkarılır

1. **Küçük kaçakta pompa çoğu zaman kapalıdır.**
   - SCe düşük debide periyodik bir sıfır debi testi yapar. Debi yoksa pompayı durdurur [K: SC2.0-Booster kılavuzu s.14].
   - Pompa durunca bina, basınç tankındaki suyla beslenir. Basınç açma eşiğine düşene kadar pompa çalışmaz.
   - Gece, kullanım yokken, sadece küçük bir kaçak varsa pompa zamanın büyük kısmında **kapalı** kalır.
2. **Pompa kapalıyken hesaplanmış debi kaçağı göremez.**
   - Pompa duruyorken `flow` değeri modele ve yazılım sürümüne bağlı [K: CIF veri noktası listesi, flow açıklaması].
   - Pompa çalışırken ölçülen şey tankı dolduran pompa debisidir, kaçak debisi değildir.
3. **Hesaplanmış debinin çözünürlüğü de yetmez.**
   - `flow` register'ı 0.1 m³/h adımlarla gelir. Bu **100 L/h** demek [K: CIF listesi].
   - Hedeflediğimiz kaçaklar 2–50 L/h aralığında [V]. Hepsi tek bir çözünürlük adımının altında kalıyor.
   - Wilo da bu değerin kapalı döngü kontrol için kullanılmamasını söylüyor [K].
4. **Kaçak, pompa kapalıyken tanktan su çeker. Bu durma süresini (T_off) kısaltır.**
   - Kullanım olmayan bir döngüde: **Q_kaçak ≈ ΔV_tank / T_off**.
   - ΔV_tank, açma ve kapama basınçları arasında tanktan çekilen su hacmi (Boyle yasasından, §2.1).
   - T_off, pompa "çalışıyor" bitinin 1 s aralıkla okunmasıyla **1 s çözünürlükle** ölçülür.
   - Örnek: ΔV = 5 L [V] ve kaçak 5 L/h ise T_off ≈ 3600 s olur. 1 s çözünürlük bu ölçüm için fazlasıyla yeterli [T].
5. **Büyük kaçakta durum tersine döner.**
   - Kaçak, sıfır debi testinin eşiğinden büyükse test başarısız olur ve pompa gece boyunca **sürekli** çalışır.
   - Bu durumda Seviye 1'de "gece sürekli çalışma", Seviye 2'de `powerInput` ve `flow` sinyalleri kaçağı gösterir.
   - Sıfır debi testinin eşiği fabrikada ayarlanıyor ve yalnız Wilo servisi değiştirebiliyor [K: kılavuz s.14]. Değerini bilmiyoruz, bu yüzden **parametre** olarak tutuluyor [V].

Bu argüman simülasyonda **S-ARG** senaryosuyla gösterilecek (§4).

---

## 1. Kapsam: MVP ve İleri

| | **MVP** (1 günde kodlanır, 22 Kasım ara teslimi) | **İleri** (5 Aralık finali) |
|---|---|---|
| Kontrol | Basitleştirilmiş SC: iki eşikli aç-kapa. SCe: sıfır debi testiyle durma. Tek pompa. | 2–4 pompa, ana pompa değişimi, p-v modu |
| Pompa | Çalışırken sabit nominal debi (SC), ya da çıkışı karşılayan debi (SCe) | **H(Q) eğrisi ve afinite yasaları**, verim eğrisi η(Q) |
| Tank | İzotermal Boyle yasası | Politropik genleşme, ön dolum basıncı kaybı (tank arızası) |
| Kaçak | Boru: orifis, N1 = 0.5. Rezervuar: dönemsel dolum darbeleri. | FAVAD, N1 0.5–1.5. Sürekli akan rezervuar. Çek valf kaçağı. |
| Talep | Poisson olayları, gün içi profil | Yaşlı veya gece vardiyası gibi kullanıcı profilleri, mevsimsellik |
| Modbus | 0.1 bar kuantizasyon, 1 s okuma, kümülatif sayaçlar | Okuma kaçırma ve gecikme, sensör sapması, register taşması |
| Model | Fizik tabanlı kestirici + basit tür sınıflandırıcı | Simülasyonda eğitilen ML modeli, test düzeneğiyle doğrulama, haftalar boyu değişim noktası tespiti |
| Seviye 2 | Basit güç modeli (sabit H ve η) | Pompa eğrisinden güç ve hız |

---

## 2. Fiziksel model (MVP)

### 2.1 Basınç tankı (membranlı)
- Sistemde membranlı bir basınç tankı olduğu varsayılıyor [V]. SiBoost2.0 Smart Helix VE'de tankın standart mı aksesuar mı olduğunu doğrulamadım.
- **Boyle yasası** (izotermal [V]): p_abs · V_gaz = p0_abs · V0
  - V0: tank hacmi.
  - p0: ön dolum basıncı.
  - p_abs = p_gösterge + 1.013 bar.
- Tanktaki su hacmi: **V_w(p) = V0 · (1 − p0_abs / p_abs)**
- Açma (p_on) ve kapama (p_off) basınçları arasında çekilebilen su:
  **ΔV = V0 · p0_abs · (1/p_on_abs − 1/p_off_abs)** [T]
- Kütle dengesi: **dV_w/dt = Q_pompa − Q_talep − Q_kaçak**
- Basınç: **p_abs = p0_abs · V0 / (V0 − V_w)**

### 2.2 Kontrol

**SC (sabit hızlı, iki noktalı kontrol)** [K: kılavuz s.10]
- Basınç p_on'un altına düşünce pompa çalışır.
- Basınç p_off'un üstüne çıkınca ve gecikme süresi dolunca pompa durur.

**SCe (sabit basınç ve sıfır debi testi)** [K: kılavuz s.11–14]
- Pompa basıncı ayar değerinde tutar.
- Tek pompa düşük devirde çalışırken her T_zf saniyede bir sıfır debi testi yapılır.
- MVP'deki karşılığı: Q_çıkış < Q_zf ise test geçer, t_follow süresi sonunda pompa durur [V: Q_zf, T_zf, t_follow].
- Pompa durduktan sonra basınç aktivasyon eşiğine (p_set − Δp_on) düşünce yeniden çalışır.

### 2.3 Pompa (MVP)
- **SC:** Çalışırken Q_pompa = Q_nom [V].
- **SCe:** Çalışırken p = p_set tutulur, yani Q_pompa = Q_talep + Q_kaçak. Bunun tek istisnası, tank yeniden dolarken kısa bir süre Q_nom ile çalışmasıdır [V].
- **Hız:**
  - SC: n = n_nom.
  - SCe: n = n_min + (n_max − n_min) · Q_pompa / Q_max (doğrusal) [V]. Gerçekçi model İleri'de afinite yasalarıyla kurulacak.

### 2.4 Güç (Seviye 2, MVP)
- **P_el = ρ · g · Q_pompa · H / η_top + P_0**
  - H ≈ p / (ρ·g): emme tarafı basıncı ihmal ediliyor [V].
  - η_top sabit [V].
  - P_0: elektronik tüketimi [V].
- Pompa durduğunda P_el = P_bekleme [V].
- Fiziksel ilişki [K]: P_hidrolik = ρ·g·Q·H.

### 2.5 Kaçak modelleri
- **Boru sızıntısı (orifis):** **Q = C_d · A · √(2·p/ρ)**, yani Q ∝ p^0.5.
  - FAVAD genellemesi: Q ∝ p^N1.
  - Rijit kaçaklar için N1 = 0.5, esnek kaçaklar için 1.5 [K: [Autodesk InfoWorks WS Pro, Leakage Modeling](https://help.autodesk.com/cloudhelp/ENU/INFWP-UserGuide/files/GUID-C33F20D8-17A4-4D10-9883-FF8D91DF9D04.htm)].
  - MVP'de N1 = 0.5. İleri'de 0.5–1.5 aralığında rastgele seçilecek.
  - C_d·A, nominal basınçta hedef kaçak debisini (L/h) verecek şekilde kalibre edilir [T].
- **Sızan rezervuar (klozet):**
  - Rezervuardan klozete sürekli q_r debisiyle su sızar.
  - Rezervuardaki seviye V_trig kadar düşünce şamandıralı vana açılır ve t_fill sürede bu hacmi şebekeden çeker [V: V_trig, t_fill].
  - Sonuç: tanka **dönemsel talep darbeleri** gelir. Periyot V_trig / q_r, ortalama debi q_r.
  - Bu darbeler, kaçak türünü ayırt etmek için kullanılacak hipotez sinyali [V].

### 2.6 Bina talebi
- Daire sayısı N_d [V] ve daire başına kişi sayısı [V].
- **Kişi başı kullanım: 146 L/gün** [K, ikincil kaynak]. Su Yönetimi Genel Müdürlüğü'nün 2021 verisinde kentlerde kayıplar hariç değer ([Ekonomi Gazetesi, 26.03.2026](https://www.ekonomigazetesi.com/surdurulebilir-ekonomi/su-karnesinin-en-buyuk-kirigi-su-kaybi-75544)).
- **Olay türleri:** musluk, sifon (rezervuar dolumu), duş. Her biri için debi ve süre dağılımı [V].
- **Saatlik olay oranı:** λ(t), sabah ve akşam tepeli bir profil [V]. Gece 02:00–05:00 arasında λ küçük ama sıfır değil [V].

---

## 3. Modbus çıktısı emülasyonu

Simülasyon ideal değerleri değil, **gerçek Modbus okumasına benzeyen** veriyi üretir.

| Adım | Kural | Kaynak |
|---|---|---|
| İç zaman adımı | dt_sim = 0.1 s | [V] |
| Okuma aralığı | **Δt_poll = 1 s** (parametre) | [V] |
| Basınç | Gerçek p + sensör gürültüsü (σ parametre), sonra **0.1 bar'a kuantize** | Çözünürlük [K: register 40026], gürültü [V] |
| Çalışıyor biti | Okuma anında pompa durumu (0/1) | [K: 40033 bit 3] |
| Kalkış sayaçları | **Kümülatif** UINT32. Her kalkışta +1 (sistem ve pompa başına). | [K: 40077, 40081] |
| Çalışma saati | **Kümülatif**, floor(toplam çalışma süresi / 3600 s) | [K: 40097, 1 h çözünürlük] |
| powerInput | Tam sayı W | [K: CIF input reg. 4] |
| speed | Tam sayı 1/dk | [K: CIF input reg. 7] |
| flow (hesaplanmış) | Q_pompa'nın 0.1 m³/h'e kuantize hali. Pompa dururken 0. | Çözünürlük [K], duruşta 0 [V] |

### CSV şeması (test düzeneğiyle ortak)

| Sütun | Tip | Seviye | Açıklama |
|---|---|---|---|
| `timestamp` | ISO 8601 | 1 | Okuma zamanı |
| `pressure_bar` | float, 0.1 adım | 1 | Sistem basıncı |
| `pump1_running` | 0/1 | 1 | Çalışıyor biti |
| `system_starts_total` | int | 1 | Sistem kalkış sayacı |
| `pump1_starts_total` | int | 1 | Pompa 1 kalkış sayacı |
| `pump1_hours_total` | int | 1 | Pompa 1 çalışma saati |
| `power_w` | int | 2 | Elektrik gücü |
| `speed_rpm` | int | 2 | Hız |
| `flow_calc_m3h` | float, 0.1 adım | 2 | Hesaplanmış debi |
| `gt_leak_lph` | float | yalnız simülasyon | Gerçek kaçak debisi (etiket) |
| `gt_leak_type` | none / reservoir / pipe | yalnız simülasyon | Kaçak türü (etiket) |
| `gt_demand_lph` | float | yalnız simülasyon | Gerçek talep (etiket) |

`gt_` ile başlayan sütunlar yalnız simülasyonda var, gerçek veride ve modele girdi olarak kullanılmaz.

**Test düzeneğiyle eşleştirme notu:**
- Düzenekte akım sensörü kullanılacak.
  - **INA219** gerilimi ve akımı birlikte ölçer, bu yüzden **P = V · I** ile doğrudan `power_w` hesaplanır.
  - **ACS712** yalnız akımı ölçer. Bu durumda P ≈ V_nom · I yaklaşımı kullanılır ve "yaklaşık" diye işaretlenir.
- Düzenekteki küçük DC pompanın hız bilgisi yoksa `speed_rpm` boş bırakılır.
- `flow_calc_m3h` için düzenekte bir debimetre varsa onun değeri 0.1 m³/h'e kuantize edilerek yazılır, yoksa boş kalır.

---

## 4. Senaryolar

| Kod | Kaçak | Kaçak debileri [V] | Amaç |
|---|---|---|---|
| L0 | Yok | 0 | Yanlış alarm oranını ölçmek |
| LR | Sızan rezervuar | 2, 5, 10, 20 L/h | Dönemsel dolum darbeleri |
| LP | Boru sızıntısı (orifis) | 2, 5, 10, 20, 50 L/h (nominal basınçta) | Sürekli, basınca bağlı kaçak |
| **S-ARG** | Boru, 5 L/h | 5 L/h | §0'daki argümanı göstermek |

**S-ARG çıktıları:** L0 ile LP-5 aynı gece (02:00–05:00) penceresinde karşılaştırılır.
1. Pompanın çalıştığı zaman oranı. Beklenti: ikisinde de düşük.
2. Gece boyunca `flow_calc_m3h` ortalaması ile gerçek kaçak debisi. Beklenti: hesaplanmış debi ya sıfır ya da pompanın dolum debisi; ikisi de kaçağı göstermez.
3. T_off dağılımı. Beklenti: L0'da uzun ya da tek bir duruş, LP-5'te ~ΔV/Q aralıklarla tekrarlayan döngüler.
4. Q̂ = ΔV / medyan(T_off) ile tahmin edilen debi ve gerçek debi.

Her senaryo için **SC ve SCe modları** ayrı ayrı koşulur. Simülasyon süresi 14 gün ve birden fazla rastgele tohum ile çalıştırılır [V]. Bina parametreleri her koşuda belirli aralıklardan rastgele seçilir [V].

### MVP için başlangıç parametreleri (hepsi [V], düzenek ya da gerçek veriyle güncellenecek)

| Parametre | Değer |
|---|---|
| V0 (tank hacmi) | 24 / 50 / 100 L |
| p0 (ön dolum basıncı) | p_on − 0.2 bar |
| SC eşikleri | p_on = 3.0 bar, p_off = 4.0 bar |
| SCe | p_set = 4.0 bar, Δp_on = 0.5 bar |
| Sıfır debi testi | Q_zf = 30 L/h, T_zf = 60 s, t_follow = 30 s |
| Q_nom | 2 m³/h |
| η_top | 0.45 |
| P_bekleme | 5 W |
| Bina | N_d = 12, 3 kişi/daire |
| Rezervuar | V_trig = 0.5 L, t_fill = 10 s |
| Sensör gürültüsü | σ_p = 0.02 bar |

---

## 5. Model: girdi, çıktı, yöntem

**Girdi:** Bir gecelik pencere (varsayılan 01:00–05:00 [V]).
- Seviye 1: `pressure_bar`, `pump1_running`, sayaçlar.
- Seviye 2: Seviye 1'e ek olarak `power_w`, `speed_rpm`, `flow_calc_m3h`.

**Ara özellikler:**
- Döngü listesi: her döngü için T_on, T_off, kalkış ve duruştaki basınç.
- Kullanım içermeyen döngülerin ayrılması: düzensiz kısa T_off'lar ve basınç sıçramaları elenir.
- Seviye 2'de ayrıca: pompa çalışırken ortalama güç ve gece boyunca sürekli çalışma bayrağı.

**Çıktı:**

| Çıktı | Tanım |
|---|---|
| `leak_lph` | Kaçak debisi tahmini (L/h) |
| `leak_type` | none / reservoir / pipe |
| `cost_tl_month` | Aylık maliyet tahmini (TL/ay) |
| `confidence` | Güven skoru (temiz döngü sayısına ve dağılımına göre) |

**MVP yöntemi:**
1. **Fizik tabanlı kestirici, çok gecelik:**
   - Gece meşru kullanım (sifon, musluk) bir T_off'u **kısaltır**, hiçbir zaman uzatmaz. Bu yüzden tek bir gecenin medyanı kaçağı olduğundan büyük gösterebilir.
   - Kestirim **son K gecenin** (varsayılan K = 7 [V]) temiz döngülerinden yapılır:
     - **Ana kestirici:** T_off dağılımının üst yüzdeliği (ör. 90. yüzdelik [V]) ya da en uzun m döngünün ortalaması [V]. **Q̂ = ΔV / T_off,üst**
     - **Dağılım kontrolü:** Kaçak varsa T_off değerleri ΔV/Q etrafında dar bir tepe oluşturur. Kullanım olayları bu tepenin solunda dağınık bir kuyruk yaratır. Tepe konumu ve genişliği güven skoruna girer.
   - ΔV, kurulum parametrelerinden (V0, p0, eşikler) hesaplanır. Bu parametreler bilinmiyorsa, kaçak olmayan bir gecenin döngülerinden kalibre edilir [V].
   - S-ARG'a ek bir kontrol: tek gecelik medyan ile K gecelik üst yüzdelik kestiricilerinin hataları, gece kullanım oranı artırılarak karşılaştırılır.
2. **Tür sınıflandırıcı (kural tabanlı):**
   - Rezervuar kaçağı: T_off dizisinde düzenli bir periyot ve kısa basınç düşüş darbeleri.
   - Boru kaçağı: düzgün ve tekrarlı T_off.
   - Kaçak yok: döngü yok ya da T_off > eşik.
3. **Büyük kaçak modu:** Gece boyunca sürekli çalışma varsa, Seviye 2'de kaçak debisi `flow_calc` ve güç üzerinden tahmin edilir. Seviye 1'de yalnız "büyük kaçak" bayrağı verilir.

**İleri:** Simülasyonda üretilen veriyle gradient boosting ve döngü dizisi üzerinde bir sekans modeli eğitilir. Domain randomization uygulanır, test düzeneğinde doğrulama yapılır. Haftalar boyunca değişim noktası tespiti eklenir.

---

## 6. Başarı metrikleri

| Metrik | Tanım |
|---|---|
| **Tespit edilebilen en küçük kaçak** | Ayda en fazla 1 yanlış alarm (L0'da) koşulunda, %90 tespit oranına ulaşılan en küçük kaçak debisi (L/h) |
| **Debi tahmin hatası** | `leak_lph` için MAE (L/h) ve MAPE. LR ve LP için ayrı ayrı. |
| **Tür sınıflandırma** | 3 sınıf için macro-F1 ve karışıklık matrisi |
| **Tespit gecikmesi** | Kaçak başladıktan sonra ilk doğru alarma kadar geçen gece sayısı |
| **Seviye 2 katkısı** | Seviye 1 ile Seviye 1+2 arasındaki MAE farkı |
| **S-ARG** | `flow_calc` tabanlı ve T_off tabanlı tahminlerin hatası, yan yana |

Metrikler simülasyonda, farklı bina parametreleri ve rastgele tohumlarla ayrılmış test kümesinde ölçülür. Hedef sayı yok, önce bir baseline ölçülecek.

---

## 7. Maliyet (TL/ay)

**cost_tl_month = leak_lph × 24 × 30 / 1000 × (su_birim + atıksu_birim)**

- **Varsayılan birim fiyatlar:** İSKİ konut tarifesi, Ocak 2026. Su **35,26 TL/m³**, atıksu **17,62 TL/m³**.
  - Kaynak: [İSKİ açıklaması, Cumhuriyet, 12.05.2026](https://www.cumhuriyet.com.tr/turkiye/iski-den-su-elektrikten-pahali-iddialarina-yanit-2503278).
  - İSKİ'nin fatura örneğinde atıksu bedeli de m³ başına hesaplanıyor [K].
- Fiyatlar zamanla değişebilir, bu yüzden **parametre** olarak tutulur. KDV ve diğer vergiler hariç.
- Fiyatlar 2026'nın ilk ayından kalma. Demo öncesinde güncel tarife iski.gov.tr'den kontrol edilmeli.
- İnsani su hakkı indirimi gibi kademeli indirimler kaçak hesabına dahil edilmedi [V].
- **Örnek** [T]: 5 L/h kaçak → 3,6 m³/ay → 3,6 × 52,88 = **≈190 TL/ay**.

---

## 8. Notlar ve riskler

- **Sunumda karıştırılmaması gereken iki metrik:**
  - Bakanlığın **%33,54**'ü **su kaybı** oranı ([Tarım ve Orman Bakanlığı SYGM, 04.12.2022](https://tarimorman.gov.tr/SYGM/Haber/1076/Bugun-Dunya-Su-Kayiplari-Gunu)).
  - **%46**, TÜİK'e atıfla verilen **faturalanamayan su** oranı. TÜİK bülteninden doğrulanamadı.
  - Faturalanamayan su, faturalanmayan ama izinli kullanımları da içerir. İkisi farklı metrikler.
  - Ayrıca V1, sayaçtan **sonraki** bina içi kaçağı hedefliyor. Bu kaçak abonenin faturasına yansır, şebeke kaybı istatistiğine girmez.
- **Karıştırıcı etkenler (İleri'de modellenecek):**
  - Tank ön dolum basıncının kaybı: ΔV küçülür ve döngüler kısalır, kaçağa benzer bir görüntü oluşur.
  - Çek valf kaçağı: tanktaki su pompa üzerinden geri kaçar.
  - Meşru gece kullanımı.
  - Sıcaklığa bağlı genleşme.
- **SCe'nin gerçek davranışı:** Sıfır debi testinin parametreleri bilinmiyor. MVP'deki SCe modeli bir yaklaşım; gerçek ünite verisi olmadan doğrulanamaz.
- **Tank:** SiBoost2.0 Smart Helix VE'de basınç tankının standart olup olmadığı doğrulanmadı. Tank yoksa ya da çok küçükse T_off çok kısalır ve yöntemin hassasiyeti değişir.
