#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from sklearn.datasets import load_iris
from gallery.models import IrisSample

print("Loading Iris dataset from scikit-learn...")

data = load_iris()
X = data.data  # Features
y = data.target  # Labels (0=setosa, 1=versicolor, 2=virginica)
target_names = data.target_names

species_map = {
    0: 'setosa',
    1: 'versicolor',
    2: 'virginica',
}

count = 0
for idx, (features, label) in enumerate(zip(X, y), start=1):
    try:
        IrisSample.objects.update_or_create(
            instance_id=idx,
            defaults={
                'sepal_length': float(features[0]),
                'sepal_width': float(features[1]),
                'petal_length': float(features[2]),
                'petal_width': float(features[3]),
                'species': species_map[label],
            }
        )
        count += 1
    except Exception as e:
        pass

print(f"✓ SUCCESS: Loaded {count} iris samples!")
