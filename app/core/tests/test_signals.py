from unittest.mock import patch

from django.test import tag

from .test_setup import TestSetUp
from ..models import TermSet, SchemaLedger


@tag('unit')
class SignalTests(TestSetUp):

    def test_create_TermSet(self):
        """Function to check create postsave of schema ledger
        in termsets and terms"""

        with patch('core.signals.termset_object'):
            self.schema.save()
            termset = TermSet.objects.get(name=self.schema_name)

            self.assertEqual(termset.name, self.schema_name)
            self.assertEqual(termset.version, self.version)
            self.assertEqual(termset.status, self.status)

    def test_update_TermSet(self):
        """Function to check update postsave of schema ledger
        in termsets and terms"""

        with patch('core.signals.update_status'), \
                patch('core.signals.create_TermSet'):

            self.schema.save()

            schemaledger = \
                SchemaLedger.objects.get(schema_name=self.schema_name)
            schemaledger.status = 'retired'
            schemaledger.save()

            termset = TermSet.objects.get(name=self.schema_name)
            self.assertEqual(termset.status, 'retired')
