import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.management.utils.signals_utils import termset_object, update_status
from core.models import SchemaLedger, TermSet

logger = logging.getLogger('dict_config_logger')


@receiver(post_save, sender=SchemaLedger)
def create_term_set(sender, instance, created, **kwargs):
    if created:
        termset = TermSet.objects.create(name=instance.schema_name,
                                         version=instance.version,
                                         status=instance.status,
                                         updated_by=instance.updated_by)
        termset.save()

        termset_object(instance.metadata, termset, instance.status,
                       instance.updated_by)

        logger.info("TermSet created")


@receiver(post_save, sender=SchemaLedger)
def update_term_set(sender, instance, created, **kwargs):
    if not created:
        termset = TermSet.objects.get(iri=instance)
        termset.status = instance.status
        termset.updated_by = instance.updated_by
        termset.save()

        update_status(termset, termset.status, termset.updated_by)
        logger.info("TermSet updated")


@receiver(post_save, sender=TermSet)
def update_schema_ledger(sender, instance, created, **kwargs):
    if not created:
        SchemaLedger.objects.filter(schema_iri=instance.iri). \
            update(status=instance.status,
                   updated_by=instance.updated_by)

        update_status(instance, instance.status, instance.updated_by)
        logger.info("SchemaLedger updated")
