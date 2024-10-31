# Generated by Django 4.0 on 2024-10-24 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0008_delete_surveyresult_alter_pet_color_alter_pet_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_type', models.CharField(choices=[('dog', '犬'), ('cat', '猫')], max_length=10)),
                ('size', models.CharField(choices=[('small', '小型'), ('medium', '中型'), ('large', '大型')], max_length=10)),
                ('age', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='pet',
            name='color',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='pet',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='pet',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='pets/'),
        ),
    ]
