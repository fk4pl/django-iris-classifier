import os
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import IrisSample
from .forms import IrisSampleForm, CSVImportForm
import csv
from io import TextIOWrapper

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier



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
    if not (request.user.is_staff or request.user.groups.filter(name='writer').exists()):
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
    if not (request.user.is_staff or request.user.groups.filter(name='writer').exists()):
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
    if not (request.user.is_staff or request.user.groups.filter(name='writer').exists()):
        return HttpResponse('Permission denied', status=403)
    sample = get_object_or_404(IrisSample, pk=pk)
    if request.method == 'POST':
        sample.delete()
        return redirect('gallery:iris_list')
    return render(request, 'gallery/iris_confirm_delete.html', {'sample': sample})


def search(request):
    qs = IrisSample.objects.all()
    q_id = request.GET.get('instance_id')
    species = request.GET.get('species')
    min_sepal = request.GET.get('min_sepal')
    if q_id:
        qs = qs.filter(instance_id=q_id)
    if species:
        qs = qs.filter(species=species)
    if min_sepal:
        try:
            qs = qs.filter(sepal_length__gte=float(min_sepal))
        except ValueError:
            pass
    return render(request, 'gallery/search.html', {'results': qs})


@login_required
def import_csv(request):
    if not (request.user.is_staff or request.user.groups.filter(name='writer').exists()):
        return HttpResponse('Permission denied', status=403)
    if request.method == 'POST':
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            f = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                try:
                    IrisSample.objects.update_or_create(
                        instance_id=int(row.get('instance_id') or row.get('id') or 0),
                        defaults={
                            'sepal_length': float(row.get('sepal_length') or row.get('sepal_length_cm') or 0),
                            'sepal_width': float(row.get('sepal_width') or 0),
                            'petal_length': float(row.get('petal_length') or 0),
                            'petal_width': float(row.get('petal_width') or 0),
                            'species': row.get('species') or row.get('label') or 'setosa'
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
    qs = IrisSample.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="iris_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['instance_id', 'sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species'])
    for s in qs:
        writer.writerow([s.instance_id, s.sepal_length, s.sepal_width, s.petal_length, s.petal_width, s.species])
    return response


def ml_predict(request):
    result = None
    error = None
    image_name = None
    if request.method == 'POST':
        try:
            sl = float(request.POST.get('sepal_length') or 0)
            sw = float(request.POST.get('sepal_width') or 0)
            pl = float(request.POST.get('petal_length') or 0)
            pw = float(request.POST.get('petal_width') or 0)
            algo = request.POST.get('algorithm')

            # Combine sklearn iris data with database IrisSample data
            data = load_iris()
            X = list(data.data)
            y = list(data.target)
            
            # Add database samples
            db_samples = IrisSample.objects.all()
            species_map = {'setosa': 0, 'versicolor': 1, 'virginica': 2}
            for sample in db_samples:
                X.append([sample.sepal_length, sample.sepal_width, sample.petal_length, sample.petal_width])
                y.append(species_map.get(sample.species.lower(), 0))
            
            # Scale features for better model performance
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Select algorithm
            if algo == 'rf':
                clf = RandomForestClassifier(n_estimators=100, random_state=42)
            elif algo == 'lr':
                clf = LogisticRegression(max_iter=200, random_state=42)
            else:
                # Default to KNN
                clf = KNeighborsClassifier(n_neighbors=1)

            clf.fit(X_scaled, y)
            
            # Scale input prediction as well
            test_input_scaled = scaler.transform([[sl, sw, pl, pw]])
            pred = clf.predict(test_input_scaled)[0]
            species = data.target_names[pred]
            result = species
            image_lookup = {
                'setosa': 'images/setosa.png',
                'versicolor': 'images/versicolor.png',
                'virginica': 'images/virginica.png',
            }
            image_name = image_lookup.get(species)
        except (ValueError, TypeError):
            error = 'Please enter valid decimal numbers for all measurements'
    return render(request, 'gallery/ml.html', {'result': result, 'error': error, 'image_name': image_name})

