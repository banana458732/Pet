# Generated by Django 5.1.3 on 2024-11-24 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("karikeiyaku", "0002_karikeiyaku_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="karikeiyaku",
            name="status",
            field=models.CharField(
                choices=[
                    ("仮契約中", "仮契約中"),
                    ("キャンセル", "キャンセル"),
                    ("仮契約済", "仮契約済"),
                ],
                default="仮契約中",
                max_length=50,
                verbose_name="ステータス",
            ),
        ),
    ]
