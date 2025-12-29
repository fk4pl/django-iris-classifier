import os
import csv
from io import TextIOWrapper

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from .models import IrisSample
from .forms import IrisSampleForm, CSVImportForm


def index(request):
    return render(request, 'gallery/index.html')


def iris_list(request):
    samples = IrisSample.objects.all().order_by('instance_id')
    return render(request, 'gallery/iris_list.html', {'samples': samples})


def iris_detail(request, pk):
    sample = get_object_or_404(IrisSample, pk=pk)
    return render(request, 'gallery/iris_detail.html', {'sample': sample})


@login_required
def iris_create(request):
    # Kullanıcının personel veya 'writer' (yazar) grubunda olup olmadığını kontrol et
    is_writer = request.user.groups.filter(name='writer').exists()
    if not (request.user.is_staff or is_writer):
        return HttpResponse('Permission denied', status=403)

    if request.method == 'POST':
        form = IrisSampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gallery:iris_list')
    else:
        form = IrisSampleForm()
    
    return render(request, 'gallery/iris_form.html', {'form': form, 'action': 'Create'})


@login_required
def iris_update(request, pk):
    # Kullanıcının personel veya 'writer' (yazar) grubunda olup olmadığını kontrol et
    is_writer = request.user.groups.filter(name='writer').exists()
    if not (request.user.is_staff or is_writer):
        return HttpResponse('Permission denied', status=403)

    sample = get_object_or_404(IrisSample, pk=pk)
    
    if request.method == 'POST':
        form = IrisSampleForm(request.POST, instance=sample)
        if form.is_valid():
            form.save()
            return redirect('gallery:iris_detail', pk=pk)
    else:
        form = IrisSampleForm(instance=sample)
    
    return render(request, 'gallery/iris_form.html', {'form': form, 'action': 'Edit'})


@login_required
def iris_delete(request, pk):
    # Kullanıcının personel veya 'writer' (yazar) grubunda olup olmadığını kontrol et
    is_writer = request.user.groups.filter(name='writer').exists()
    if not (request.user.is_staff or is_writer):
        return HttpResponse('Permission denied', status=403)

    sample = get_object_or_404(IrisSample, pk=pk)
    
    if request.method == 'POST':
        sample.delete()
        return redirect('gallery:iris_list')
    
    return render(request, 'gallery/iris_confirm_delete.html', {'sample': sample})


def search(request):
    results = IrisSample.objects.all()
    
    query_id = request.GET.get('instance_id')
    species = request.GET.get('species')
    min_sepal = request.GET.get('min_sepal')
    
    if query_id:
        results = results.filter(instance_id=query_id)
    
    if species:
        results = results.filter(species=species)
    
    if min_sepal:
        try:
            results = results.filter(sepal_length__gte=float(min_sepal))
        except ValueError:
            pass
            
    return render(request, 'gallery/search.html', {'results': results})


@login_required
def import_csv(request):
    # İzinleri kontrol et
    is_writer = request.user.groups.filter(name='writer').exists()
    if not (request.user.is_staff or is_writer):
        return HttpResponse('Permission denied', status=403)

    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            # Dosyayı metin modunda aç
            text_file = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.DictReader(text_file)
            
            count = 0
            for row in reader:
                try:
                    # Değerleri al veya varsayılan olarak 0 kullan
                    instance_id = int(row.get('instance_id') or row.get('id') or 0)
                    sepal_length = float(row.get('sepal_length') or row.get('sepal_length_cm') or 0)
                    sepal_width = float(row.get('sepal_width') or 0)
                    petal_length = float(row.get('petal_length') or 0)
                    petal_width = float(row.get('petal_width') or 0)
                    species = row.get('species') or row.get('label') or 'setosa'

                    IrisSample.objects.update_or_create(
                        instance_id=instance_id,
                        defaults={
                            'sepal_length': sepal_length,
                            'sepal_width': sepal_width,
                            'petal_length': petal_length,
                            'petal_width': petal_width,
                            'species': species
                        }
                    )
                    count += 1
                except Exception:
                    continue
            
            return HttpResponse(f'Imported {count} rows')
    else:
        form = CSVImportForm()
        
    return render(request, 'gallery/import_csv.html', {'form': form})


def export_csv(request):
    samples = IrisSample.objects.all()
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iris_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['instance_id', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'])
    
    for sample in samples:
        writer.writerow([
            sample.instance_id, 
            sample.sepal_length, 
            sample.sepal_width, 
            sample.petal_length, 
            sample.petal_width, 
            sample.species
        ])
        
    return response


def ml_predict(request):
    result = None
    error = None
    image_name = None
    
    if request.method == 'POST':
        try:
            # Giriş değerlerini al ve ondalıklı sayıya çevir
            sepal_length = float(request.POST.get('sepal_length') or 0)
            sepal_width = float(request.POST.get('sepal_width') or 0)
            petal_length = float(request.POST.get('petal_length') or 0)
            petal_width = float(request.POST.get('petal_width') or 0)
            algorithm = request.POST.get('algorithm')

            # Kütüphaneden yardımcı verileri yükle
            data = load_iris()
            features = list(data.data)
            labels = list(data.target)
            
            # Veritabanımızdaki verileri ekle
            db_samples = IrisSample.objects.all()
            species_map = {'setosa': 0, 'versicolor': 1, 'virginica': 2}
            
            for sample in db_samples:
                features.append([
                    sample.sepal_length, 
                    sample.sepal_width, 
                    sample.petal_length, 
                    sample.petal_width
                ])
                labels.append(species_map.get(sample.species.lower(), 0))
            
            # Model için verileri hazırla
            scaler = StandardScaler()
            features_scaled = scaler.fit_transform(features)
            
            # Sınıflandırıcıyı seç
            if algorithm == 'rf':
                classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            elif algorithm == 'lr':
                classifier = LogisticRegression(max_iter=200, random_state=42)
            else:
                classifier = KNeighborsClassifier(n_neighbors=1)

            # Modeli eğit
            classifier.fit(features_scaled, labels)
            
            # Yeni giriş için tür tahmini yap
            input_data = [[sepal_length, sepal_width, petal_length, petal_width]]
            input_scaled = scaler.transform(input_data)
            
            prediction_index = classifier.predict(input_scaled)[0]
            predicted_species = data.target_names[prediction_index]
            
            result = predicted_species
            
            # Sonuç için görseli al
            species_images = {
                'setosa': 'images/setosa.png',
                'versicolor': 'images/versicolor.png',
                'virginica': 'images/virginica.png',
            }
            image_name = species_images.get(predicted_species)
                
        except (ValueError, TypeError):
            error = 'Please enter valid decimal numbers for all measurements'
            
    return render(request, 'gallery/ml.html', {
        'result': result, 
        'error': error, 
        'image_name': image_name
    })
