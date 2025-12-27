from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.index, name='index'),
    path('iris/', views.iris_list, name='iris_list'),
    path('iris/add/', views.iris_create, name='iris_create'),
    path('iris/<int:pk>/', views.iris_detail, name='iris_detail'),
    path('iris/<int:pk>/edit/', views.iris_update, name='iris_update'),
    path('iris/<int:pk>/delete/', views.iris_delete, name='iris_delete'),
    path('search/', views.search, name='search'),
    path('import-csv/', views.import_csv, name='import_csv'),
    path('export-csv/', views.export_csv, name='export_csv'),
    path('ml/', views.ml_predict, name='ml_predict'),
]
