from django.db.models.signals import post_save
from django.dispatch import receiver
import logging

from core.management.utils.signals_utils import save_metadata
from core.models import SchemaLedger, TermSet

logger = logging.getLogger('dict_config_logger')


@receiver(post_save, sender=SchemaLedger)
def create_TermSet(sender, instance, created, **kwargs):
    if created:
        schemaledger = SchemaLedger.objects.get(schema_iri=instance)

        termset = TermSet.objects.create(name=schemaledger.schema_name,
                                         version=schemaledger.version,
                                         status=schemaledger.status)
        termset.save()
        save_metadata(schemaledger.metadata, termset)

        logger.info("TermSet created")


@receiver(post_save, sender=SchemaLedger)
def update_TermSet(sender, instance, created, **kwargs):
    if not created:
        schemaledger = SchemaLedger.objects.get(schema_iri=instance)
        termset = TermSet.objects.get(iri=instance)
        termset.status = schemaledger.status
        termset.save()
        logger.info("TermSet updated")
