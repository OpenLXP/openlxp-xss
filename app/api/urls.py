from api import views
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = 'api'

urlpatterns = [
     path('schemas/', views.SchemaLedgerDataView.as_view(),
          name='schemaledger'),
     path('mappings/', views.TransformationLedgerDataView.as_view(),
          name='transformationledger'),
]
