# Generated by Django 4.0 on 2025-02-06 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('karikeiyaku', '0004_alter_karikeiyaku_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='karikeiyaku',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='契約終了日'),
        ),
    ]
