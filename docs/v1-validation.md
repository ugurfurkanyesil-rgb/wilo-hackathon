# V1 Doğrulama: Hidrofor = Kaçak Sensörü

Tarih: 2026-11-17.
- Wilo ve rakip ürün kılavuzları resmi sitelerden PDF olarak indirildi ve metinleri tek tek okundu.
- Okunamayan ya da açılamayan kaynaklar "doğrulanamadı" olarak işaretli.

## Özet

| Soru | Sonuç |
|---|---|
| a) SiBoost dışarıya veri veriyor mu? | **Evet, Modbus TCP standart.** Kontrol ünitesinden okunabilenler: basınç, pompa çalışıyor biti, kalkış sayaçları ve çalışma saati. **Akım okunamıyor.** Pompa başına haberleşme modülüyle (CIF) **elektrik gücü (W) ve hız (1/dk)** okunabiliyor. |
| a-ek) Akım yerine güç veya frekans kullanılabilir mi? | **Evet.** Helix2.0-VE'de akım verisi yok, ama `powerInput` (W) ve `speed` (1/dk) var. V1 için güç, akımdan daha doğrudan bir sinyal. |
| b) Rakipler ne yapıyor? | Grundfos SCALA2 ve DAB Esybox **evet/hayır şeklinde bir kaçak alarmı** veriyor ve pompayı durduruyor. Phyn Plus **ek bir cihazla** kaçak çapını tahmin ediyor. **Wilo'nun kendi sayfasında "leakage detection" (kaçak algılama) geçiyor**, yöntemi belli değil (bkz. risk). |
| c) %46 doğrulandı mı? | **TÜİK bülteninin kendisine ulaşılamadı.** Resmi alternatif: Tarım ve Orman Bakanlığı'na göre ortalama su kaybı oranı **%33,54**. |

---

## a) SiBoost Smart Helix VE'nin dışarıya verdiği veriler

### Hangi kontrol ünitesi?
- Güncel model **Wilo-SiBoost2.0 Smart Helix VE** ve kontrol ünitesi **Smart Controller SCe2.0** ([ürün sayfası](https://wilo.com/il/en/Products/en/products/siboost2-0-smart-helix-ve_id495)).
- SCe varyantının nasıl çalıştığı **Wilo-Control SC2.0-Booster** kurulum ve kullanım kılavuzunda anlatılıyor ([PDF, Ed.01/2023-09](https://cms.media.wilo.com/dcidocpfinder/wilo629451/7984526/wilo629451.pdf)). Kılavuzun 5.2 bölümünde SC ve SCe ayrı ayrı anlatılıyor. Modbus register 40003'teki "Control device type" listesinde de "SCe" seçeneği var.
- Daha önce `idea-pool`'da linklediğimiz eski "SiBoost Smart Helix VE" sayfası "SCe" kontrol ünitesinden söz ediyor. Eski nesil kontrol ünitesinin Modbus tablosunu **doğrulayamadım**.

### Kontrol ünitesi seviyesi (SC2.0 / SCe2.0)
Kaynak: SC2.0-Booster kılavuzu.
- **Haberleşme:** Kılavuzda şöyle yazıyor: *"The control device is prepared for connection via ModBus TCP as standard"* (s.17).
  - Modbus RTU, BACnet MS/TP ve BACnet IP için ek haberleşme modülleri var (s.18).
  - Ayrıca SBM (toplu çalışma) ve SSM (toplu arıza) kuru kontak çıkışları var.
- **Okunabilen veriler** (Modbus parametre tablosu, s.55–59):

| Register | Veri | Birim/çözünürlük | V1 için anlamı |
|---|---|---|---|
| 40026 | Actual value (sistem basıncı) | 0.1 bar | Basınç düşüş hızı. Çözünürlük kaba, simülasyonda test edilmeli. |
| 40033–40036 | Pump status 1–4, bit 3 = Running | Bit | Bu bit sık aralıklarla okunursa **kalkış ve duruş zamanları** çıkarılabilir. |
| 40077–40078 | Number of switching-on procedures of the system | Sayaç | Gece kalkış sayısı (iki okuma arasındaki fark). |
| 40081–40088 | Total switching cycles of pump 1–4 | Sayaç | Pompa başına kalkış sayısı. |
| 40097–40104 | Total operating hours of pump 1–4 | 1 h | Gece analizi için **çok kaba**. |
| 40139–40140 | Fault status | Bitmap | Arıza ve kuru çalışma gibi durumları kaçak sinyalinden ayırmak için. |

- **Bu tabloda akım, güç veya frekans register'ı yok.** Kontrol ünitesinin ekranındaki "Pump data set" menüsünde pompaların bazı tanı verileri gösteriliyor (s.44), ama bu verilerin Modbus ile okunabildiğine dair bir bilgi yok.

### Pompa seviyesi (CIF modülü takılı Helix2.0-VE)
Kaynak: [Wilo Modbus veri noktası listesi](https://cms.media.wilo.com/cdndoc/wilo194406/11516106/wilo194406.html). [Wilo Modbus sayfası](https://wilo.com/gb/en/Digital-Energy/Building-automation/Data-points-and-data-point-list/Modbus/), CIF Modbus RTU (2190368) ve CIF Ethernet Multiprotocol (2211408) modülleri için **SiBoost2.0 Smart 1** ve **Helix2.0-VE**'yi uyumlu ürün olarak listeliyor.

| Input register | Veri | Birim | Helix2.0-VE desteği |
|---|---|---|---|
| 1 | pressure | cm H₂O (×10) | ✅ |
| 2 | flow (**hesaplanmış**) | 0.1 m³/h | ✅ Not: Liste, bu değerin kapalı döngü kontrol için kullanılmamasını söylüyor. |
| 3 | energyConsumption | 1 kWh | ✅ Gece analizi için çok kaba. |
| 4 | **powerInput** | **1 W** | ✅ |
| 6 | electricalCurrent | 0.1 A | ❌ Yalnız Stratos, ChronoLine IL-E, Stratos GIGA ≤7.5 kW ve VeroLine IP-E'de var. |
| 7 | **speed** | **1/dk** | ✅ |

**a-ek sorusunun cevabı:** Akım yerine **elektrik gücü (W)** kullanılabilir.
- Güç, hidrolik yükü akımdan daha doğrudan yansıtır: P_el = ρ·g·Q·H / η.
- Frekans (Hz) doğrudan verilmiyor, onun yerine **hız (1/dk)** veriliyor. Hızın frekansla orantılı olduğunu varsayıyorum (motor kayması ihmal edilirse). Helix2.0-VE'nin motor tipini doğrulamadım.
- Hesaplanmış debi de var, ama Wilo bu değerin düşük debilerde ne kadar doğru olduğunu garanti etmiyor. Gece kaçağı tam da bu düşük debi bölgesinde olduğu için bu değere güvenmiyoruz.

**Eski Helix VE (IF-Modbus modülü):** [IF-Modbus veri noktası listesine](https://cms.media.wilo.com/cdndoc/wilo181065/3657434/wilo181065.html) göre `power input` (W) ve `speed` (1/dk) "MVIE, …" ailesinde destekleniyor. `Electrical Current` ise "MVIE, … (0.55…7.5 kW)" için listelenmiş. Listenin başında "MVIE/MVISE/MHIE/HELIX VE" aynı satırda geçiyor, ama Helix VE'nin bu satıra dahil olduğu kesin değil.

### Bulut ve uzaktan izleme
- Ürün sayfasında *"Optional Wilo-Gateway for remote monitoring"* yazıyor ([ürün sayfası](https://wilo.com/il/en/Products/en/products/siboost2-0-smart-helix-ve_id495)).
- Wilo-Smart Gateway'in SiBoost ile nasıl bağlandığını (Wilo Net mi, Modbus mu) ve hangi verileri buluta gönderdiğini **doğrulayamadım**. Gateway kılavuzunu ([PDF](https://cms.media.wilo.com/dcidocpfinder/wilo456456/5643043/wilo456456.pdf)) açıp okumadım.

### V1 simülasyonunu etkileyen bulgu: SCe'nin sıfır debi testi
Kılavuz (s.14), sıfır debi testini şöyle anlatıyor:

> *"When operating only one pump in the lower frequency range and with constant pressure, a zero-flow test is carried out cyclically. This briefly increases the setpoint … If the pressure does not drop again … there is a zero-flow and the base-load pump is switched off."*

Bu şu anlama geliyor:
- Frekans konvertörlü SCe sistemi gece de bir aç-kapa döngüsüne giriyor.
- Kaçak yoksa sıfır debi testi başarılı olur, pompa durur ve basınç yavaş düşer.
- Kaçak varsa basınç daha hızlı düşer, böylece **duruş aralıkları kısalır ve kalkış sayısı artar**.
- Yani sabit hızlı (SC) ve frekans konvertörlü (SCe) sistemlerin ikisinde de **kalkış/duruş zamanları kaçağı yansıtan ana sinyal** olabilir. Bunun doğru olup olmadığı simülasyonda test edilecek.

### Sonuç (a)
- **"Ek donanım yok" iddiası kısmen doğru.**
  - Modbus TCP standart olarak geldiği için kalkış/duruş zamanları ve basınç **ek donanım olmadan** okunabiliyor. Gereken tek şey, Modbus'ı sık aralıklarla okuyacak küçük bir istemci.
  - Güç ve hız okumak için **pompa başına CIF modülü** gerekiyor. Bu Wilo'nun kendi aksesuarı, ama yine de bir donanım ekleme sayılır.
- **Demoda bunun karşılığı:** Model iki girdi seviyesiyle tasarlanmalı.
  - **Seviye 1:** Yalnız kontrol ünitesi verisi (kalkış/duruş + basınç).
  - **Seviye 2:** Seviye 1'e ek olarak pompa gücü.
  - Demoda Seviye 2'nin doğruluğa ne kadar katkı yaptığı gösterilir.

---

## b) Rakip ve benzer ürünlerin kaçak özellikleri

| Ürün | Ne yapıyor | Çıktı | Ek donanım | Kaynak |
|---|---|---|---|---|
| **Grundfos SCALA2** (ev tipi booster) | "Anti cycling" özelliği fabrikada **kapalı** geliyor. Kapalıyken pompa sabit bir desende 40 kez kalkarsa alarm verir ama çalışmaya devam eder. Açıkken sabit desenli kalkış/duruşta *"there is a leakage in the system"* der, **pompayı durdurur** ve "alarm 3" verir. | Evet/hayır alarm | Yok | [SCALA2 kurulum ve kullanım kılavuzu, 10.3.4](https://api.grundfos.com/literature/Grundfosliterature-5769057.pdf) |
| **DAB Esybox Pop** (ev tipi booster) | Kılavuza göre *"The pump's electronic control is able to detect the presence of a leak based on its frequency."* Basic modda pompayı durdurup elle sıfırlanmayı bekler. Smart modda yeniden kalkış basıncı farkını (RP) değiştirerek kaçağın etkisini azaltır. Varsayılan mod: Smart. | Evet/hayır alarm, pompa durumu | Yok | [Esybox Pop kılavuzu, 7.2.3.10 ve 7.3.1](https://www.dabpumps.com/sites/default/files/document/esybox_pop_dab_instruction_manual_web_version_multi_60231842.pdf) |
| **Phyn Plus** (akıllı kesme vanası) | Ana hatta takılıyor. "Plumbing Check" sırasında suyu kapatıp basınç düşüşünü (dP, psi) ölçüyor ve **tahmini kaçak çapını** (dD, inç) hesaplıyor. Alarm eşikleri dP ve dD'ye bağlı. Kaçak debisi veya maliyet çıktısı makalede yok. | dP, dD, alarm | **Var** (vana ve sensör) | [Phyn yardım merkezi](https://helpcenter.phyn.com/help/what-are-the-plumbing-check-thresholds-to-get-a-plumbing-check-alert) |
| **Wilo-SiBoost2.0 Smart Helix VE** | Ürün sayfasında: *"The optional interface to the SCADA connection also enables monitoring and leakage detection."* Yöntemi, çıktısı ve bunu kimin yaptığı (Wilo mu, SCADA tarafı mı) belli değil. **Doğrulanamadı.** | Bilinmiyor | SCADA bağlantısı | [Ürün sayfası](https://wilo.com/il/en/Products/en/products/siboost2-0-smart-helix-ve_id495) |

### V1'in farkları, madde madde

| Özellik | SCALA2 | Esybox | Phyn Plus | **V1** |
|---|---|---|---|---|
| Kaçak var/yok | ✅ | ✅ | ✅ | ✅ |
| **Kaçak debisi (L/saat)** | ❌ | ❌ | ❌ (çap veriyor, debi değil) | ✅ Hedef |
| **Maliyet (TL/ay)** | ❌ | ❌ | ❌ | ✅ (debi × su tarifesi; tarife kullanıcıdan alınacak) |
| **Kaçak türü** (sızan rezervuar / boru) | ❌ | ❌ | ❌ | ✅ Hedef (hipotez: rezervuar kaçağı dönemsel bir dolum deseni, boru kaçağı sabit bir taban debi bırakır) |
| Pompayı durdurmadan izleme | Ayara bağlı | Smart modda evet | Test sırasında suyu kesiyor | ✅ Pasif izleme |
| Çok daireli bina ve basınçlandırma ünitesi | ❌ (ev tipi) | ❌ (ev tipi) | ❌ (tek hat) | ✅ |
| Ek donanım | Yok | Yok | Var | Yok (Seviye 1) / CIF modülü (Seviye 2) |
| Zaman içindeki eğilim ve yöneticiye rapor | ❌ | ❌ | Uygulamada var | ✅ |

### Özgünlük için risk
- Kaçağın kalkış/duruş deseninden algılanması **yeni bir fikir değil**: hem Grundfos hem DAB bunu ürünlerinde yapıyor.
- Wilo da kendi ürün sayfasında "leakage detection" diyor.
- V1'in özgünlüğü üç noktada:
  1. Kaçak debisini ve maliyetini sayısal olarak tahmin etmesi.
  2. Kaçak türünü ayırt etmesi.
  3. Çok pompalı bina ünitesinde pasif çalışması.
- **Öneri:** Sunumda "kaçak algılama" değil, **"kaçağın debisi, maliyeti ve türü"** öne çıkarılmalı.
- **Öneri:** Wilo'nun SCADA tarafındaki "leakage detection" özelliğinin ne olduğu bootcamp'te mentora sorulmalı.

---

## c) %46 faturalanamayan su oranı

- **TÜİK bülteni:** `data.tuik.gov.tr` adresi `veriportali.tuik.gov.tr`'ye yönleniyor. Bu portal otomatik erişime 403 döndürüyor ya da boş sayfa veriyor. **Bülteni açıp doğrulayamadım.**
- Bültenin içeriğini aktaran [alomaliye.com sayfasında](https://www.alomaliye.com/2025/12/09/su-ve-atiksu-istatistikleri-2024/) kayıp veya faturalanamayan su oranı **geçmiyor**.
- %46 rakamı şu an yalnız [İstiklal köşe yazısında](https://www.istiklal.com.tr/yazarlar/kentsel-su-sisteminde-kayip-ve-kacaklari-1063570h) var.
- **Resmi alternatif:** [Tarım ve Orman Bakanlığı Su Yönetimi Genel Müdürlüğü, 04.12.2022](https://tarimorman.gov.tr/SYGM/Haber/1076/Bugun-Dunya-Su-Kayiplari-Gunu): *"Ülkemizde hâlihazırda su kaybı oranı ortalaması %33,54 seviyesinde"*. Aynı sayfada 2040 hedefi %10.
- **Yasal hedef:** Büyükşehir ve il belediyeleri için 2023'e kadar en fazla %30, 2028'e kadar en fazla %25 ([Genelge 2021/47](https://www.tarimorman.gov.tr/Duyuru/1461/Icme-Suyu-Sistemlerinde-Su-Kayiplarinin-Azaltilmasina-Yonelik-Is-Termin-Plani-Genelgesi-Yururluge-Girmistir)).
- **Kavram farkı:**
  - %33,54 **su kaybı** oranı.
  - %46 **faturalanamayan su** oranı. Bu oran, faturalanmayan ama izinli kullanımları da (ör. itfaiye, park sulama) içerir. İkisi doğrudan karşılaştırılamaz.
  - Ekonomi Gazetesi'ndeki bir yazı, Su Yönetimi Genel Müdürlüğü verisine dayanarak 2021 için fiziki kaybı %24,09, idari kaybı %9,45, faturalanamayan suyu %38,67 olarak veriyor ([26.03.2026](https://www.ekonomigazetesi.com/surdurulebilir-ekonomi/su-karnesinin-en-buyuk-kirigi-su-kaybi-75544)). Bu ikincil bir kaynak.
- **Sunum için öneri:** Resmi rakam olarak **%33,54** (Bakanlık) ve **2028 hedefi %25** kullanılmalı. %46'yı kullanmak istersen TÜİK bültenini tarayıcıda açıp ilgili tabloyu doğrulaman gerekiyor.
- Not: V1, belediyenin **sayacından sonraki** bina içi kaçakları hedefliyor. Bu kaçaklar abonenin faturasına yansıdığı için şebeke kaybı istatistiğine girmez. Ulusal kayıp oranı sunumda yalnızca genel bağlam olarak kullanılmalı.
