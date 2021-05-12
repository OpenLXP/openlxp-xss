from django.contrib import admin

from core.models import SchemaLedger


# Register your models here.
@admin.register(SchemaLedger)
class SchemaLedgerAdmin(admin.ModelAdmin):
    list_display = ('id', 'schema_name', 'schema_iri', 'status', )
