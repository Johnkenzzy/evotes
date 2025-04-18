# Generated by Django 4.2.20 on 2025-04-09 07:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0001_initial'),
        ('ballots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('voter_id', models.CharField(max_length=100, unique=True)),
                ('full_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_accredited', models.BooleanField(default=False)),
                ('has_voted', models.BooleanField(default=False)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.organization')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ballot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ballots.ballot')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ballots.option')),
                ('voter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='voters.voter')),
            ],
            options={
                'unique_together': {('voter', 'ballot')},
            },
        ),
    ]
