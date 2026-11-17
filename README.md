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

## Yapı

```
app/main.py      Streamlit arayüzü
src/data.py      Veri yükleme + sentetik örnek
src/model.py     Placeholder: mevsimsel profil + robust z-skor anomali, seasonal-naive tahmin
data/sample/     Takip edilen küçük örnek veri
data/raw|external|processed/   Git dışı
docs/            datasets.md, idea-pool.md
```
