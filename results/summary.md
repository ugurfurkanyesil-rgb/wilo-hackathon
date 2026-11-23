# Simülasyon sonuçları

Tarih: 2026-11-23. Bütün sonuçlar **simülasyondur**. Gerçek bina verisi yok. Parametrelerin çoğu varsayım [V]; kaynaklı olanlar [K] diye işaretli (`src/sim/*.py`). Yeniden üretmek için:

```powershell
python scripts\run_leak.py
python scripts\run_tank.py
python scripts\run_checks.py   # ek sağlamlık testleri A–F (run_leak.py'den sonra)
```

---

## 1. Kaçak (V1): hidrofor verisinden gece kaçağı

**Kurgu.**
- Gece 00:00–05:00 penceresi, 1 sn okuma aralığı, sabit hızlı pompa (SC, iki eşikli kontrol). Membranlı basınç tankı Boyle yasasıyla modellendi.
- Gece kullanımı: sifon ve musluk olayları, saatte 0,5–3 olay [V].
- Kaçak modelleri: boru (orifis, Q ∝ √p) ve klozet rezervuarı (dönemsel dolum darbeleri).
- Modele giden veri Modbus'tan okunacak veriye benziyor:
  - Basınç: 0,1 bar adımlı, ±0,02 bar gürültülü.
  - Pompa "çalışıyor" biti.
  - Hesaplanmış debi: yalnız karşılaştırma için kullanıldı.
- Tank hacmi koşudan koşuya değişiyor: 24, 50 veya 100 L [V].
- Her tahmin **7 gecelik** veriden yapılıyor.

**Yöntem** (`src/sim/leak_estimator.py`):
- Pompa dururken kaçak tankı boşaltır, bu yüzden duruş süresi T_off ≈ ΔV / Q olur.
- Gece kullanımı duruşu yalnız **kısaltır**. Bu yüzden 7 gecedeki en uzun duruşlar ΔV / Q etrafında dar bir küme oluşturur.
- Kaçak kararı için üç koşul aranıyor:
  1. Küme dar olmalı (değişim katsayısı ≤ 0,10).
  2. Kümede en az 4 duruş olmalı.
  3. Küme en az 3 farklı gecede görülmeli.
- ΔV, kurulumda bir kez **bilinen 10 L/sa'lik test vanası** açılarak kalibre ediliyor. Bunun nedeni pompanın kapama basıncını biraz aşması ve Boyle hesabının gerçekte çekilen hacmi eksik vermesi.
- Eşik 15 eğitim tohumunda seçildi, sonuçlar 20 ayrı test tohumunda ölçüldü. Toplam 260 test koşusu var.

**Sonuçlar (test kümesi)**

| Gösterge | Değer |
|---|---|
| Kaçak yokken yanlış alarm | 20 koşudan 1'inde (%5) |
| %90+ tespit edilen en küçük kaçak | **20 L/sa** (10 L/sa'te %85–90) |
| Tespit edilen kaçaklarda debi hatası (MAPE) | **%10** |
| Basit yöntem: pompalanan hacim / süre | Ortalama %131 hata. Gece kullanımını da kaçak sayıyor, medyan sapma +6,3 L/sa. |
| Anlık hesaplanmış debi (Seviye 2 register) | Bütün senaryolarda medyan **0 L/sa**. Pompa gece çoğunlukla duruyor. |

Kaçak debisine göre tespit oranı:

| Kaçak (L/sa) | 2 | 3 | 5 | 10 | 20 | 50 |
|---|---|---|---|---|---|---|
| Boru | 0,15 | 0,30 | 0,60 | 0,85 | 1,00 | 1,00 |
| Rezervuar | 0,20 | 0,30 | 0,65 | 0,90 | 1,00 | 1,00 |

- Tank büyüdükçe tespit zorlaşıyor. Tespit oranı 24 L tankta %74, 50 L'de %62, 100 L'de %50 (bütün kaçak debileri birlikte). Büyük tankta ΔV büyük olduğu için küçük kaçağın duruş süresi gece penceresini aşıyor.
- **Maliyet bağlamı:** İSKİ konut 1. kademe Kasım 2026 tarifesiyle (su 44,63 + atıksu 22,28 = 66,91 TL/m³, KDV hariç; [Endeks24, 19.11.2026](https://www.endeks24.com/istanbul-da-suya-her-ay-zam-2027-de-de-surecek-tavan-yuzde-2)) 10 L/sa ≈ 482 TL/ay, 20 L/sa ≈ 963 TL/ay. Tarife her ay güncellendiği için bu rakamlar da değişir.

**Kaçak türü: boru mu, klozet rezervuarı mı?**

İlk denemede tek bir özellik (basıncın darbeli düşmesi) kullanıldı. Bu yalnız 24 L tankta işe yaradı. 50–100 L tankta rezervuarın dolum darbesi 0,1 bar adımın altında kalıyor. Bu yüzden ikinci bir fiziksel imza eklendi:

- **Basınca bağımlılık:** Boru kaçağının debisi basınca bağlı (Q ∝ p^N1). Bu yüzden boru kaçağı tankı döngünün yüksek basınçlı ilk yarısında daha hızlı boşaltır. Rezervuar kaçağının debisi basınçtan bağımsızdır.
  - Ölçüm: (orta basıncın altında geçen süre) / (üstünde geçen süre).
  - Bu oran temiz döngülerin medyanından alınıyor. Tek bir döngüde fark 0,1 bar adımın altında kalıyor, ama 7 gecedeki onlarca döngünün medyanında görülebiliyor.
  - Kurulum testindeki vana boru gibi davrandığı için oran o testteki değere bölünerek normalize ediliyor.
- **Darbeli düşüş:** Rezervuar suyu darbelerle çektiği için basınç basamak basamak düşüyor. Ölçüm: 30 saniyelik düşüşlerin 99. yüzdeliğinin ortalamaya oranı. Bu imza küçük tankta görülüyor.
- **Sınıflandırıcı:** İki imza, kaçak debisi ve ΔV ile bunların etkileşimleri bir lojistik regresyona veriliyor. Hangi imzanın işe yaradığı tank boyuna bağlı olduğu için etkileşim terimleri gerekiyor; onlarsız test doğruluğu %89'du.

| Tür sınıflandırması (tespit edilen kaçaklar) | Doğruluk |
|---|---|
| Test kümesi, toplam (159 kaçak) | **%97** |
| 24 L / 50 L / 100 L tank | %100 / %94 / %92 |
| Sağlamlık: boru kaçağı, N1 = 1,0 (eğitimde 0,5) | %97 (30 koşu) |
| Sağlamlık: rezervuar dolum hacmi 0,8 L (eğitimde 0,5) | %100 (30 koşu) |
| Sağlamlık: rezervuar dolum hacmi **0,3 L** | **%63** (30 koşu) |

**Okuma:**
- Kaçak türü simülasyonda büyük ölçüde ayrılıyor.
- Rezervuar küçük darbelerle doluyorsa ayrım zayıflıyor. Gerçek rezervuarların dolum davranışını bilmiyoruz [V].
- Bu iddia, finalde test düzeneğinde gerçek bir klozet rezervuarı ve iğneli vanayla sınanacak.

**Grafikler:** `leak_night_trace.png` (kaçaksız gece ile 5 L/sa kaçaklı gece), `leak_estimate_vs_true.png`.

---

## 2. Taze Depo: kesinti takvimi değişirken depo seviyesi

**Kurgu.**
- Bina: 12 daire, 36 kişi, kişi başı 146 L/gün [K, ikincil kaynak], yani günde ≈5,3 m³.
- Depo 10 m³ [V]. Şebekeden dolum 4 m³/sa [V].
- 180 gün, saatlik adım. İlk 14 gün ölçüme katılmıyor.
- Su yaşı tam karışım modeliyle hesaplandı (EPANET "MIXED").
- Kesinti senaryosu [V]. İki gerçek olaydan esinlenildi: İzmir'de kesinti sıklığının değişmesi ve Ankara'da suyun yalnız az tüketilen saatlerde verilmesi. Üç dönem var:
  - Gün 0–60: 3 günde bir, 23:00–05:00.
  - Gün 60–120: 2 günde bir, 09:00–21:00.
  - Gün 120–180: her gün 08:00–22:00.
  - Bunlara ek olarak ayda yaklaşık 2 habersiz kesinti, 4–16 saat.
- 20 rastgele senaryonun ortalaması alındı.

**Karşılaştırılan politikalar:**
- **Şamandıra:** Bugünkü durum, depo hep dolu.
- **Sabit kural:** Depoda k günlük ortalama tüketim kadar su tutulur.
- **Sabit takvim:** Kurulumda girilen ilk kesinti takvimine göre önceden doldurur (Tanktronic benzeri). Takvim sonradan değişse de güncellenmez.
- **NABIZ:**
  - Binanın kendi kesinti desenini son 10 günden öğrenir. Şebekede su olup olmadığını her saat kısa bir vana testiyle anlar [V].
  - Tüketimi saat bazında 90. yüzdelikle tahmin eder.
  - Beklenen bir sonraki kesintiyi köprüleyecek kadar su tutar. Habersiz kesintiler için de bir "taban yedek" bırakır.

| Politika | Ortalama su yaşı (sa) | Susuz saat (166 gün) |
|---|---|---|
| Şamandıra (hep dolu) | 39,4 | 0,9 |
| Sabit takvim (kurulumda girilen) | 24,2 | **38,0** |
| Sabit kural, 1 günlük | 19,1 | 54,0 |
| Sabit kural, 1,25 günlük | 24,5 | 8,2 |
| Sabit kural, 1,5 günlük | 30,2 | 3,7 |
| **NABIZ, taban 12 sa** | 20,6 | 16,1 |
| **NABIZ, taban 18 sa** | 25,5 | 6,2 |
| **NABIZ, taban 24 sa** | 31,4 | 2,9 |

**Dürüst okuma:**
- **Şamandıraya göre:** NABIZ (taban 18 sa) suyun yaşını **%35 düşürüyor** (39 → 25 sa). Bunun karşılığında 166 günde yaklaşık 6 susuz saat var. Şamandırada bu süre 1 saatin altında.
- **Kurulumda girilen sabit takvime göre:** Aynı tazelikte (≈25 sa) **6 kat daha az susuz saat** (38 → 6). Takvim değişince sabit takvim çöküyor. "Basit zamanlayıcı neden yetmez?" sorusunun doğrudan cevabı bu.
- **Sabit kurala göre:** Kazanç **küçük**. En iyi ayarlanmış sabit kural (1,25 gün) NABIZ eğrisine çok yakın. Fark taze uçta açılıyor: yaklaşık 20 saatlik yaşta NABIZ 16 susuz saat veriyor, 1 günlük sabit kural 54. Doğru k değerini ise ancak sonradan bilebiliyoruz.
- Habersiz kesintiler öngörülemiyor. Bu kesintilerin riskini "taban yedek" belirliyor, yani tazelik ile güvence arasındaki seçimi yöneticiye bırakan bir ayar var.

**Grafikler:** `tank_tradeoff.png` (tazelik ve güvence eğrisi), `tank_week_trace.png` (kesinti her güne geçtikten sonraki bir hafta).

---

## 3. Ek sağlamlık testleri (`scripts/run_checks.py`)

Ana test kümesinin dışında, yöntemi zorlayan altı durum denendi (A–F). A–E, 20 ayrı test binasında koşuldu; tank boyu ve gece kullanımı ana testteki gibi rastgele. Kaçak türü sınıflandırıcısı ana testte eğitilen modeldir, burada yeniden eğitilmedi (A hariç, aşağıda açıklandı).

**A. Frekans konvertörlü kontrol (SCe).**
- Kılavuza göre SCe basıncı sabit tutuyor ve belirli aralıklarla bir "sıfır debi testi" yapıyor: debi yoksa pompayı durduruyor, basınç düşünce yeniden çalıştırıyor ([SC2.0-Booster kılavuzu, s.14](https://cms.media.wilo.com/dcidocpfinder/wilo629451/7984526/wilo629451.pdf)). Testin debi eşiği ve aralığı fabrika ayarı; bilmiyoruz. Varsayılan eşik 30 L/sa, aralık 60 sn [V].
- **Eşiğin altındaki kaçaklar:** Pompa yine durup kalkıyor, yöntem çalışıyor. 5 L/sa'te %85–90, 10 L/sa ve üstünde %100 tespit; debi hatası %8.
- **Eşiğin üstündeki kaçaklar:** Sıfır debi testi geçmediği için pompa bütün gece çalışıyor. Yöntem bunu "gece boyunca durmadı" diye yakalıyor ve **büyük kaçak** olarak işaretliyor (50 L/sa'te %100). Debisini Seviye 1 veriyle söyleyemiyor.
- Eşik değişirse sınır da kayıyor: eşik 15 L/sa olunca 20 L/sa'lik kaçak da "büyük kaçak" oluyor; 60 L/sa olunca 50 L/sa'lik kaçak debisiyle ölçülüyor.
- **Kaçak türü:** SC verisiyle eğitilen sınıflandırıcı SCe'de çalışmadı (%52, yazı tura). SCe'de basınç 3,5–4,0 bar arasında dolaşıyor, SC'de 3,0–4,0. Aynı yöntemle SCe verisinden ayrı eğitilen bir sınıflandırıcı (eğitim tohumları 1–15) testte **%99** doğruluk verdi. Yani her kontrol modu için ayrı model gerekiyor. Eğitim aralığının dışındaki bir debide (eşik 60 iken 50 L/sa) bu model de yanıldı.
- Yanlış alarm: 20 kaçaksız binanın 2'sinde (%10). Biri 0,8, diğeri 4,1 L/sa gibi küçük bir değer verdi.

**B. Basınç tankının hava basıncını kaybetmesi.**
- Membranlı tankların ön dolum basıncı zamanla düşer. Kurulumda yapılan test vanası kalibrasyonu (ΔV) eskir ve debi tahmini kayar.
- Kurulumdan sonra 0,3 / 0,6 / 1,0 bar kayıpta debi hatası %11 / %22 / %34'e çıktı. Tespit ve tür doğruluğu etkilenmedi (%98–100).
- **Çözüm denendi:** ΔV, pompanın her çalışmasının süresinden yeniden hesaplanırsa (ΔV ≈ pompa debisi × çalışma süresi, kurulumdaki oranla ölçeklenmiş; pompa debisi 2 m³/sa [V]) hata **%3**'e iniyor. Bu, finalde modele eklenecek.
- Not: Tank hava kaybı kendi başına bir bakım ihtiyacı. Aynı hesap ΔV'nin zamanla küçüldüğünü göstereceği için ayrıca "tankın havası azaldı" uyarısı verilebilir. Bu simülasyonda test edilmedi.

**C. Daha gürültülü basınç sensörü (±0,05 bar, ana testte ±0,02).** Tespit %94, debi hatası %2, tür %96, yanlış alarm %5. Etkisi küçük.

**D. Daha kalabalık geceler (saatte 3–5 kullanım, ana testte 0,5–3).** Tespit **%73**'e düştü, yanlış alarm **%10** (20 binada 2). Kullanım arttıkça temiz duruşlar azalıyor. Gece vardiyalı ya da kalabalık binalarda daha uzun gözlem (7 yerine 14 gece) gerekebilir; denenmedi.

**E. Veri buluttan, seyrek aralıkla gelirse (10 sn / 60 sn / 5 dk).**
- Neden önemli: Wilo'nun uzaktan izleme platformu Wilo-Monitor. Veri oraya saniyede bir değil, daha seyrek gidebilir; aralığı bilmiyoruz. Algoritmanın bodrumda bir cihazda mı, yoksa doğrudan Wilo-Monitor'da mı çalışabileceğini bu belirliyor.
- **"Pompa çalışıyor" biti seyrek okunursa yöntem çöküyor.** Pompa her seferinde yalnız ≈9 saniye çalışıyor; seyrek örnekleme bu çalışmaların çoğunu kaçırıyor. Tespit 10 sn'de %54'e, 60 sn'de %6'ya düşüyor.
- **Kalkış sayacı kullanılırsa çalışıyor.** Wilo kontrol ünitesinin kümülatif kalkış sayacı (register 40077/40081) hiçbir kalkışı kaçırmıyor. Kalkış anlarını sayacın arttığı okumalardan alan varyantta (`start_intervals`) sonuçlar:

| Okuma aralığı | Tespit | Debi hatası | Yanlış alarm |
|---|---|---|---|
| 10 sn | %88 | %5 | %5 |
| 60 sn | %88 | %5 | %5 |
| 5 dk | %85 | %12 | %10 |

- Kaçak debisine göre (60 sn): 5 L/sa %62, 10 L/sa %88, 20 ve 50 L/sa %100. Bu, ana testteki saniyelik verinin sonuçlarıyla aynı seviyede.
- **Kaçak türü bu varyantta yok.** Tür ayrımı basıncın döngü içindeki şeklini kullanıyor ve saniyelik basınç istiyor.
- **Sonuç (mimari):** Debi, maliyet ve depo önerisi doğrudan Wilo-Monitor'da, 1 dakikalık kalkış sayacı verisiyle hesaplanabilir; bodrumda ayrı bir cihaz gerekmez. Kaçak türü için hesabın kontrol ünitesinin içinde ya da yanında, saniyelik veriyle yapılması gerekir. Bu ikinci aşama olabilir.

**F. Kaçağın pompaya yükü (fazladan kalkış).** Kaçak tankı boşalttıkça pompa kendiliğinden kalkar; kalkış sayısı ≈ kaçak debisi / ΔV. Simülasyonda (gece kullanımı yokken, saatte):

| Tank | ΔV | 5 L/sa | 10 L/sa | 20 L/sa |
|---|---|---|---|---|
| 24 L | 4,6 L | 1,0 | 2,0 | 4,0 |
| 50 L | 9,5 L | 0,4 | 1,0 | 2,0 |
| 100 L | 19,0 L | 0,2 | 0,4 | 1,0 |

- Kaçak gece gündüz sürdüğü için 24 L tankta 10 L/sa'lik bir kaçak günde ≈48 fazladan kalkış demek. Kaçak yokken gece kullanımı (saatte 1,5 olay) yalnız ≈0,9 kalkış/sa üretiyor.
- Kalkışın pompa ömrüne etkisini sayısallaştırmadık. Bunun için pompa ve motorun izin verilen kalkış sayısı Wilo'dan öğrenilmeli. Enerji etkisi küçük: kaybolan su zaten basılıyor, fazladan enerji kaçak hacmiyle orantılı.

**Simüle edilmeyen ama bilinen bir risk: pompanın çek valfi sızdırırsa.** Pompa dururken su çek valften depoya geri kaçar. Bu da tankı basınca bağlı bir hızla boşaltır, yani NABIZ'a "boru kaçağı" gibi görünür. Su kaybolmuyor (depoya dönüyor) ama pompa boşuna çalışıyor ve valfin bakımı gerekiyor. Seviye 1 veriyle bina içi kaçaktan ayrılamaz. Tesisatçı kontrolünde ilk bakılacak yer olarak raporda belirtilmeli.

---

## Sınırlar
- SCe sıfır debi testinin gerçek eşiği ve davranışı bilinmiyor; modeldeki değerler varsayım.
- Basınç tankının hacmi, ön dolum basıncı ve Wilo'nun gerçek kontrol davranışı varsayım.
- Depodaki karışım modeli varsayım. LIFO tipi bir depoda yaş daha yüksek çıkar.
- Gerçek veri ya da düzenek ölçümü yok. Sıradaki adım `docs/v1-test-rig.md`.
