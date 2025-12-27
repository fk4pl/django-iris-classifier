# Django Iris Uygulaması

Iris çiçeği türünü tahmin eden Django tabanlı web uygulaması. CRUD, arama, CSV import/export, ML tahmin, REST API, ve kullanıcı yönetimi özellikleri içerir.

## Gereksinimler

- Python 3.10+
- Django 4.2+
- scikit-learn, pandas, djangorestframework

## Hızlı Başlangıç

### 1️⃣ Sanal ortam kurulması (ilk kez - bir defa yapılır)

Terminal/PowerShell'i açın ve proje klasörüne gidin:

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
*(PowerShell izinleri için `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` çalıştırmanız gerekebilir)*

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

### 2️⃣ Sunucuyu başlatma (her seferinde)

Sanal ortamı etkinleştirin (eğer kapattıysanız):
```powershell
.\.venv\Scripts\Activate.ps1
```

Sunucuyu başlatın:
```powershell
python manage.py runserver
```

Tarayıcıda açın: http://127.0.0.1:8000

### Roller

- **Admin**: Tüm işlemleri yapabilir
- **Writer Grubu**: Iris oluştur/sil/düzenle işlemlerini yapabilir
- **Reader Grubu**: Sadece iris verilerini görüntüleyebilir


Admin hesabı: **admin / admin**

## CSV İçe Aktar Formatı

```
instance_id,sepal_length,sepal_width,petal_length,petal_width,species
1,5.1,3.5,1.4,0.2,setosa
2,7.0,3.2,4.7,1.4,versicolor
...
```
## Sorun Giderme

### "Permission denied" hatası
- Giriş yapın ve writer rolünde olduğunuzdan emin olun.

### CSV yükleme başarısız
- Dosya formatının doğru olduğunu kontrol edin (CSV, encoding: UTF-8).

### ML tahmin çalışmıyor
- scikit-learn yüklü mü kontrol edin: `pip install scikit-learn`
