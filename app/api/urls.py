from django.urls import path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

app_name = 'api'

urlpatterns = [
     path('schemaledger/', views.schemaledger_requests,
         name='schemaledger'),
     path('transformationledger/', views.transformationledger_requests,
         name='transformationledger'),
]
