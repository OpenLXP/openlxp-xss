from core.models import SchemaLedger, TransformationLedger
from django.contrib import admin


# Register your models here.
@admin.register(SchemaLedger)
class SchemaLedgerAdmin(admin.ModelAdmin):
    """Admin form for the SchemaLedger model"""
    list_display = ('id', 'schema_name', 'schema_iri', 'status', 'version',)
    fields = [('schema_name', 'schema_iri', 'schema_file', 'status',),
              ('major_version', 'minor_version', 'patch_version',)]


@admin.register(TransformationLedger)
class TransformationLedgerAdmin(admin.ModelAdmin):
    """Admin form for the TransformationLedger model"""
    list_display = ('id', 'source_schema_name', 'source_schema_version',
                    'target_schema_name', 'target_schema_version', 'status',)
    fields = [('source_schema', 'target_schema',),
              ('schema_mapping_file', 'status',)]

    # Override the foreign key fields to show the name and version in the
    # admin form instead of the ID
    def get_form(self, request, obj=None, **kwargs):
        form = super(TransformationLedgerAdmin, self).get_form(request,
                                                               obj,
                                                               **kwargs)
        form.base_fields['source_schema'].label_from_instance = \
            lambda obj: "{} {}".format(obj.schema_name, obj.version)
        form.base_fields['target_schema'].label_from_instance = \
            lambda obj: "{} {}".format(obj.schema_name, obj.version)
        return form
