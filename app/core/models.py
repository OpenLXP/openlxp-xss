from django.db import models
from model_utils.models import TimeStampedModel


class SchemaLedger(TimeStampedModel):
    """Model for Uploaded Schemas"""
    schema_name = models.CharField(max_length=255)
    schema_iri = models.CharField(max_length=255)
    schema_metadata = models.FileField(upload_to='schemas/')
    status = models.CharField(max_length=50)
