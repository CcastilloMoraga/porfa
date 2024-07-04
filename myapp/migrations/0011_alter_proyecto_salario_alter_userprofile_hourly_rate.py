# Generated by Django 5.0.1 on 2024-06-15 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_remove_proyecto_salario_currency_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='salario',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='hourly_rate',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
