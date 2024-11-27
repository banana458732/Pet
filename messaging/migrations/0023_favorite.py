# Generated by Django 4.0 on 2024-11-27 01:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_phone_number'),
        ('petapp', '0029_alter_pet_sex'),
        ('messaging', '0022_delete_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by', to='petapp.pet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='accounts.customuser')),
            ],
            options={
                'unique_together': {('user', 'pet')},
            },
        ),
    ]