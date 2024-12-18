# Generated by Django 5.1.3 on 2024-11-21 07:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("petapp", "0028_remove_pet_syu_pet_kinds_alter_pet_age_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Karikeiyaku",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "end_date",
                    models.DateField(blank=True, null=True, verbose_name="契約終了日"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="作成日時"),
                ),
                (
                    "pet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="petapp.pet",
                        verbose_name="ペット",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="ユーザー",
                    ),
                ),
            ],
        ),
    ]
