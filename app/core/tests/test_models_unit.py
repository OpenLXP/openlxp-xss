from django.core.exceptions import ValidationError
from django.test import tag

from core.models import (ChildTermSet, SchemaLedger, Term, TermSet,
                         TransformationLedger, validate_version)

from .test_setup import TestSetUp


@tag('unit')
class ModelTests(TestSetUp):

    def test_schema_ledger(self):
        """Test that creating a SchemaLedger is successful"""

        schema_name = 'test_name'
        schema_iri = 'test_iri'
        metadata = {
            'test': 'test'
        }
        status = 'published'
        version = '1.0.1'
        major_version = 1
        minor_version = 0
        patch_version = 1

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

        source_schema_name = self.schema
        target_schema_name = self.schema
        schema_mapping = {
            "test": "test"
        }
        status = "published"

        mapping = \
            TransformationLedger(source_schema=source_schema_name,
                                 target_schema=target_schema_name,
                                 schema_mapping=schema_mapping,
                                 status=status)

        mapping.save()

        self.assertEqual(mapping.source_schema, source_schema_name)
        self.assertEqual(mapping.target_schema, target_schema_name)
        self.assertEqual(mapping.schema_mapping, schema_mapping)
        self.assertEqual(mapping.status, status)

    def test_term_set(self):
        """Test that creating a TermSet is successful"""
        ts_name = "test_name"
        ts_version = "0.0.1"
        ts_status = TermSet.STATUS_CHOICES[0][0]

        expected_iri = "xss:" + ts_version + "@" + ts_name

        ts = TermSet(name=ts_name, version=ts_version, status=ts_status)

        ts.save()

        self.assertEquals(ts.iri, expected_iri)
        self.assertEquals(ts.name, ts_name)
        self.assertEquals(ts.version, ts_version)
        self.assertEquals(ts.status, ts_status)

    def test_child_term_set(self):
        """Test that creating a ChildTermSet is successful"""
        cts_name = "test_name"
        cts_status = TermSet.STATUS_CHOICES[0][0]
        cts_parent = self.ts

        expected_iri = "xss:" + cts_parent.version + \
            "@" + cts_parent.name + "/" + cts_name

        cts = ChildTermSet(name=cts_name, status=cts_status,
                           parent_term_set=cts_parent)

        cts.save()

        self.assertEquals(cts.iri, expected_iri)
        self.assertEquals(cts.name, cts_name)
        self.assertEquals(cts.version, cts_parent.version)
        self.assertEquals(cts.status, cts_status)

    def test_term(self):
        """Test that creating a Term is successful"""
        t_name = "test_name"
        t_description = "test description"
        t_data_type = "string"
        t_use = Term.USE_CHOICES[0][0]
        t_source = "source"
        t_ts = self.ts
        t_status = "published"

        expected_iri = "xss:" + t_ts.version + "@" + t_ts.name + "?" + t_name

        term = Term(name=t_name, description=t_description,
                    data_type=t_data_type, use=t_use,
                    source=t_source, term_set=t_ts, status=t_status)

        term.save()

        self.assertEquals(term.iri, expected_iri)
        self.assertEquals(term.name, t_name)
        self.assertEquals(term.data_type, t_data_type)
        self.assertEquals(term.use, t_use)
        self.assertEquals(term.source, t_source)
        self.assertEquals(term.term_set, t_ts)
        self.assertEquals(term.status, t_status)

    def test_validate_version_pass(self):
        """Test that validate version passes correct formats"""
        validate_version("0.0.1")
        self.assertTrue(True)

    def test_validate_version_fail(self):
        """Test that validate version fails bad formats"""
        self.assertRaises(ValidationError, validate_version, "0.0..1")
