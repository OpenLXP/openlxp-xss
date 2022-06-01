import logging

from django.core.exceptions import ObjectDoesNotExist
from requests.exceptions import HTTPError
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from api.serializers import TermSetSerializer
from core.management.utils.xss_helper import sort_version
from core.models import TermSet

logger = logging.getLogger('dict_config_logger')


def check_status(messages, queryset):
    queryset = queryset.filter(status='published')
    if not queryset:
        message = "Error fetching record, no " \
                  "published record with required parameters"
        messages.append(message)
        logger.error(message)
        raise ObjectDoesNotExist()
    return queryset


class SchemaLedgerDataView(GenericAPIView):
    """Handles HTTP requests to the Schema Ledger"""

    queryset = TermSet.objects.all().filter(status='published')

    def get(self, request):
        """This method defines the API's to retrieve data
        from the Schema Ledger"""

        queryset = self.get_queryset()

        # all requests must provide the schema name
        messages = []
        name = request.GET.get('name')
        version = request.GET.get('version')
        iri = request.GET.get('iri')

        errorMsg = {
            "message": messages
        }

        if name:
            # look for a model with the provided name
            queryset = queryset.filter(name=name)

            if not queryset:
                messages.append("Error; no schema found with the name '" +
                                name + "'")
                errorMsg = {
                    "message": messages
                }
                return Response(errorMsg, status.HTTP_400_BAD_REQUEST)

            # if the schema name is found, filter for the version.
            # If no version is provided, we fetch the latest version
            if not version:
                queryset = [ts for ts in queryset]
                queryset = sort_version(queryset, reverse_order=True)
            else:
                queryset = queryset.filter(version=version)

            if not queryset:
                messages.append("Error; no schema found for version '" +
                                version + "'")
                errorMsg = {
                    "message": messages
                }
                return Response(errorMsg, status.HTTP_400_BAD_REQUEST)
        elif iri:
            # look for a model with the provided name
            queryset = queryset.filter(iri=iri)

            if not queryset:
                messages.append("Error; no schema found with the iri '" +
                                iri + "'")
                errorMsg = {
                    "message": messages
                }
                return Response(errorMsg, status.HTTP_400_BAD_REQUEST)
        else:
            messages.append("Error; query parameter 'name' or 'iri'"
                            " is required")
            logger.error(messages)
            return Response(errorMsg, status.HTTP_400_BAD_REQUEST)
        try:
            serializer_class = TermSetSerializer(queryset[0])
            logger.info(queryset[0])
            # only way messages gets sent is if there was
            # an error serializing or in the response process.
            messages.append(
                "Error fetching records please check the logs.")
            return Response(serializer_class.data,
                            status.HTTP_200_OK)
        except ObjectDoesNotExist:
            errorMsg = {
                "message": messages
            }
            return Response(errorMsg, status.HTTP_400_BAD_REQUEST)
        except HTTPError as http_err:
            logger.error(http_err)
            return Response(errorMsg,
                            status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as err:
            logger.error(err)
            return Response(errorMsg,
                            status.HTTP_500_INTERNAL_SERVER_ERROR)


class TransformationLedgerDataView(GenericAPIView):
    """Handles HTTP requests to the Transformation Ledger"""
    queryset = TermSet.objects.all().filter(status='published')

    def get(self, request):
        """This method defines the API's to retrieve data
        from the Transformation Ledger"""
        # all requests must provide the source and target
        # schema names and versions
        source_name = request.GET.get('sourceName')
        source_iri = request.GET.get('sourceIRI')
        target_name = request.GET.get('targetName')
        target_iri = request.GET.get('targetIRI')
        source_version = request.GET.get('sourceVersion')
        target_version = request.GET.get('targetVersion')

        messages = self._check_params(
            source_name, source_iri, target_name, target_iri)

        errorMsg = {
            "message": messages
        }

        if len(messages) == 0:
            # look for a model with the provided name

            try:
                source_qs = self._filter_by_source(
                    source_name, source_version, source_iri, messages)
                target_qs = self._filter_by_target(
                    target_name, target_version, target_iri, messages)
                mapping_dict = target_qs.first().mapped_to(source_qs.first()
                                                           .iri)
                messages.append(
                    "Error fetching records please check the logs.")
            except ObjectDoesNotExist:
                errorMsg = {
                    "message": messages
                }
                return Response(errorMsg, status.HTTP_400_BAD_REQUEST)
            except HTTPError as http_err:
                logger.error(http_err)
                return Response(errorMsg,
                                status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as err:
                logger.error(err)
                return Response(errorMsg,
                                status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(
                    {
                        'source': source_qs.first().iri,
                        'target': target_qs.first().iri,
                        'schema_mapping': mapping_dict
                    }, status.HTTP_200_OK)
        else:
            logger.error(messages)
            return Response(errorMsg, status.HTTP_400_BAD_REQUEST)

    def _check_params(self, source_name, source_iri, target_name, target_iri):
        messages = []
        if source_name == source_iri and source_name is None:
            messages.append("Error; query parameter 'sourceName' or "
                            "'sourceIRI' is required")

        if target_name == target_iri and target_name is None:
            messages.append("Error; query parameter 'targetName' or "
                            "'targetIRI' is required")
        return messages

    def _filter_by_source(self, source_name, source_version, source_iri,
                          messages):
        if source_name:
            # look for a model with the provided name
            queryset = self.get_queryset().filter(name=source_name)
            if not queryset:
                messages.append("Error; no source schema found "
                                "with the name '" + source_name + "'")
                raise ObjectDoesNotExist()

            # if the schema name is found, filter for the version.
            # If no version is provided, we fetch the latest version
            if not source_version:
                term_sets = [ts for ts in queryset]
                term_set = sort_version(term_sets, reverse_order=True)[0]
                queryset = queryset.filter(iri=term_set.iri)
            else:
                queryset = queryset.filter(version=source_version)
            if not queryset:
                messages.append(
                    "Error; no source schema found for version '" +
                    source_version + "'")
                raise ObjectDoesNotExist()
        elif source_iri:
            # look for a model with the provided iri
            queryset = self.get_queryset().filter(iri=source_iri)

            if not queryset:
                messages.append("Error; no schema found "
                                "with the iri '" + source_iri + "'")
                raise ObjectDoesNotExist()
        return queryset

    def _filter_by_target(self, target_name, target_version, target_iri,
                          messages):
        queryset = self.get_queryset()
        if target_name:
            # look for a model with the provided name
            queryset = queryset.filter(name=target_name)

            if not queryset:
                messages. \
                    append("Error; no target schema found "
                           "with the name '" + target_name + "'")
                raise ObjectDoesNotExist()

            # if the schema name is found, filter for the version.
            # If no version is provided, we fetch the latest version
            if not target_version:
                term_sets = [ts for ts in queryset]
                term_set = sort_version(term_sets, reverse_order=True)[0]
                queryset = queryset.filter(iri=term_set.iri)
            else:
                queryset = queryset.filter(version=target_version)

            if not queryset:
                messages.append(
                    "Error; no target schema found for version '" +
                    target_version + "'")
                raise ObjectDoesNotExist()

        elif target_iri:
            # look for a model with the provided name
            queryset = queryset.filter(iri=target_iri)

            if not queryset:
                messages.append("Error; no schema found "
                                "with the iri '" + target_iri + "'")
                raise ObjectDoesNotExist()
        return queryset
