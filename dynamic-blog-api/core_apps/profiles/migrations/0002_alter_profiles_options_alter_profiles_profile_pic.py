# Generated by Django 4.0.5 on 2022-06-25 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profiles',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AlterField(
            model_name='profiles',
            name='profile_pic',
            field=models.ImageField(default='', upload_to='', verbose_name='DP'),
        ),
    ]
