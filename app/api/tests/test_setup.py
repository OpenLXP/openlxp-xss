from core.models import SchemaLedger, TransformationLedger
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    """Class with setup and teardown for tests in XDS"""

    def setUp(self):
        """Function to set up necessary data for testing"""
        self.schema = SchemaLedger(schema_name="test_name",
                                   schema_iri="schema_iri",
                                   metadata="metadata",
                                   status="published",
                                   version="1.2.3")
        self.mapping = TransformationLedger(source_schema_name="sourceNm",
                                            target_schema_name="targetNm",
                                            source_schema_version="sourceVrs",
                                            target_schema_version="targetVrs",
                                            schema_mapping="mapping",
                                            status="published")
        self.schema_name = "test_name"
        self.schema_iri = "schema_iri"
        self.metadata = "metadata"
        self.status = "published"
        self.version = "1.2.3"
        self.source_schema_name = "sourceNm"
        self.target_schema_name = "targetNm"
        self.source_schema_version = "sourceVrs"
        self.target_schema_version = "targetVrs"
        self.schema_mapping = "mapping"

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
