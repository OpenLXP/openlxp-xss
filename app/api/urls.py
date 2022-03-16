from api import views
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

app_name = 'api'

urlpatterns = [
     path('schemas/', views.schemaledger_requests,
          name='schemaledger'),
     path('mappings/', views.transformationledger_requests,
          name='transformationledger'),
]
