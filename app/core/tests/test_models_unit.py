from django.test import SimpleTestCase, tag

from core.models import SchemaLedger


@tag('unit')
class ModelTests(SimpleTestCase):

    def test_schema_ledger(self):
        """Test that creating a SchemaLedger is successful"""
        schema_name = 'test_name'
        schema_iri = 'test_iri'
        schema_metadata = 'file.csv'
        status = 'PASS'

        schema = SchemaLedger(schema_name=schema_name,
                              schema_iri=schema_iri,
                              schema_metadata=schema_metadata,
                              status=status)

        self.assertEqual(schema.schema_name, schema_name)
        self.assertEqual(schema.schema_iri, schema_iri)
        self.assertEqual(schema.status, status)
