import json
from unittest.mock import patch

from django.test import tag
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import SchemaLedger, TransformationLedger


@tag('unit')
class ViewTests(APITestCase):

    def test_schemaledger_requests_no_param(self):
        """Test that making a get request to the schema api with no query
            params returns an error"""
        url = reverse('api:schemaledger')
        response = self.client.get(url)
        responseDict = json.loads(response.content)
        expected_error = ["Error; query parameter 'name' is required"]

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(responseDict['message'], expected_error)

    def test_schemaledger_requests_no_version(self):
        """Test that making a get request to the schema api with just a schema
            name should return the latest version"""
        url = "%s?name=test" % (reverse('api:schemaledger'))

        with patch('api.views.SchemaLedger.objects') as schemaObj:
            schemaLedger = SchemaLedger(schema_name="test_name",
                                        schema_iri="schema_iri",
                                        metadata="metadata",
                                        status="published",
                                        version="1.2.3")
            schemaObj.return_value = schemaObj
            schemaObj.all.return_value = schemaObj
            schemaObj.filter.return_value = schemaObj
            schemaObj.order_by.return_value = schemaObj
            schemaObj.first.return_value = schemaLedger

            response = self.client.get(url)
            responseDict = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(responseDict["schema_name"], "test_name")

    def test_schemaledger_requests_all_params(self):
        """Test that making a get request to the schema api with just all
            query params returns a valid object"""
        url = "%s?name=test&version=1.0.0" % (reverse('api:schemaledger'))

        with patch('api.views.SchemaLedger.objects') as schemaObj:
            schemaLedger = SchemaLedger(schema_name="test_name",
                                        schema_iri="schema_iri",
                                        metadata="metadata",
                                        status="published",
                                        version="1.2.3")
            schemaObj.return_value = schemaObj
            schemaObj.all.return_value = schemaObj
            schemaObj.filter.return_value = schemaObj
            schemaObj.order_by.return_value = schemaObj
            schemaObj.first.return_value = schemaLedger

            response = self.client.get(url)
            responseDict = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(responseDict["schema_name"], "test_name")

    def test_schemaledger_requests_no_schema_found(self):
        """Test that making a get request to the schema api with just a schema
            that doesn't exist returns an error"""
        url = "%s?name=test&version=1.0.2" % (reverse('api:schemaledger'))

        with patch('api.views.SchemaLedger.objects') as schemaObj:
            schemaLedger = SchemaLedger(schema_name="test_name",
                                        schema_iri="schema_iri",
                                        metadata="metadata",
                                        status="published",
                                        version="1.2.3")
            schemaObj.return_value = schemaObj
            schemaObj.all.return_value = schemaObj
            schemaObj.filter.return_value = None
            schemaObj.order_by.return_value = schemaObj
            schemaObj.first.return_value = schemaLedger

            response = self.client.get(url)
            responseDict = json.loads(response.content)
            expected_error = ["Error; no schema found with the name 'test'"]

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(responseDict['message'], expected_error)

    def test_transformationledger_requests_no_param(self):
        """Test that making a get request to the mappings api with no query
            params returns 4 errors for each required parameter"""
        url = reverse('api:transformationledger')
        response = self.client.get(url)
        responseDict = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(responseDict['message']), 4)

    def test_transformationledger_requests_no_mapping_found(self):
        """Test that making a get request to the mappings api with all params
            fails when no transformationledger is found"""
        url = ("%s?sourceName=test&sourceVersion=1.0.2&targetName=test2&" +
               "targetVersion=1.0.0") % (reverse('api:transformationledger'))

        with patch('api.views.TransformationLedger.objects') as mappingObj:
            mappingObj.return_value = mappingObj
            mappingObj.all.return_value = mappingObj
            mappingObj.filter.return_value = None

            response = self.client.get(url)

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transformationledger_requests_all_params(self):
        """Test that making a get request to the mappings api with all params
            is returns transformationledger when it exists"""
        url = ("%s?sourceName=test&sourceVersion=1.0.2&targetName=test2&" +
               "targetVersion=1.0.0") % (reverse('api:transformationledger'))

        with patch('api.views.TransformationLedger.objects') as mappingObj:
            transformationLedger = \
                TransformationLedger(source_schema_name="sourceNm",
                                     target_schema_name="targetNm",
                                     source_schema_version="sourceVrs",
                                     target_schema_version="targetVrs",
                                     schema_mapping="mapping",
                                     status="published")
            mappingObj.return_value = mappingObj
            mappingObj.all.return_value = mappingObj
            mappingObj.filter.return_value = mappingObj
            mappingObj.first.return_value = transformationLedger

            response = self.client.get(url)
            responseDict = json.loads(response.content)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(responseDict["source_schema_name"], "sourceNm")
