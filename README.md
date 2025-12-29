# Django Iris Uygulaması

Iris çiçeği türünü tahmin eden Django tabanlı web uygulaması. CRUD, arama, CSV import/export, ML tahmin, REST API, ve kullanıcı yönetimi özellikleri içerir.

### 1. Sanal ortam kurulması

```powershell
cd C:\Users\YourUsername\Desktop\django-iris-classifier-main
```

Sanal ortam oluşturun:
```powershell
python -m venv .venv
```

Sanal ortamı etkinleştirin:
```powershell
.\.venv\Scripts\Activate.ps1
```

Gerekli paketleri yükleyin:
```powershell
pip install -r requirements.txt
```

Veritabanını kurun:
```powershell
python manage.py migrate
```

Iris örnek verilerini yükleyin:
```powershell
python manage.py bootstrap_app
```

### 2. Sunucuyu başlatma (her seferinde)

Sanal ortamı etkinleştirin (eğer kapattıysanız):
```powershell
.\.venv\Scripts\Activate.ps1
```

Sunucuyu başlatın:
```powershell
python manage.py runserver
```

## Roller

- **Admin**: Tüm işlemleri yapabilir
- **Writer Grubu**: Iris oluştur/sil/düzenle işlemlerini yapabilir
- **Reader Grubu**: Sadece iris verilerini görüntüleyebilir


Admin hesabı: isim: admin şifre: admin

## CSV Import Formatı

```
instance_id,sepal_length,sepal_width,petal_length,petal_width,species
```
