# Generated by Django 3.0.4 on 2020-04-06 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200331_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='fill_out_sheet',
            name='no_response',
            field=models.BooleanField(default=True),
        ),
    ]
