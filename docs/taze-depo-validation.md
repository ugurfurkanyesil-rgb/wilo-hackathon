# Taze Depo Doğrulama

Tarih: 2026-11-19.
- Her iddianın yanında kaynak linki var. PDF'ler indirilip metinleri okundu.
- Açılamayan kaynaklar **"doğrulanamadı"**, yalnız arama motoru özetinde görülenler **"kısmen doğrulandı"** diye işaretli.
- "Yorum:" diye başlayan cümleler benim çıkarımım, kaynak değil.

## Özet

| Soru | Sonuç |
|---|---|
| a) Problem kanıtı var mı? | **Güçlü.** Türkiye'de 3 saha çalışması (Diyarbakır, Adana ×2) ve Tayvan'da 178 binalık bir çalışma, depoda bekleyen suyun bozulduğunu gösteriyor. Tayvan çalışması ikilemi aynen yazıyor: depolar kesinti korkusuyla gereğinden büyük yapılıyor ve klor hızla düşüyor. 2025-26'da İzmir ve Ankara'da kesintiler resmî kaynaklarla doğrulandı. |
| a) Konut deposu temizliği için bir mevzuat var mı? | **Bulamadım.** Bağlayıcı tek hüküm Lejyoner Yönetmeliği'nde (soğuk su deposu yılda en az 2 kez temizlenir). O da yalnız hastane, otel ve AVM gibi yerleri kapsıyor, **konutları kapsamıyor**. |
| b) Benzer ürün var mı? | **Kısmen.** Keraflo Tanktronic (İngiltere) depo seviyesini elektronik olarak ve takvime göre ayarlıyor. Tüketim tahmini, kesinti riski ve su yaşı hesabı yapmıyor. Wilo break tank yalnız şamandıra şalteri ve seviye göstergesiyle geliyor. Grundfos'ta benzer bir özellik bulamadım. |
| c) Teknik olarak yapılabilir mi? | **Evet, ama ek donanım gerekiyor:** seviye sensörü ve motorlu vana. Tüketim, seviye sensörü ile hidrofor verisinden birlikte çıkarılabilir. Su yaşının fiziği basit (yaklaşık τ ≈ V/Q), ama depodaki karışımın nasıl olduğu belirsiz. |
| d) Yapay zekanın katkısı ne? | **Orta.** Tüketim tahmini, binanın kesinti desenini kendi kendine öğrenmesi ve seviye optimizasyonu, sabit bir zamanlayıcıdan iyi. Ama basit bir kural faydanın önemli kısmını alabilir. Bu, jüride risk. |

---

## a) Problem kanıtları

### Depo suyunun kalitesi

| Çalışma | Yer, örneklem | Bulgu | Durum |
|---|---|---|---|
| Çalık O. (danışman Ali Ceylan), tıpta uzmanlık tezi ([YÖK Açık Bilim](https://acikbilim.yok.gov.tr/handle/20.500.12812/292765), [tezara](https://tezara.org/theses/164560)) | Diyarbakır kent merkezi, 200 konut; hem depo girişinden hem depo çıkışından örnek | Özette: *"Koliform bakteri, depo girişi şebeke su örneklerinin %35'inde, depo çıkışı su örneklerinin %52.0'inde saptanmıştır."* Depo çıkışındaki koliform *"deponun hacmine, kilitli tutulmasına, yapıldığı malzemeye, yaşına ve su giriş sıklığına bağlı olarak anlamlı düzeyde"* değişiyor. | **Kısmen doğrulandı.** YÖK sitesine DNS hatası nedeniyle bağlanılamadı, tezara 403 verdi. Alıntılar arama motorunun gösterdiği özet metninden. Tezin yılını bilmiyorum. |
| Aydın R., Atakav Y., [Ç.Ü. Müh.-Mim. Fak. Dergisi 33(1), 2018](https://dergipark.org.tr/en/pub/cukurovaummfd/article/420689) | Adana Seyhan, 53 apartman, 159 örnek (depo girişi, depo çıkışı, 1. kat) | *"bakiye klor sadece 4 apartmanın su deposunda ölçülebilmiştir"*. Depo çıkışında %5 total koliform. | Doğrulandı (makale sayfası). Türkçe ve İngilizce özetlerdeki giriş oranları birbirini tutmuyor. |
| Wang G.S., Chen H.W., [Water Sci. & Tech.: Water Supply 6(2), 2006, doi:10.2166/ws.2006.046](https://scholars.lib.ntu.edu.tw/bitstreams/4124c91a-0ae4-4e85-a99b-c3e495b9155e/download) | Tayvan'da 3 şehir, 178 bina, 323 örnek | *"In order to prevent a water supply shortage, the roof-top storage tanks are built much larger than necessary in most of the cases. The chlorine residual decreases rapidly in the storage tanks due to the long retention time"*. Mikrobiyal yeniden üremenin çoğu, klorun 0,2 mg/L'nin altında olduğu örneklerde görülmüş. | Doğrulandı (PDF okundu). |
| [EPA Distribution System Toolbox, Water Age, EPA 815-F-22-002, 2022](https://www.epa.gov/system/files/documents/2022-04/ds-toolbox-fact-sheets_water-age-mgt_final-508_revised.pdf) | Kılavuz | *"Excessive water age can lead to … increased disinfection byproduct (DBP) formation, disinfectant residual consumption, and microbial growth."* Su yaşının, kullanım düşükken veya depo gereğinden büyükken arttığını söylüyor. | Doğrulandı (PDF okundu). |

**Diyarbakır rakamlarının doğru okunması (sunum için önemli):**
- %35, depoya **giren şebeke suyu** için. Yani suyun bir kısmı depoya zaten kirli geliyor.
- Depo bu oranı %52'ye çıkarıyor, yani artış 17 puan.
- Yorum: Taze Depo yalnız depodan kaynaklanan kısmı azaltabilir, şebekeden gelen kirliliği çözemez. Sunumda "depo suyu bozuyor" yerine **"depo, gelen suyu daha da kötüleştiriyor ve suyun depoya giriş sıklığı bunu anlamlı biçimde etkiliyor"** demek daha doğru.

### Depoyu kim temizliyor?
- **Adana anketi** ([Aydın, Atakav, Ceylan, Ç.Ü. Müh.-Mim. Fak. Dergisi 31(ÖS 2), 2016](https://dergipark.org.tr/en/download/article-file/307763)). Depo kullanan 528 kişiyle yapıldı.
  - Katılımcıların **%55,1'i kapıcı**, %58,9'u ilkokul mezunu.
  - %42,6'sı deponun ne sıklıkla temizlenmesi gerektiğini bilmiyor.
  - Depoların yalnız **%22,5'i önerilen sıklıkta** temizleniyor.
  - Bu, "depoları çoğunlukla eğitimsiz kapıcılar temizliyor" iddianı destekleyen en iyi kaynak.
- **"%59 eğitimsiz" rakamı apartman için kullanılmamalı.** [Çamur, İlter, Topbaş, Turk J Public Health 16(1), 2018](https://dergipark.org.tr/en/download/article-file/532282): *"Depo temizliği yapan personelin %59.0'ı bu konuda bir eğitim almamıştır."* Bu rakam **belediyelerin depolarıyla** ilgili.

### Mevzuat
- **Lejyoner Hastalığı Kontrol Usul ve Esasları Hakkında Yönetmelik** ([RG 13.05.2015/29354, PDF](https://hsgm.saglik.gov.tr/depo/birimler/mikrobiyoloji-referans-laboratuvarlari-ve-biyolojik-urunler-db/Dokumanlar/LEJYONER_HASTALIGI_KONTROL_USUL_VE_ESASLARI_YONETMELIK.pdf)):
  - Madde 8(1)(a): *"Soğuk su tankları en az yılda iki kez, sıcak su tankları ise en az yılda üç kez boşaltılır, temizlenir ve dezenfekte edilir."*
  - Madde 8(1)(b): Suyun durduğu veya çok yavaş aktığı ölü bölge bırakılmaz.
  - **Kapsam (Madde 5):** yataklı sağlık kurumları, turistik konaklama tesisleri, huzurevleri, büyük AVM'ler ve benzerleri. **Konut ve apartman kapsamda değil.**
- **Sağlık Bakanlığı'nın konut deposu temizliği genelgesi: doğrulanamadı.**
  - Adana makalesinin yazarları *"Sağlık Bakanlığı su depolarının yılda iki kere profesyonel ekiplerce temizlettirilmesi gerektiği konusunda kullanıcıları uyarsa da"* diyor, ama birincil kaynak göstermiyor.
  - [memurlar.net'teki eski bir haber](https://www.memurlar.net/haber/679318/bakanliktan-uyari-suya-dikkat.html), sağlık kurumlarına yönelik bir genelgeden söz ediyor (tarihi belirsiz).
  - Yorum: Konutlarda depo temizliği için **bağlayıcı bir periyot bulamadım.** Bu bir boşluk ve sunumda "kimse sorumlu değil" argümanını destekliyor.
- **İnsani Tüketim Amaçlı Sular Hakkında Yönetmelik:** Arama özetine göre kalite, musluktan akan suda aranıyor ([alomaliye](https://www.alomaliye.com/2005/02/17/insani-tuketim-amacli-sular-hakkinda-yonetmelik/)). Madde metnini açıp okumadım, **doğrulanamadı.**
- **Uluslararası referans:** İngiltere'nin iş sağlığı ve güvenliği kurumu HSE ([sayfa](https://www.hse.gov.uk/Legionnaires/things-to-consider.htm)) şunları öneriyor:
  - *"Keep the volume of water stored to a minimum (just enough for 1 day's usage)."*
  - *"Check to ensure the tank remains clean, at least annually."*
  - Depolanan su 20°C'nin altında kalmalı.
  - Yorum: "Depoyu az doldur" fikrinin resmî bir dayanağı var.

### 2025-2026 kesintileri ve depo talebi

| İddia | Kaynak | Durum |
|---|---|---|
| İzmir'de 6 Ağustos 2025'ten itibaren 13 ilçede gece 23:00–05:00 arası planlı ve dönüşümlü kesinti yapıldı, 6 Şubat 2026'da sona erdi. Tahtalı Barajı'nın aktif doluluğu 30 Aralık 2025'te %0,13'tü. | [İZSU, 06.02.2026](https://izsu.gov.tr/haberler/tahtali-yukselise-gecti-gece-kesintileri-sona-erdi) | Doğrulandı (resmî). |
| İzmir'de kesintinin ilk programı: 6–21 Ağustos 2025, 5 bölge, 11 ilçe. | [memurlar.net / İHA, 06.08.2025](https://www.memurlar.net/haber/1142818/izmir-de-bes-bolgede-donusumlu-su-kesintisi-basliyor.html) | Doğrulandı. |
| Kesinti sıklığı sonradan değişti: "3 günde 1"den "2 günde 1"e (Eylül 2025), sonra "her gün"e (Aralık 2025). | Arama özetleri ([Yeni Şafak](https://www.yenisafak.com/izmirde-su-kesintileri-2-gunde-1e-dusuruldu-izmirde-hangi-mahallelerde-su-kesintisi-var-iste-su-kesintisi-programi-h-4747100), [Milliyet](https://www.milliyet.com.tr/galeri/izmir-su-kesintisi-17-aralik-2025-izmirde-sular-nerede-kesik-sular-ne-zaman-gelecek-iste-izsu-planli-su-kesintisi-programi-7503723)) | Kısmen doğrulandı. |
| Ankara: ASKİ, kuraklık nedeniyle suyu "en az su tüketilen saatlerde" kontrollü vereceğini açıkladı. Kuraklık yaklaşık 18 aydır sürüyor. | [Habertürk / AA, 04.12.2025](https://www.haberturk.com/baskentte-kontrollu-su-donemi-3842844) | Doğrulandı. |
| İzmir'de ev tipi depo üretimi son iki ayda "%100'e yakın" arttı. | Bir üreticinin beyanı, [Haber7 / AA, 31.07.2025](https://www.haber7.com/guncel/haber/3551756-su-kesintileri-izmirlileri-su-deposu-almaya-yoneltti) | Doğrulandı, ama resmî istatistik değil. |
| "Ev tipi su deposu" aramaları %150 arttı. | [NTV, 09.01.2026](https://www.ntv.com.tr/ntvpara/galeri-su-kesintileri-artiyor-depo-almak-isteyenlerin-aramalari-artti-1706724) | Rakamın kaynağı haberde yazmıyor. Zayıf. |

- Yorum: İzmir'deki kesinti takvimi 6 ay içinde en az üç kez değişti. Bu, d) bölümündeki "sabit zamanlayıcı yetmez" argümanının somut örneği.
- **Apartman deposu talebindeki artışa dair resmî veri bulamadım.** Haberlerin çoğu ev tipi depolarla ilgili.

---

## b) Benzer çözümler

| Ürün / çalışma | Ne yapıyor | Taze Depo'dan farkı | Durum |
|---|---|---|---|
| **Keraflo Tanktronic** (İngiltere) | Elektronik depo yönetimi. Seviye ve sıcaklığı izliyor, motorlu vanayla depoyu dolduruyor. *"Each tank can be set with its own operating levels to follow up to 10 x schedules; close level, fill delay…"* Ayrıca *"Holiday Schedule feature enables users to vary tank capacity to match changing levels of demand"*. Binanın merkezi yönetim sistemine (BMS) alarm gönderebiliyor. | Seviye **kullanıcının elle girdiği takvime** göre değişiyor. Tüketim tahmini, kesinti riski ve su yaşı hesabı **yok** (broşürde geçmiyor). Pazarı İngiltere: sürekli şebeke, kesinti sorunu yok. | Doğrulandı ([broşür PDF](https://cdn.shopify.com/s/files/1/0620/6219/8980/files/Tanktronic-6p-Flyer-2022-ID-42803.pdf)). **En yakın rakip.** |
| **Wilo break tank** (PE ara depo, 150–3000 L) | Hidroforu şebekeye dolaylı bağlayan ara depo. Teslimatta *"Water level indicator"* ve düşük su seviyesi için *"float switch"* var. | Pasif. Elektronik ya da değişken seviye kontrolü yok, su yaşı yönetimi yok. | Doğrulandı ([ürün sayfası](https://wilo.com/gb/en/Products/en/accessory/break-tank-for-sanitary-water-application-rectangular-version)). Yorum: **Wilo için fırsat**, depo ile hidrofor zaten aynı sistemde. |
| **Grundfos** | Hidrofor setlerinde ölü bölge bırakmayan "hygienic manifold" tasarımı var ([sayfa](https://www.grundfos.com/ca/learn/research-and-insights/hygienic-designed-manifold)). Home Booster kılavuzu, su uzun süre kullanılmazsa deponun boşaltılıp yıkanmasını öneriyor. | Depo seviyesi ya da su yaşı yönetimi bulamadım. | Kısmen (yalnız arama özeti). |
| **Şehir şebekesi ölçeğinde araştırma** (Technion, Shmaya ve Ostfeld) | Şebeke depolarında maliyet ile su yaşı arasındaki dengeyi gözeten pompa ve depo işletimi; belirsiz talep altında model öngörülü kontrol (MPC). | Bina ölçeğinde değil, şehir şebekesinde. Yorum: Yöntemin bilimsel dayanağı var, ama apartman deposuna uygulanmasını bulamadım. | **Doğrulanamadı** (MDPI 403 verdi; yalnız [arama özeti](https://ostfeld.net.technion.ac.il/files/2025/06/202.pdf)). |
| **EPA önerisi** | *"Optimize pumping and tank filling/draining operations."* Depoyu gereğinden büyük yapmamayı öneriyor. | Kılavuz, ürün değil. | Doğrulandı ([PDF](https://www.epa.gov/system/files/documents/2022-04/ds-toolbox-fact-sheets_water-age-mgt_final-508_revised.pdf)). |
| **Türkiye'deki ürünler** | Alarko dijital pompa panosunda "su seviye göstergesi" var ([kılavuz](https://www.alarko-carrier.com.tr/Data/Files/Dokumanlar/kullanim-kilavuzu/dijital-pompa-kontrol-panosu-kk-d1-17-04-2024.pdf)). Ajax ve Sonoff kaçak durumunda suyu kesen akıllı vanalar satıyor. | Hiçbiri su yaşı ya da dinamik seviye yapmıyor. | Kısmen (yalnız arama özeti; Alarko kılavuzunu açmadım). |

**Özgünlük sonucu:**
- **Seviyeyi elektronik olarak ayarlamak yeni değil** (Tanktronic).
- Aramalarımda bulamadığım dört şey var:
  1. Kesinti riskine göre otomatik seviye.
  2. Hidrofor verisinden tüketim çıkarmak.
  3. Su yaşına göre temizlik uyarısı.
  4. Kesintili şebeke koşullarında apartmana yönelik ürün.
- Bunlar "yok" demek değil, "bulamadım" demek. Mentora sorulmalı.

---

## c) Teknik uygulanabilirlik

### Tipik kurulum (varsayım)
Şebeke → şamandıralı giriş vanası → bodrum deposu → hidrofor → daireler.
- **Varsayım:** Bu düzen Türkiye'deki apartmanlarda yaygın.
- Çatı deposu (yerçekimiyle besleme), depoyu atlayan bypass hattı veya depo yokken doğrudan şebekeden besleme gibi varyantlar olabilir.
- Hangi düzenin yaygın olduğunu mülakatlarda sor (interview-guide'ın demografik kısmı).

### Seviyeyi dinamik ayarlamak için gerekenler

| Bileşen | Görev | Not |
|---|---|---|
| Seviye sensörü (hidrostatik basınç transmitteri ya da ultrasonik) | Depodaki hacmi ölçer: V(t) = A·h(t) | Wilo break tank'ın kendi seviye göstergesinin elektriksel çıkışı olup olmadığını bilmiyorum. |
| Motorlu küresel vana ya da solenoid vana (giriş hattında) | "Kapanma seviyesini" değişken yapar | Normalde açık seçilmeli: elektrik veya kontrolcü arızasında depo bugünkü gibi şamandıra seviyesine kadar dolar. **Mevcut şamandıra taşma emniyeti olarak kalır.** |
| Kontrolcü (ESP32 ya da Raspberry Pi) | Modbus ile hidrofor verisini okur, vanayı sürer, buluta veri gönderir | V1 test düzeneğindeki donanımla ortak. |
| Opsiyonel: sıcaklık sensörü | HSE'nin 20°C sınırını izler | Ucuz. |
| Opsiyonel: serbest klor sensörü | Su yaşını doğrudan kaliteyle doğrular | Pahalı ve bakım istiyor. İlk sürümde yok. |

Fiyatları doğrulamadım.

### Tüketim tahmini: hidrofor verisinden ne kadar mümkün?
Kütle dengesi: A·dh/dt = Q_giriş − Q_çıkış. Depodan çıkan su (Q_çıkış), hidroforun bastığı suya ve binanın tüketimine eşit.

| Yöntem | Nasıl | Güvenilirlik |
|---|---|---|
| **1. Vana kapalıyken seviye düşüşü** | Q_çıkış = −A·dh/dt | **En doğrudan.** Vanayı Taze Depo kontrol ettiği için vananın kapalı olduğu aralıklar bilinir. Depo taban alanı (A) kurulumda ölçülür. |
| **2. Hidrofor verisi** | Wilo Helix2.0-VE, CIF modülüyle *hesaplanmış debi* (0,1 m³/h) veriyor. SC2.0 kontrol ünitesi ise pompa çalışma biti ve basınç veriyor ([v1-validation.md](v1-validation.md)). | Wilo, hesaplanmış debinin kapalı döngü kontrolde kullanılmamasını söylüyor. Düşük debilerde doğruluğunu bilmiyorum, test edilmeli. |
| **3. Vana açıkken** | Q_giriş = Q_çıkış + A·dh/dt | Q_çıkış hidrofordan gelirse giriş debisi hesaplanır. **Vana açık olduğu hâlde Q_giriş ≈ 0 ise şebekede kesinti var demektir.** Bina böylece kendi kesinti kaydını tutar. |

**Dürüst not:** Seviye sensörü varsa, tüketimi bulmak için hidrofor verisi **şart değil** (Yöntem 1 yeter).
- Hidrofor verisinin katkısı: Yöntem 3, çapraz doğrulama ve V1 (kaçak) ile ortaklık.
- Yorum: Tek başına Taze Depo'da Wilo bağı zayıflıyor, birleşik versiyonda güçleniyor.

### Su yaşı hesabının fiziği
Tanım: *"Water age is the time spent by a parcel of water in the network."* ([EPANET 2.2 kılavuzu](https://usepa.github.io/EPANET2.2/3_network_model.html)). Burada "depoya girdiğinden beri geçen süre" olarak kullanılıyor. EPANET'teki dört depo karışım modeli aynı sayfada:

| Model | Varsayım | Depodaki yaş | Hangi depoya uyar (EPANET) |
|---|---|---|---|
| **Tam karışım** | *"all water that enters a tank is instantaneously and completely mixed"* | Kütle dengesinden: **da/dt = 1 − (Q_giriş / V)·a**. Kararlı durumda **a ≈ V/Q**. | *"facilities that operate in fill-and-draw fashion"* |
| İki bölmeli | İki ayrı tam karışımlı bölme | İkinci bölme ölü bölgeyi temsil eder, o bölgedeki yaş daha yüksektir. | Kısa devre akış ve ölü bölge |
| **Tıkaç akış (FIFO)** | *"no mixing of water at all"*, ilk giren ilk çıkar | Çıkan suyun yaşı en yaşlı parselin yaşıdır, kararlı durumda ≈ V/Q. | *"baffled tanks … simultaneous inflow and outflow"* |
| Tıkaç akış (LIFO) | Son giren ilk çıkar | **Dipteki su seviye o noktaya inmedikçe hiç yenilenmez.** Yaşı sınırsız büyüyebilir. | Girişi ve çıkışı dipte olan dar ve uzun depolar |

**Asıl kaldıraç:** Hangi model geçerli olursa olsun, kararlı durumda yaş, depolanan hacim bölü tüketim (V/Q) ile orantılı. **Tüketimi değiştiremeyiz, ama V'yi değiştirebiliriz.**
- Örnek (gerçek veri değil, oran örneği): Depo hacmi 3 günlük tüketime eşitse tam karışımda ortalama yaş yaklaşık 3 gün olur. Seviye 1 günlük tüketimde tutulursa yaklaşık 1 güne iner.
- LIFO benzeri bir depoda ayrıca **ara sıra düşük seviyeye inmek** (dip suyunu yenilemek) gerekir.
- Türk apartman depolarında hangi modelin geçerli olduğunu bilmiyorum. Bu, girişin ve çıkışın deponun neresinde olduğuna ve deponun şekline bağlı.
- Sunumda tam karışım modeli kullanılabilir. Model belirsizliği "varsayım" olarak işaretlenir; finalde iki model karşılaştırılır.

### Hedef seviye
- V_hedef(t) = max( V_yedek(t), V_min ).
- **Yedek ihtiyacı:** V_yedek = tahmini tüketim (beklenen kesinti süresi boyunca) + güvenlik payı.
- **Fiziksel taban:** V_min, hidroforun kuru çalışmasını önleyen asgari seviye.
- Yaş sınırı aşılırsa (yani yedek ihtiyacı nedeniyle depo uzun süre dolu kalırsa) **temizlik ya da yöneticiye uyarı** gönderilir.
- **Öncelik her zaman yedekte:** Sistem binayı susuz bırakmamalı.

---

## d) "Basit bir zamanlayıcı neden yetmez?"

| | Sabit kural ya da zamanlayıcı (Tanktronic benzeri) | Taze Depo (yapay zekalı) |
|---|---|---|
| Yedek hacmi | Elle girilen sabit seviye | Binanın kendi tüketimini tahmin eder (gün, saat, mevsim, tatil). Yedek, beklenen kesinti süresine göre hesaplanır. |
| Kesinti takvimi | Elle girilir, değişince elle güncellenir | İzmir'de kesinti takvimi 6 ayda en az 3 kez değişti (bkz. a). Bina kesintiyi Yöntem 3'le kendisi algılar, desenini öğrenir ve depoyu önceden doldurur. Duyurulmuş kesintiler de bir girdi olabilir (İSKİ'nin kesinti sorgulama sayfası var; makine okunabilir bir arayüzünü **doğrulamadım**). |
| Su yaşı | Hesaplanmaz | Ölçülen tüketim ve karışım modeliyle sürekli hesaplanır. |
| Temizlik | Takvime göre ya da hiç | Su yaşı ve sıcaklık geçmişine göre uyarı verir. |
| Hata maliyeti | Seviye düşük ayarlanırsa kesintide su biter, yüksek ayarlanırsa su bayatlar | Belirsizliği tahmin ederek ikisi arasındaki dengeyi kurar (olasılıksal tahmin ve model öngörülü kontrol). |

**Dürüst değerlendirme:**
- Su yaşı hesabı fiziktir, yapay zeka değil.
- "Seviyeyi ortalama günlük tüketimin k katında tut, duyurulan kesintiden önce doldur" gibi basit bir kural da faydanın önemli kısmını alabilir.
- Yapay zekanın gerçek katkısı iki yerde:
  1. **Belirsiz ve değişken kesintilerde yedek ile tazelik arasındaki dengeyi binaya özel kurmak.**
  2. **Ek sayaç olmadan tüketim ve kesinti verisi üretmek.**
- Jüri "bunu bir kural yapmaz mı?" diye sorarsa, bu iki noktayla ve İzmir'deki değişen takvim örneğiyle cevap verilmeli.

---

## Puan tablosu (1–5)

Yorum: Puanlar benim değerlendirmem, ölçüm değil. Mülakatlardan sonra güncellenmeli.

| Kriter (ağırlık) | Taze Depo | V1 Kaçak | Birleşik |
|---|---|---|---|
| Problem-ihtiyaç-çözüm uyumu (%25) | **4.** Bina ölçeğinde kanıt güçlü (4 saha çalışması), ikilem Tayvan çalışmasında yazılı, kesintiler güncel. Kullanıcının bu acıyı gerçekten hissedip hissetmediği bilinmiyor. | **3.** Türkiye'de bina içi kaçağa dair veri zayıf: ulusal kayıp oranı şebekeyi kapsıyor, sayaçtan sonraki kaçağı değil ([v1-validation](v1-validation.md) c). | **3.** İki problem, hikâyeyi bölüyor. Uyum, hangi problemin ana problem olduğuna bağlı. |
| Özgünlük (%20) | **4.** Elektronik seviye var (Tanktronic), ama kesinti farkındalığı, su yaşı ve hidrofor verisi birlikte bulunamadı. | **3.** Grundfos, DAB ve Wilo'da kaçak algılama zaten var. Fark yalnız debi, maliyet ve kaçak türü. (2026-11-17'deki 4 puan, v1-validation'daki rakip bulgusundan sonra düşürüldü.) | **4.** "Pompa binanın sensörü" çerçevesi iki kullanım alanıyla daha özgün. |
| Yapay zekanın anlamlı kullanımı (%20) | **3.** Tahmin ve optimizasyon anlamlı, ama basit bir kural faydanın önemli kısmını alabilir (bkz. d). | **4.** Dolaylı sinyalden kaçak debisi çıkarmak gerçek bir tahmin ve öğrenme problemi. | **4.** Ortak tüketim modeli iki işi birden görüyor. |
| Uygulanabilirlik (%20) | **3.** Ek donanım gerekiyor (sensör ve vana; bileşenler olgun, Tanktronic bunu kanıtlıyor). Bu kurguya uygun açık veri setim yok, test yalnız simülasyonla yapılabilir. Yanlış seviye kararının riski var: bina susuz kalabilir. | **4.** Seviye 1 veri Modbus'tan ek donanımsız okunuyor; simülasyon ve test düzeneği tasarlandı. | **3.** Kapsam büyük, iki ayrı doğrulama gerekiyor. |
| Etki ve gelişim (%15) | **3.** Etki daha çok sağlık ve su kalitesinde. Su **miktarında** doğrudan tasarruf kanıtım yok (8 sorudan 7. soru zayıf kalıyor). Gösterge: depo su yaşı (saat), yaş sınırını aşan süre yüzdesi. | **4.** Doğrudan su tasarrufu (L/saat, TL/ay). | **4.** Hem miktar hem kalite. |
| **Ağırlıklı toplam** | **3,45** | **3,55** | **3,55** |

- Yorum: Fark 0,1 puan, değerlendirme belirsizliğinin içinde kalıyor. Bu tablo seçimi belirlemiyor; **mülakatlar belirleyecek.**
- Belirleyici sorular:
  1. Yöneticiler ve sakinler depo suyunun bayatlığını mı, kesintide susuz kalmayı mı, yoksa su faturası ve kaçağı mı daha çok dert ediyor?
  2. Depo + hidrofor düzeni ne kadar yaygın?
  3. Depoyu kim, ne sıklıkla temizliyor?

## Açık konular
- Diyarbakır tezinin tam metnini tarayıcıda aç; yılı ve yöntemi doğrula.
- Konut deposu temizliğine dair Sağlık Bakanlığı veya belediye düzenlemesi var mı? Mentora ya da İl Sağlık Müdürlüğü'ne sor.
- Wilo'nun SiBoost / break tank tarafında seviye verisi okunabiliyor mu? Mentora sor.
- Taze Depo'da su **miktarı** etkisi: taşma kaybı, temizlikte boşaltılan su gibi kayıplar ölçülebilir mi? Kaynak bulamadım.
