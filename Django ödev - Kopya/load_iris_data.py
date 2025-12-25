import csv
import requests
from io import StringIO
from gallery.models import IrisSample

# UCI Iris Dataset CSV URL
url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

try:
    response = requests.get(url)
    response.encoding = 'utf-8'
    
    reader = csv.reader(StringIO(response.text))
    count = 0
    
    for idx, row in enumerate(reader, start=1):
        if len(row) < 5:
            continue
        
        try:
            # Map species names
            species_map = {
                'Iris-setosa': 'setosa',
                'Iris-versicolor': 'versicolor',
                'Iris-virginica': 'virginica',
            }
            
            species = species_map.get(row[4].strip(), 'setosa')
            
            IrisSample.objects.update_or_create(
                instance_id=idx,
                defaults={
                    'sepal_length': float(row[0]),
                    'sepal_width': float(row[1]),
                    'petal_length': float(row[2]),
                    'petal_width': float(row[3]),
                    'species': species,
                }
            )
            count += 1
        except Exception as e:
            print(f"Error at row {idx}: {e}")
            continue
    
    print(f"Loaded {count} iris samples from UCI dataset.")
    
except Exception as e:
    print(f"Error downloading dataset: {e}")
