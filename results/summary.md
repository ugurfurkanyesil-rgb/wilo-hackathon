# Simülasyon sonuçları

Tarih: 2026-11-23. Bütün sonuçlar **simülasyondur**. Gerçek bina verisi yok. Parametrelerin çoğu varsayım [V]; kaynaklı olanlar [K] diye işaretli (`src/sim/*.py`). Yeniden üretmek için:

```powershell
python scripts\run_leak.py
python scripts\run_tank.py
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
- **Maliyet bağlamı:** İSKİ Ocak 2026 tarifesiyle 10 L/sa ≈ 380 TL/ay, 20 L/sa ≈ 760 TL/ay.

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

## Sınırlar
- SCe (frekans konvertörlü) kontrolün sıfır debi testi modellenmedi, yalnız SC modu var.
- Basınç tankının hacmi, ön dolum basıncı ve Wilo'nun gerçek kontrol davranışı varsayım.
- Depodaki karışım modeli varsayım. LIFO tipi bir depoda yaş daha yüksek çıkar.
- Gerçek veri ya da düzenek ölçümü yok. Sıradaki adım `docs/v1-test-rig.md`.
