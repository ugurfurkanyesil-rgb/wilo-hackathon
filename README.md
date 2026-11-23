# Water AI Hackathon 2026 — Demo

Generic time-series demo: **load data → anomaly detection / forecast → chart** (Streamlit).
The model in `src/model.py` is a placeholder baseline; it will be adapted once the hackathon question is announced.

## Kurulum (Windows PowerShell)

Python 3.13 ile test edildi.

```powershell
cd $env:USERPROFILE\Desktop\wilo-hackathon
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

`Activate.ps1` "running scripts is disabled" hatası verirse (yalnız bir kez):

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Çalıştırma

```powershell
streamlit run app\main.py
```

Tarayıcıda `http://localhost:8501` açılır. Aktivasyon olmadan:

```powershell
.\.venv\Scripts\python.exe -m streamlit run app\main.py
```

## Örnek veriyi yeniden üretme

```powershell
python src\data.py
```

`data/sample/synthetic_pump.csv`: 14 gün, 15 dk aralıklı **sentetik** pompa verisi (`flow_m3h`, `pressure_bar`, `current_a`) ve `anomaly` etiketi (akım sıçraması, basınç düşümü, akım kayması). Gerçek ölçüm değildir.

## Kendi verinle kullanma

Sol menüden **Dosya yükle** → CSV/XLSX. Bir tarih sütunu otomatik bulunur, sayısal sütunlar seçilebilir. `anomaly` (0/1) sütunu varsa precision/recall/F1 gösterilir.

## NABIZ simülasyonu (V1 kaçak + Taze Depo)

Sonuçlar ve yorumu: [`results/summary.md`](results/summary.md). Bütün sayılar simülasyondur, gerçek ölçüm değildir.

```powershell
python scripts\run_leak.py    # gece kaçağı: 260 test koşusu, ~2 dk
python scripts\run_tank.py    # depo politikaları: 20 senaryo x 180 gün, ~30 sn
python scripts\build_site.py  # sonuç JSON'larını site/data/ altına kopyalar
```

Tanıtım sayfası `site/index.html`: kaçak simülasyonu tarayıcıda çalışır, depo sonuçları `site/data/` dosyalarından okunur. Yerelde açmak için:

```powershell
cd site
python -m http.server 8000   # sonra http://localhost:8000
```

`main` dalına `site/` değişikliği gelince `.github/workflows/pages.yml` sayfayı GitHub Pages'e yükler. Bunun için repo ayarlarında Pages kaynağının "GitHub Actions" seçilmiş olması gerekir.

```
src/sim/leak_sim.py        Bina hidroforu + basınç tankı + kaçak, Modbus benzeri 1 Hz çıktı
src/sim/leak_estimator.py  Duruş süresinden kaçak debisi (T_off ≈ ΔV / Q)
src/sim/tank_sim.py        Depo seviyesi politikaları, su yaşı, kesinti senaryosu
results/                   Grafikler, metrikler, summary.md
site/                      Tanıtım sayfası (GitHub Pages)
teslim/                    24 Kasım ara teslim sunumu ve e-posta metni
```

## Yapı

```
app/main.py      Streamlit arayüzü
src/data.py      Veri yükleme + sentetik örnek
src/model.py     Placeholder: mevsimsel profil + robust z-skor anomali, seasonal-naive tahmin
data/sample/     Takip edilen küçük örnek veri
data/raw|external|processed/   Git dışı
docs/            datasets.md, idea-pool.md
```
