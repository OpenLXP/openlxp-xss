import json
import logging
import re

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from model_utils.models import TimeStampedModel

from django.db.models.signals import post_save

logger = logging.getLogger('dict_config_logger')


def validate_version(value):
    check = re.fullmatch('[0-9]*[.][0-9]*[.][0-9]*', value)
    if check is None:
        raise ValidationError(
            '%(value)s does not match the format 0.0.0',
            params={'value': value},
        )


class TermSet(TimeStampedModel):
    """Model for Termsets"""
    STATUS_CHOICES = [('published', 'published'),
                      ('retired', 'retired')]
    iri = models.SlugField(max_length=255, unique=True,
                           allow_unicode=True, primary_key=True)
    name = models.SlugField(max_length=255, allow_unicode=True)
    version = models.CharField(max_length=255, validators=[validate_version])
    status = models.CharField(max_length=255, choices=STATUS_CHOICES)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        """Generate iri for item"""
        self.iri = self.name + '-' + self.version
        update_fields = kwargs.get('update_fields', None)
        if update_fields:
            kwargs['update_fields'] = set(update_fields).union({'iri'})

        super().save(*args, **kwargs)


class ChildTermSet(TermSet):
    """Model for Child Termsets"""
    parent_term_set = models.ForeignKey(
        TermSet, on_delete=models.CASCADE, related_name='children')

    def save(self, *args, **kwargs):
        """Generate iri for item"""
        self.iri = self.parent_term_set.iri + '-' + self.name
        self.version = self.parent_term_set.version
        update_fields = kwargs.get('update_fields', None)
        if update_fields:
            kwargs['update_fields'] = set(
                update_fields).union({'iri', 'version'})

        super(TermSet, self).save(*args, **kwargs)


class Term(TimeStampedModel):
    """Model for Terms"""
    TYPE_CHOICES = [('required', 'required'),
                    ('optional', 'optional')]
    name = models.SlugField(max_length=255, allow_unicode=True)
    description = models.TextField()
    iri = models.SlugField(max_length=255, unique=True,
                           allow_unicode=True, primary_key=True)
    data_type = models.CharField(max_length=255)
    use = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    source = models.CharField(max_length=255)
    term_set = models.ForeignKey(
        TermSet, on_delete=models.CASCADE, related_name='terms')
    mapping = models.ManyToManyField('self', blank=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        """Generate iri for item"""
        self.iri = self.term_set.iri + '-' + self.name
        update_fields = kwargs.get('update_fields', None)
        if update_fields:
            kwargs['update_fields'] = set(update_fields).union({'iri'})

        super().save(*args, **kwargs)


class SchemaLedger(TimeStampedModel):
    """Model for Uploaded Schemas"""
    SCHEMA_STATUS_CHOICES = [('published', 'published'),
                             ('retired', 'retired')]

    schema_name = models.CharField(max_length=255)
    schema_iri = models.SlugField(max_length=255, unique=True,
                                  allow_unicode=True)
    schema_file = models.FileField(upload_to='schemas/',
                                   null=True,
                                   blank=True)
    term_set = models.OneToOneField(
        TermSet, on_delete=models.CASCADE, related_name='schema', null=True,
        blank=True)
    status = models.CharField(max_length=255,
                              choices=SCHEMA_STATUS_CHOICES)
    metadata = models.JSONField(blank=True,
                                help_text="auto populated from uploaded file")
    version = models.CharField(max_length=255,
                               help_text="auto populated from other version "
                                         "fields")
    major_version = models.SmallIntegerField(default=0)
    minor_version = models.SmallIntegerField(default=0)
    patch_version = models.SmallIntegerField(default=0)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        # can't save 2 schemas with the same name for the same version
        constraints = [
            models.UniqueConstraint(fields=['schema_name', 'version'],
                                    name='unique_schema')
        ]

    def __str__(self):
        return str(self.term_set)

    def clean(self):
        # store the contents of the file in the metadata field
        if self.schema_file:
            json_file = self.schema_file
            json_obj = json.load(json_file)  # deserializes it

            self.metadata = json_obj
            json_file.close()
            self.schema_file = None

        # combine the versions
        version = \
            str(self.major_version) + '.' + str(self.minor_version) \
            + '.' + str(self.patch_version)
        self.version = version

    def save(self, *args, **kwargs):
        """Generate iri for item"""
        self.schema_iri = self.schema_name + '-' + self.version
        update_fields = kwargs.get('update_fields', None)
        if update_fields:
            kwargs['update_fields'] = set(update_fields).union({'iri'})

        super().save(*args, **kwargs)


def create_TermSet(sender, instance, created, **kwargs):
    if created:
        TermSet.objects.create(term_set=instance)
        logger.info("TermSet created")


# post_save.connect(create_TermSet, sender=SchemaLedger)


def update_TermSet(sender, instance, created, **kwargs):
    if not created:
        instance.TermSet.save()
        logger.info("TermSet updated")


# post_save.connect(update_TermSet, sender=SchemaLedger)


class TransformationLedger(TimeStampedModel):
    """Model for Uploaded schema transformation mappings"""
    SCHEMA_STATUS_CHOICES = [('published', 'published'),
                             ('retired', 'retired')]

    source_schema = models.ForeignKey(SchemaLedger,
                                      on_delete=models.CASCADE,
                                      related_name='source_mapping')
    # source_schema_name = models.CharField(max_length=255)
    # source_schema_version = \
    #     models.CharField(max_length=6,
    #                      help_text="version of the source schema")
    target_schema = models.ForeignKey(SchemaLedger,
                                      on_delete=models.CASCADE,
                                      related_name='target_mapping')
    # target_schema_name = models.CharField(max_length=255)
    # target_schema_version = \
    #     models.CharField(max_length=255,
    #                      help_text="version of the target schema")
    schema_mapping_file = models.FileField(upload_to='schemas/',
                                           null=True,
                                           blank=True)
    schema_mapping = \
        models.JSONField(blank=True,
                         help_text="auto populated from uploaded file")
    status = models.CharField(max_length=255,
                              choices=SCHEMA_STATUS_CHOICES)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def clean(self):
        # store the contents of the file in the schema_mapping field
        if self.schema_mapping_file:
            json_file = self.schema_mapping_file
            json_obj = json.load(json_file)  # deserialises it

            self.schema_mapping = json_obj
            json_file.close()
            self.schema_mapping_file = None

        if self.source_schema:
            self.source_schema_name = self.source_schema.schema_name
            self.source_schema_version = self.source_schema.version

        if self.target_schema:
            self.target_schema_name = self.target_schema.schema_name
            self.target_schema_version = self.target_schema.version