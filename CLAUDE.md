# Water AI Hackathon 2026 — Proje Rehberi

## Bağlam
Water AI Hackathon 2026'ya katılıyorum (Wilo Türkiye x imece). Bu klasör proje klasörüm.

### Soru ve alan
- Soru: **"Yapay zekâdan yararlanarak suyun daha verimli, sürdürülebilir ve akıllı yönetilmesini nasıl sağlayabiliriz?"**
- İki alan var: Şehirler / Binalar. Biz **Binalar** alanındayız.

### Takvim
- 17 ve 19 Kasım: online bootcamp (tamamlandı).
- 23 Kasım Pazartesi: Zoom toplantısı (geri bildirim).
- 24 Kasım Salı akşamı: teslim. E-posta: imece@imece.com, konu: "Water AI Hackathon - (Takım Adı) Proje Fikri".
- 30 Kasım: finalistler açıklanacak.
- 5 Aralık: İstanbul'da final. Sunum Türkçe.
- Yapay zeka araçlarında kısıtlama yok.

### Süreç: tasarım odaklı düşünme
Keşfet → Tanımla → Fikir Üret → Prototiple → Test Et (çift elmas: genişle/daral).
- **Keşfet:** paydaş haritası + 3 mülakat (ödev). Kurallar: önce demografik bilgi; genelden özele açık uçlu sorular; "neden" diye sor; cevap önerme; sessizlikten korkma.
- **Tanımla:** gözlem ≠ içgörü; "3 Neden" kuralı; en önemli 3 içgörü → "...nasıl yapabiliriz?" problem tanımı.
- **Fikir Üret:** oylama kriterleri özgünlük, uygulanabilirlik, ölçeklenebilirlik, etki. Son iki fikir arasında kalınırsa özgünlük × uygulanabilirlik matrisi.

### Teslim formatı
Proje Fikri Kanvası (poster) veya en fazla 10 sayfalık sunum. Opsiyonel 3-4 dk video (link). Her alan 1-2 cümle; doğrulanmamış bilgi **"varsayım"** olarak işaretlenir. 8 soru:
1. **Problem:** kentte/binada hangi somut su sorunu, nerede, kimde? Önemini gösteren gözlem, görüşme veya kaynak.
2. **Hedef kullanıcı ve ihtiyaç:** çözümü önce kim kullanacak, hangi durumda neyi yapmakta zorlanıyor?
3. **Mevcut yaklaşım ve eksikliği:** kullanıcı bugün nasıl baş ediyor, nerede yetersiz?
4. **Çözüm önerisi:** kullanıcı çözümü hangi anda, nasıl kullanacak, neyi daha iyi yapabilecek?
5. **Yapay zekanın rolü:** somut olarak ne yapacak, daha basit bir yönteme göre katkısı ne?
6. **Veri ve uygulanabilirlik:** hangi veri, araç, altyapı gerekli; hangisine erişim var, hangisi doğrulanmadı?
7. **Beklenen su etkisi:** su kullanımında veya sistemin işleyişinde ne değişir, hangi göstergeyle takip edilir?
8. **İlk test:** işe yaraması için hangi varsayım doğru olmalı, hackathon günü nasıl sınanır?

### Değerlendirme kriterleri
| Kriter | Ağırlık |
|---|---|
| Problem, ihtiyaç ve çözüm uyumu | %25 |
| Çözümün özgünlüğü | %20 |
| Yapay zekanın anlamlı kullanımı | %20 |
| Uygulanabilirlik (veri, araç, altyapı, ilk test planı) | %20 |
| Beklenen etki ve gelişim potansiyeli | %15 |

Çalışan demo istenmiyor.

### Wilo hakkında bildiklerimiz
- Pompa üreticisi. Alanları: Bina Teknolojileri, OEM, Su Yönetimi, Sanayi.
- Stratejisi: "Pioneering WATER AI for You" (Creating / Caring / Connecting).
- Bootcamp'te gösterilen su değer zinciri: Su Temini → İçme Suyu Arıtımı → Dağıtım/Basınçlandırma → Atıksu Transferi → Atıksu Arıtımı → Sulama/Yeniden Kullanım. Ayrıca Taşkın Önleme.

### Profil
3. sınıf Elektrik-Elektronik Mühendisliği öğrencisi. Gömülü sistemler, sensörler, C/C++ ve Python biliyor.

## Teknik kararlar
- **Simülasyon (2026-11-23, kullanıcı isteğiyle):** `src/sim/`, `scripts/run_leak.py`, `scripts/run_tank.py`; sonuçlar `results/summary.md`. Kaçak türü iki fiziksel imza + lojistik regresyonla simülasyonda %97 ayrıldı (küçük rezervuar darbesinde %63); "simülasyonda" diye sunulur, düzenekle doğrulanacak. Ek sağlamlık testleri `scripts/run_checks.py` (A SCe, B tank hava kaybı, C gürültü, D kalabalık gece, E seyrek veri, F pompa kalkışı) — sonuçlar summary §3. Maliyet: İSKİ Kasım 2026, 66,91 TL/m³ (aylık güncelleniyor). Test düzeneği (`docs/v1-test-rig.md`) final için yedekte.
- **Wilo gözüyle düzeltmeler (2026-11-23, kullanıcı isteğiyle):**
  - NABIZ ayrı cihaz değil, **Wilo-Monitor modülü**. Faz 1 bulutta: kalkış sayacı (reg. 40077/40081) 1 dk arayla yeter, debi/maliyet/depo önerisi (sim. %88 tespit, %5 debi hatası; çalışma biti 60 sn'de %6'ya çöküyor). Faz 2 kontrol ünitesinin yanında: kaçak türü saniyelik basınç istiyor.
  - Depo için önce **öneri modu** (yönetici onaylar); otomatik vana pilottan sonra.
  - Segment: önce SiBoost'lu siteler, sonra basınç şalterli hidroforlar (retrofit). İş modeli (varsayım): WiloCare aylık paketine modül, ödeyen site yönetim firması.
  - Wilo SiBoost SCADA ile kaçak algılama sunuyor, yöntemi yayımlanmamış: rakip tablosunda "?" ve Wilo'ya soru.
  - Ölçülen şey "kalite" değil, suyun depoda **bekleme süresi**. Pompa kalkışı göstergesi eklendi (24 L tankta 10 L/sa ≈48 fazladan kalkış/gün).
- Tanıtım sayfası: `site/` (GitHub Pages, `.github/workflows/pages.yml`).
- Demo iskeleti (final için yedek): Streamlit (`app/main.py`, `src/`), `4dbf99f`. Değişirse güncellenir.
- Veri: `data/raw/`, `data/external/`, `data/processed/` git dışında; `data/sample/` (küçük örnek veri) takip edilir.
- Git: push: origin/main, kullanıcı onayıyla. Repo private.

## Faz 0 — soru açıklanmadan önceki hazırlık (tamamlandı)
1. Klasör yapısı ve git: yapıldı.
2. `docs/datasets.md`: yapıldı.
3. `docs/idea-pool.md`, ardından `docs/idea-pool-v2.md`: yapıldı.
4. Demo iskeleti (venv, Streamlit, `src/data.py`, `src/model.py`): yapıldı (`4dbf99f`), **final için yedek.**

## Fikir seçimi
- **En ağır kriter problem-çözüm uyumu (%25).** Fikir, mülakat bulgularıyla desteklenmeden kesinleşmez.
- Özgünlük %20. Yaygın fikirler (idea-pool.md P1–P3) final değil; P1 (SKAB pompa anomali) teknik yedek.
- Aktif havuz: `docs/idea-pool-v2.md` (problemden başlayan).
- **Karar (2026-11-17):** Ana yön **V1 — hidrofor = kaçak sensörü**. V4 (kuyu pompası = akifer sensörü) sunumda "pompa zaten sensör" vizyonunun ikinci kullanım alanı. V3 yedek.
- **Değerlendirmedeki adaylar (2026-11-19):** "Taze Depo" (apartman deposunda su yaşı yönetimi) ve "V1 + Taze Depo birleşik" (binanın su yönetim beyni). Seçimi kullanıcı yapar.
- **Karar (2026-11-23):** Birleşik versiyon, adı **NABIZ**. Kullanıcı seçimi Claude'a bıraktı. Mülakat yapılmadı; ara teslim kanvası `docs/canvas-draft.md`, sunum `teslim/`.
- Sıradaki işler (her adımdan önce kullanıcı onayı): `docs/taze-depo-validation.md`, `docs/interview-guide.md`, ardından 3 mülakat → içgörüler → 8 soruluk kanvas.

## Veri ve fikir kuralları
- Fikirler yalnız `docs/datasets.md`'deki doğrulanmış kaynaklara dayanır. Login istemeyenler önce; doğrulanamamış kaynaklar (SWaT/WADI vb.) kullanılmaz.
- Wilo ürün adı yalnız ürün sayfası açılıp doğrulandıysa, linkiyle yazılır; aksi halde "genel pompa".
- Teslimde doğrulanmamış her bilgi "varsayım" olarak işaretlenir.

## Kurallar
- Kullanıcıya Türkçe yanıt ver. Kod, yorumlar ve teknik terimler İngilizce olabilir.
- Rakam, istatistik veya lisans bilgisi uydurma. Her sayının ve iddianın yanına kaynak linkini koy. Bilinmeyen yerde "bilmiyorum" yaz.
- **Başlamadan önce düşün.** Varsayımları ve belirsizlikleri açıkça yaz; birden fazla yorum varsa sor. Her adıma başlamadan önce ne yapılacağı kısaca yazılır ve kullanıcı onayı beklenir.
- **Basit tut.** İsteneni karşılayan en basit çözüm; istenmeyen özellik, soyutlama veya "ileride lazım olur" eklemesi yok. Kısa yaz, gereksiz özet yapma.
- **Sadece istenene dokun.** İstenmeyen dosya, satır veya biçim değiştirilmez. Fark edilen başka sorun düzeltilmez, yalnız raporlanır.
- **Çalıştığını kanıtla.** "Bitti" demeden önce doğrula (çıktı, test, dosya içeriği, link açılıyor mu). Doğrulanamadıysa bunu açıkça söyle.
- Önemli kararlar, kullanıcı onayladıktan sonra C:\Users\NİTRO\Desktop\Wiki'ye işlenir.
