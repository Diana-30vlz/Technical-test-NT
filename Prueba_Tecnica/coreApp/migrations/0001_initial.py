# Generated by Django 5.2 on 2025-07-25 16:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.CharField(max_length=40, primary_key=True, serialize=False, unique=True)),
                ('company_name', models.CharField(blank=True, max_length=130, null=True)),
            ],
            options={
                'verbose_name': 'Compañía',
                'verbose_name_plural': 'Compañías',
            },
        ),
        migrations.CreateModel(
            name='Charges',
            fields=[
                ('charge_id', models.CharField(max_length=40, primary_key=True, serialize=False, unique=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=200, null=True)),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
                ('created_at', models.DateField()),
                ('updated_at', models.DateField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='charges', to='coreApp.company')),
            ],
            options={
                'verbose_name': 'Cargo',
                'verbose_name_plural': 'Cargos',
                'ordering': ['-created_at'],
            },
        ),
    ]
