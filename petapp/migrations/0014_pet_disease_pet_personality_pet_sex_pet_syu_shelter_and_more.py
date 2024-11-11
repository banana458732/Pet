# Generated by Django 4.0 on 2024-11-06 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('petapp', '0013_alter_petimage_pet'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='disease',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pet',
            name='personality',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='pet',
            name='sex',
            field=models.CharField(choices=[('男の子', '男の子'), ('女の子', '女の子')], default='', max_length=10),
        ),
        migrations.AddField(
            model_name='pet',
            name='syu',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.CreateModel(
            name='Shelter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
                ('shelter_type', models.CharField(choices=[('normal', '保健所'), ('protection', '保護施設')], default='normal', max_length=20)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shelter_related', to='auth.user')),
            ],
        ),
        migrations.AddField(
            model_name='pet',
            name='shelter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pets', to='petapp.shelter'),
        ),
    ]