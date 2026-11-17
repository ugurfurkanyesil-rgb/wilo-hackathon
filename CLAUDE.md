# Water AI Hackathon 2026 — Proje Rehberi

## Bağlam
Water AI Hackathon 2026'ya katılıyorum (Wilo Türkiye x imece). Bu klasör proje klasörüm.

### Takvim
- 17 ve 19 Kasım: online bootcamp. Hackathon sorusu ve teslim formatı 19 Kasım akşamı açıklanacak.
- 19–22 Kasım: takım çalışması. Ara teslim 22 Kasım Pazar 23:59.
- 30 Kasım: 10 finalist açıklanacak.
- 5 Aralık: İstanbul'da final. Sunum Türkçe.
- Yapay zeka araçlarında kısıtlama yok.

### Wilo hakkında bildiklerimiz
- Pompa üreticisi. Alanları: Bina Teknolojileri, OEM, Su Yönetimi, Sanayi.
- Stratejisi: "Pioneering WATER AI for You" (Creating / Caring / Connecting).
- Bootcamp'te gösterilen su değer zinciri: Su Temini → İçme Suyu Arıtımı → Dağıtım/Basınçlandırma → Atıksu Transferi → Atıksu Arıtımı → Sulama/Yeniden Kullanım. Ayrıca Taşkın Önleme.

### Profil
3. sınıf Elektrik-Elektronik Mühendisliği öğrencisi. Gömülü sistemler, sensörler, C/C++ ve Python biliyor.

## Teknik kararlar
- Demo: Streamlit (`app/`). Değişirse güncellenir.
- Veri: `data/raw/`, `data/external/`, `data/processed/` git dışında; `data/sample/` (küçük örnek veri) takip edilir.
- Git: yalnız yerel. Remote/push yok (kullanıcı aksini söyleyene kadar).

## Faz 0 — soru açıklanmadan önceki hazırlık
Her adıma başlamadan önce ne yapılacağı kısaca yazılır ve kullanıcı onayı beklenir.

1. Klasör yapısı ve git: CLAUDE.md, docs/, data/, notebooks/, src/, app/, .gitignore, git init.
2. `docs/datasets.md`: su değer zinciri halkalarına uygun açık veri setleri ve simülasyon araçları (EPANET, WNTR, LeakDB, BattLeDIM, Kaggle pompa sensör verileri ve ötesi). Her kaynak için: link, lisans, boyut, içerik (sensörler, etiketler), ilgili halka, indirme yolu. Yalnız açılıp doğrulanan kaynaklar listeye; doğrulanamayanlar ayrı "doğrulanamadı" bölümüne.
3. `docs/idea-pool.md`: her halka için 1–2 fikir. Her fikirde: problem, veri (datasets.md referansı), AI yöntemi, Wilo ürün/pompa bağlantısı, ölçülebilir başarı metriği, 3 günde demo yapılabilirlik puanı (1–5) ve gerekçesi. Sonda en güçlü 3 fikir için karşılaştırma tablosu.
4. Demo iskeleti: Python venv, requirements.txt, `app/main.py` (Streamlit), `src/data.py` (veri yükleme), `src/model.py` (placeholder model). Örnek veriyle uçtan uca: veri yükle → model çalıştır → grafikte göster. README.md'de Windows PowerShell için kurulum/çalıştırma komutları.
   - Kullanıcı idea-pool'dan fikir seçmeden başlanmaz.
   - İskelet seçilen fikre özel olmaz: genel zaman serisi akışı (veri yükle → anomali/tahmin → grafik). Soru 19 Kasım'da gelince uyarlanır.

## Veri ve fikir kuralları
- Fikirler yalnız `docs/datasets.md`'deki doğrulanmış kaynaklara dayanır. Login istemeyenler önce; doğrulanamamış kaynaklar (SWaT/WADI vb.) kullanılmaz.
- Wilo ürün adı yalnız ürün sayfası açılıp doğrulandıysa, linkiyle yazılır; aksi halde "genel pompa".

## Kurallar
- Kullanıcıya Türkçe yanıt ver. Kod, yorumlar ve teknik terimler İngilizce olabilir.
- Rakam, istatistik veya lisans bilgisi uydurma. Her sayının ve iddianın yanına kaynak linkini koy. Bilinmeyen yerde "bilmiyorum" yaz.
- Kısa yaz, gereksiz özet yapma.
- Önemli kararlar, kullanıcı onayladıktan sonra C:\Users\NİTRO\Desktop\Wiki'ye işlenir.
