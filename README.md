# Django Iris Uygulaması

Iris çiçeği türünü tahmin eden Django tabanlı web uygulaması. CRUD, arama, CSV import/export, ML tahmin, REST API, ve kullanıcı yönetimi özellikleri içerir.

## Gereksinimler

- Python 3.10+
- Django 4.2+
- scikit-learn, pandas, djangorestframework

## Hızlı Başlangıç

### 1. Sanal ortam kurulması (ilk kez)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate

# Opsiyonel: tek komutla admin + writer rolü + iris verisi
# Parola için ADMIN_PASSWORD ortam değişkenini ayarlayabilirsiniz.
$env:ADMIN_PASSWORD="değiştirin"  # isteğe bağlı
python manage.py bootstrap_app
```

### 2. Sunucuyu başlatma

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

Tarayıcıda: **http://127.0.0.1:8000/**

## Modeller

### IrisSample
- `instance_id` (unique)
- `sepal_length` (float)
- `sepal_width` (float)
- `petal_length` (float)
- `petal_width` (float)
- `species` (Setosa/Versicolor/Virginica)

### Collection
- `title` (string)
- `description` (text)
- `created_at` (datetime)
- `owner_name` (string)
- `public` (boolean)
- `samples` (ManyToMany → IrisSample)

## Yönetici / Rol kurulumu

`bootstrap_app` komutu şunları yapar:
- Admin kullanıcısını oluşturur (varsayılan kullanıcı adı `admin`, e-posta `admin@example.com`).
- `ADMIN_PASSWORD` tanımlıysa parolayı buna ayarlar; aksi halde `admin` kullanılır (sonradan değiştirmeniz önerilir).
- `writer` grubunu oluşturur ve admin'i bu gruba ekler.
- scikit-learn iris verisetini `IrisSample` tablosuna yükler (mevcut kayıtları günceller).

## CSV İçe Aktar Formatı

```
instance_id,sepal_length,sepal_width,petal_length,petal_width,species
1,5.1,3.5,1.4,0.2,setosa
2,7.0,3.2,4.7,1.4,versicolor
...
```

## API Örnekleri

```bash
# Tüm iris'leri al
curl http://127.0.0.1:8000/api/iris/

# Yeni iris ekle
curl -X POST http://127.0.0.1:8000/api/iris/ \
  -H "Content-Type: application/json" \
  -d '{
    "instance_id": 100,
    "sepal_length": 5.5,
    "sepal_width": 3.0,
    "petal_length": 1.3,
    "petal_width": 0.2,
    "species": "setosa"
  }'
```

## HTML/CSS Uyumu

- ✅ HTML5 doğrulaması geçiyor
- ✅ Başlık etiketleri (h1, h2, h3)
- ✅ Liste etiketleri (ul, ol)
- ✅ Bağlantılar (relative & absolute)
- ✅ Resim etiketleri (multiple pages)
- ✅ Tablo etiketleri (list + detail pages)
- ✅ Form etiketleri (signup, iris create, CSV import)
- ✅ Div etiketleri (10+ locations) with CSS styling
- ✅ Harici CSS dosyası (15+ properties)

## Sorun Giderme

### "Permission denied" hatası
- Giriş yapın ve writer rolünde olduğunuzdan emin olun.

### CSV yükleme başarısız
- Dosya formatının doğru olduğunu kontrol edin (CSV, encoding: UTF-8).

### ML tahmin çalışmıyor
- scikit-learn yüklü mü kontrol edin: `pip install scikit-learn`
