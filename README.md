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
python manage.py createsuperuser  # Admin kullanıcı oluştur
```

### 2. Sunucuyu başlatma

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

Tarayıcıda: **http://127.0.0.1:8000/**

## Ana Özellikler

### ✅ Tamamlanan Gereksinimler (100 puan)

| # | Kriter | Puan | Durum |
|---|--------|------|-------|
| 1 | Main Data Model (IrisSample + Collection, 5+ field) | 10 | ✅ |
| 2 | Relational Data Model (ManyToMany) | 10 | ✅ |
| 3 | CRUD Pages (list/detail/create/update/delete) | 15 | ✅ |
| 4 | Django Template Language | 10 | ✅ |
| 5 | User Authentication (register/login/logout/password reset) | 10 | ✅ |
| 6 | User Authorization (writer/reader roles) | 10 | ✅ |
| 7 | Search (3+ fields, multi-criteria) | 10 | ✅ |
| 8 | Import/Export CSV | 10 | ✅ |
| 9 | HTML/CSS Requirements | 10 | ✅ |
| 10 | Admin Interface | 5 | ✅ |

### 🎁 Bonus Özellikler (20 puan)

| # | Kriter | Puan | Durum |
|---|--------|------|-------|
| A | REST API (Django REST Framework) | 13 | ✅ |
| B | ML Prediction (3 algoritma: LR, KNN, RF) | 7 | ✅ |

## URL Haritası

| URL | Açıklama | Giriş Gerekli |
|-----|----------|---------------|
| `/` | Ana galeri sayfası | Hayır |
| `/iris/` | Iris örnekleri listesi | Hayır |
| `/iris/<id>/` | Iris detayı | Hayır |
| `/iris/add/` | Yeni iris ekle | **Evet (writer)** |
| `/iris/<id>/edit/` | Iris güncelle | **Evet (writer)** |
| `/iris/<id>/delete/` | Iris sil | **Evet (writer)** |
| `/search/` | Ara (3 alan: ID, tür, sepal length) | Hayır |
| `/import-csv/` | CSV yükle | **Evet** |
| `/export-csv/` | CSV indir | Hayır |
| `/ml/` | ML tahmin | Hayır |
| `/accounts/login/` | Giriş | Hayır |
| `/accounts/signup/` | Kayıt | Hayır |
| `/accounts/password-reset/` | Parola değiştir | **Evet** |
| `/admin/` | Django Admin | **Evet (admin)** |
| `/api/iris/` | REST API | Hayır |

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

## Test Kullanıcıları

Aşağıdaki test kullanıcıları önceden oluşturulmuştur:

```
Kullanıcı: admin | Şifre: admin | Rol: Superuser
Kullanıcı: writer1 | Şifre: pass | Rol: Writer
Kullanıcı: reader1 | Şifre: pass | Rol: Reader
```

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

## Geliştirici Notları

Proje şu anda geliştirme modundadır. İçeri dağıtım için:
- `SECRET_KEY` değiştirin
- `DEBUG = False` yapın
- `ALLOWED_HOSTS` güncellen
- Üretim veritabanı yapılandır (SQLite yerine PostgreSQL vb.)
