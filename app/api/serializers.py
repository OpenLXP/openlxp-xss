import logging

from rest_framework import serializers

from core.models import SchemaLedger, TermSet, TransformationLedger

logger = logging.getLogger('dict_config_logger')


class SchemaLedgerSerializer(serializers.ModelSerializer):
    """Serializes the SchemaLedger Model"""

    class Meta:
        model = SchemaLedger

        exclude = ('schema_file', 'major_version', 'minor_version',
                   'patch_version',)


class TermSetSerializer(serializers.ModelSerializer):
    """Serializes the TermSet Model"""
    schema = serializers.DictField(source='export')

    class Meta:
        model = TermSet

        fields = ('iri', 'name', 'version', 'schema')


class TransformationLedgerSerializer(serializers.ModelSerializer):
    """Serializes the SchemaLedger Model"""

    class Meta:
        model = TransformationLedger

        exclude = ('schema_mapping_file', 'source_schema', 'target_schema',)
