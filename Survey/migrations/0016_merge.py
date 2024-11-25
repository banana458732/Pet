# 0016_merge.py
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('Survey', '0015_alter_surveyresult_disease'),
        ('Survey', '0015_delete_surveyhistory'),
    ]

    operations = [
    ]
