from django.contrib import admin

from core.models import SchemaLedger, TransformationLedger


# Register your models here.
@admin.register(SchemaLedger)
class SchemaLedgerAdmin(admin.ModelAdmin):
    list_display = ('id', 'schema_name', 'schema_iri', 'status', 'version',)
    fields = [('schema_name', 'schema_iri', 'schema_file', 'status',),
              ('major_version', 'minor_version', 'patch_version',)]


@admin.register(TransformationLedger)
class TransformationLedgerAdmin(admin.ModelAdmin):
    list_display = ('id', 'source_schema_name', 'source_schema_version',
                    'target_schema_name', 'target_schema_version', 'status',)
    fields = [('source_schema_name', 'source_schema_version',),
              ('target_schema_name', 'target_schema_version',),
              ('schema_mapping_file', 'status',)]
