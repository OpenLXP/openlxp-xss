import json
import logging

from django.db import models
from model_utils.models import TimeStampedModel

logger = logging.getLogger('dict_config_logger')


class SchemaLedger(TimeStampedModel):
    """Model for Uploaded Schemas"""
    SCHEMA_STATUS_CHOICES = [('published', 'published'),
                             ('retired', 'retired')]

    schema_name = models.CharField(max_length=255)
    schema_iri = models.CharField(max_length=255)
    schema_file = models.FileField(upload_to='schemas/',
                                   null=True,
                                   blank=True)
    status = models.CharField(max_length=10,
                              choices=SCHEMA_STATUS_CHOICES)
    metadata = models.JSONField(blank=True,
                                help_text="auto populated from uploaded file")
    version = models.CharField(max_length=6,
                               help_text="auto populated from other version "
                                         "fields")
    major_version = models.SmallIntegerField()
    minor_version = models.SmallIntegerField()
    patch_version = models.SmallIntegerField()

    def clean(self):
        # store the contents of the file in the metadata field
        if self.schema_file:
            json_file = self.schema_file
            json_obj = json.load(json_file)  # deserialises it

            self.metadata = json_obj
            json_file.close()
            self.schema_file = None

        # combine the versions
        version = str(self.major_version) + '.' + str(self.minor_version) \
            + '.' + str(self.patch_version)
        self.version = version


class TransformationLedger(TimeStampedModel):
    """Model for Uploaded schema transformation mappings"""
    SCHEMA_STATUS_CHOICES = [('published', 'published'),
                             ('retired', 'retired')]

    source_schema_name = models.CharField(max_length=255)
    target_schema_name = models.CharField(max_length=255)
    source_schema_version = \
        models.CharField(max_length=6,
                         help_text="version of the source schema")
    target_schema_version = \
        models.CharField(max_length=6,
                         help_text="version of the target schema")
    schema_mapping_file = models.FileField(upload_to='schemas/',
                                           null=True,
                                           blank=True)
    schema_mapping = \
        models.JSONField(blank=True,
                         help_text="auto populated from uploaded file")
    status = models.CharField(max_length=10,
                              choices=SCHEMA_STATUS_CHOICES)

    def clean(self):
        # store the contents of the file in the schema_mapping field
        if self.schema_mapping_file:
            json_file = self.schema_mapping_file
            json_obj = json.load(json_file)  # deserialises it

            self.schema_mapping = json_obj
            json_file.close()
            self.schema_mapping_file = None
