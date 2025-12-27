import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from gallery.models import IrisSample
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# Get all data
data = load_iris()
X = list(data.data)
y = list(data.target)

species_map = {'setosa': 0, 'versicolor': 1, 'virginica': 2}
for sample in IrisSample.objects.all():
    X.append([sample.sepal_length, sample.sepal_width, sample.petal_length, sample.petal_width])
    y.append(species_map.get(sample.species.lower(), 0))

X = np.array(X)
y = np.array(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Create KNN with n_neighbors=5 to see distances
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_scaled, y)

# Test point
test_point = np.array([[12, 12, 12, 12]])
test_scaled = scaler.transform(test_point)

# Get distances and indices of 5 nearest neighbors
distances, indices = knn.kneighbors(test_scaled)

print(f"Testing input: [12, 12, 12, 12]")
print(f"Scaled input: {test_scaled[0]}")
print(f"\nNearest 5 neighbors:")
for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):
    neighbor = X_scaled[idx]
    label = data.target_names[y[idx]]
    print(f"  {i+1}. Distance: {dist:.4f}, Label: {label}, Original: {X[idx]}")

# Final prediction with n_neighbors=1
knn1 = KNeighborsClassifier(n_neighbors=1)
knn1.fit(X_scaled, y)
pred = knn1.predict(test_scaled)[0]
print(f"\nPrediction with n_neighbors=1: {data.target_names[pred]}")
