# Generated by Django 4.2.20 on 2025-04-10 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_alter_organization_address_alter_organization_logo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationadmin',
            name='is_super_admin',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
