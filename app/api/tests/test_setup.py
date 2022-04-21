from core.models import SchemaLedger, TransformationLedger
from rest_framework.test import APITestCase


class TestSetUp(APITestCase):
    """Class with setup and teardown for tests in XDS"""

    def setUp(self):
        """Function to set up necessary data for testing"""

        self.metadata = {
            "Course": {
                "CourseProviderName": "Required",
                "DepartmentName": "Optional",
                "CourseCode": "Required",
                "CourseTitle": "Required",
                "CourseShortDescription": "Required",
                "CourseAudience": "Required",
                "CourseSectionDeliveryMode": "Optional",
                "CourseObjective": "Optional",
                "CoursePrerequisites": "Required",
                "EstimatedCompletionTime": "Optional",
                "CourseSpecialNotes": "Optional",
                "CourseAdditionalInformation": "Optional",
                "CourseURL": "Optional",
                "CourseLevel": "Optional",
                "CourseSubjectMatter": "Required",
                "CourseCareerCategory": "Optional",
                "CourseAdministratorInstruction": "Optional",
                "CourseApplicationProcess": "Optional",
                "CourseCredits": "Optional"
            }
            }

        self.sourceSchema = SchemaLedger(schema_name="test_name",
                                         schema_iri="test_name_1.2.3",
                                         metadata=self.metadata,
                                         status="published",
                                         version="1.2.3")
        self.targetSchema = SchemaLedger(schema_name="test_name_1",
                                         schema_iri="test_name_1_1.2.4",
                                         metadata=self.metadata,
                                         status="published",
                                         version="1.2.4")
        self.mapping = TransformationLedger(source_schema=self.sourceSchema,
                                            target_schema=self.targetSchema,
                                            schema_mapping="mapping",
                                            status="published")
        self.schema_name = "test_name"
        self.schema_iri = "schema_iri"
        self.status = "published"
        self.version = "1.2.3"
        self.source_schema = "sourceNm"
        self.target_schema = "targetNm"
        self.source_schema_version = "sourceVrs"
        self.target_schema_version = "targetVrs"
        self.schema_mapping = "mapping"

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
