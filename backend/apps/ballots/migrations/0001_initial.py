# Generated by Django 4.2.20 on 2025-04-09 07:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('elections', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ballot',
            fields=[
                ('id', models.UUIDField(
                    default=uuid.uuid4, editable=False,
                    primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('votes', models.IntegerField(default=0)),
                ('election', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='elections.election')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.UUIDField(
                    default=uuid.uuid4,
                    editable=False, primary_key=True,
                    serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150)),
                ('title', models.CharField(max_length=255, null=True)),
                ('photo', models.ImageField(
                    blank=True, null=True,
                    upload_to='candidate_images/')),
                ('votes', models.IntegerField(default=0)),
                ('ballot', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='ballots.ballot')),
            ],
            options={
                'unique_together': {('ballot', 'name')},
            },
        ),
    ]
