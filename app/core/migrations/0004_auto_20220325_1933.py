# Generated by Django 3.1.14 on 2022-03-25 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20220324_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='mapping',
            field=models.ManyToManyField(blank=True, related_name='_term_mapping_+', to='core.Term'),
        ),
    ]
