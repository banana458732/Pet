# Generated by Django 5.1.3 on 2024-11-24 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("messaging", "0018_karikeiyaku"),
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