# Generated by Django 4.2.20 on 2025-04-22 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voters', '0006_rename_organisation_voter_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voter',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
