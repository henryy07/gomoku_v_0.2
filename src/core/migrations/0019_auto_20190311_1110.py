# Generated by Django 2.1.7 on 2019-03-11 11:10

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20190311_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(default='default.jpg', upload_to=core.models.profile_image_file_path),
        ),
    ]