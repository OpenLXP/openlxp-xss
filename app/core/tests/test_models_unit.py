from django.test import SimpleTestCase, tag

from core.models import SchemaLedger, TransformationLedger


@tag('unit')
class ModelTests(SimpleTestCase):

    def test_schema_ledger(self):
        """Test that creating a SchemaLedger is successful"""

        schema_name = 'test_name'
        schema_iri = 'test_iri'
        metadata = {
            'test': 'test'
        }
        status = 'published'
        version = '1.0.0'
        major_version = 1
        minor_version = 0
        patch_version = 0

        schema = SchemaLedger(schema_name=schema_name,
                              schema_iri=schema_iri,
                              metadata=metadata,
                              status=status,
                              version=version,
                              major_version=major_version,
                              minor_version=minor_version,
                              patch_version=patch_version)

        self.assertEqual(schema.schema_name, schema_name)
        self.assertEqual(schema.schema_iri, schema_iri)
        self.assertEqual(schema.status, status)
        self.assertEqual(schema.metadata, metadata)
        self.assertEqual(schema.version, version)
        self.assertEqual(schema.major_version, major_version)
        self.assertEqual(schema.minor_version, minor_version)
        self.assertEqual(schema.patch_version, patch_version)

    def test_transformation_ledger(self):
        """Test that creating a transformationLedger is successful"""

        source_schema_name = "test_source"
        target_schema_name = "test_target"
        source_schema_version = "source_version"
        target_schema_version = "source_target"
        schema_mapping = {
            "test": "test"
        }
        status = "published"

        mapping = \
            TransformationLedger(source_schema_name=source_schema_name,
                                 target_schema_name=target_schema_name,
                                 source_schema_version=source_schema_version,
                                 target_schema_version=target_schema_version,
                                 schema_mapping=schema_mapping,
                                 status=status)

        self.assertEqual(mapping.source_schema_name, source_schema_name)
        self.assertEqual(mapping.target_schema_name, target_schema_name)
        self.assertEqual(mapping.source_schema_version, source_schema_version)
        self.assertEqual(mapping.target_schema_version, target_schema_version)
        self.assertEqual(mapping.schema_mapping, schema_mapping)
        self.assertEqual(mapping.status, status)
