import logging

from api.serializers import (SchemaLedgerSerializer,
                             TransformationLedgerSerializer)
from core.models import SchemaLedger, TransformationLedger
from requests.exceptions import HTTPError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger('dict_config_logger')


@api_view(['GET'])
def schemaledger_requests(request):
    """Handles fetching and returning requested schemas"""
    # all requests must provide the schema name
    messages = []
    name = request.GET.get('name')
    version = request.GET.get('version')
    errorMsg = {
        "message": messages
    }

    if not name:
        messages.append("Error; query parameter 'name' is required")

    if len(messages) == 0:
        # look for a model with the provided name
        querySet = SchemaLedger.objects.all()\
            .filter(schema_name=name)

        if not querySet:
            messages.append("Error; no schema found with the name '" +
                            name + "'")
            errorMsg = {
                "message": messages
            }
            return Response(errorMsg, status.HTTP_400_BAD_REQUEST)

        # if the schema name is found, filter for the version. If no version is
        # provided, we fetch the latest version
        if not version:
            querySet = querySet.order_by('-major_version', '-minor_version',
                                         '-patch_version')
        else:
            querySet = querySet.filter(version=version)

        if not querySet:
            messages.append("Error; no schema found for version '" +
                            version + "'")
            errorMsg = {
                "message": messages
            }
            return Response(errorMsg, status.HTTP_400_BAD_REQUEST)

        try:
            serializer_class = SchemaLedgerSerializer(querySet.first())
            logger.info(querySet.first().metadata)
            # only way messages gets sent is if there was an error serializing
            # or in the response process.
            messages.append("Error fetching records please check the logs.")
        except HTTPError as http_err:
            logger.error(http_err)
            return Response(errorMsg, status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as err:
            logger.error(err)
            return Response(errorMsg, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer_class.data, status.HTTP_200_OK)
    else:
        logger.error(messages)
        return Response(errorMsg, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def transformationledger_requests(request):
    """Handles fetching and returning requested schema mappings"""
    # all requests must provide the source and target schema names and versions
    messages = []
    source_name = request.GET.get('sourceName')
    target_name = request.GET.get('targetName')
    source_version = request.GET.get('sourceVersion')
    target_version = request.GET.get('targetVersion')
    errorMsg = {
        "message": messages
    }

    if not source_name:
        messages.append("Error; query parameter 'sourceName' is required")

    if not source_version:
        messages.append("Error; query parameter 'sourceVersion' is required")

    if not target_name:
        messages.append("Error; query parameter 'targetName' is required")

    if not target_version:
        messages.append("Error; query parameter 'targetVersion' is required")

    if len(messages) == 0:
        # look for a model with the provided name
        querySet = TransformationLedger.objects.all()\
            .filter(source_schema_name=source_name,
                    target_schema_name=target_name,
                    source_schema_version=source_version,
                    target_schema_version=target_version)

        if not querySet:
            messages.append("Error; no schema mapping found with the "
                            "sourceName '" + source_name + "', targetName '" +
                            target_name + "', sourceVersion '" +
                            source_version + "', targetVersion '" +
                            target_version + "'.")
            errorMsg = {
                "message": messages
            }
            return Response(errorMsg, status.HTTP_400_BAD_REQUEST)

        try:
            serializer_class = TransformationLedgerSerializer(querySet.first())
            messages.append("Error fetching records please check the logs.")
        except HTTPError as http_err:
            logger.error(http_err)
            return Response(errorMsg, status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as err:
            logger.error(err)
            return Response(errorMsg, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer_class.data, status.HTTP_200_OK)
    else:
        logger.error(messages)
        return Response(errorMsg, status.HTTP_400_BAD_REQUEST)
