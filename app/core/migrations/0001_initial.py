# Generated by Django 3.1.12 on 2021-06-08 19:39

import django.utils.timezone
import model_utils.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SchemaLedger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('schema_name', models.CharField(max_length=255)),
                ('schema_iri', models.CharField(max_length=255)),
                ('schema_file', models.FileField(blank=True, null=True, upload_to='schemas/')),
                ('status', models.CharField(choices=[('published', 'published'), ('retired', 'retired')], max_length=10)),
                ('metadata', models.JSONField(blank=True, help_text='auto populated from uploaded file')),
                ('version', models.CharField(help_text='auto populated from other version fields', max_length=6)),
                ('major_version', models.SmallIntegerField()),
                ('minor_version', models.SmallIntegerField()),
                ('patch', models.SmallIntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransformationLedger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('source_schema_name', models.CharField(max_length=255)),
                ('target_schema_name', models.CharField(max_length=255)),
                ('source_schema_version', models.CharField(help_text='version of the source schema', max_length=6)),
                ('target_schema_version', models.CharField(help_text='version of the target schema', max_length=6)),
                ('schema_mapping_file', models.FileField(blank=True, null=True, upload_to='schemas/')),
                ('status', models.CharField(choices=[('published', 'published'), ('retired', 'retired')], max_length=10)),
                ('schema_mapping', models.JSONField(blank=True, help_text='auto populated from uploaded file')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
