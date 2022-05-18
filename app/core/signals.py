import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.management.utils.signals_utils import (termset_map, termset_object,
                                                 update_status)
from core.models import SchemaLedger, TermSet, TransformationLedger

logger = logging.getLogger('dict_config_logger')


@receiver(post_save, sender=SchemaLedger)
def create_term_set(sender, instance, created, **kwargs):
    if created:
        schemaledger = SchemaLedger.objects.get(schema_iri=instance)

        termset = TermSet.objects.create(name=schemaledger.schema_name,
                                         version=schemaledger.version,
                                         status=schemaledger.status,
                                         updated_by=schemaledger.updated_by)
        termset.save()
        termset_object(schemaledger.metadata, termset, schemaledger.status,
                       schemaledger.updated_by)

        logger.info("TermSet created")


@receiver(post_save, sender=SchemaLedger)
def update_term_set(sender, instance, created, **kwargs):
    if not created:
        schemaledger = SchemaLedger.objects.get(schema_iri=instance)
        termset = TermSet.objects.get(iri=instance)
        termset.status = schemaledger.status
        termset.updated_by = schemaledger.updated_by
        termset.save()

        update_status(termset, termset.status, termset.updated_by)
        logger.info("TermSet updated")


@receiver(post_save, sender=TransformationLedger)
def map_term_sets(sender, instance, created, **kwargs):
    if created:
        target = instance.target_schema
        source = instance.source_schema

        termset_map(target, source, instance.schema_mapping)

        logger.info("Term Sets mapped")
