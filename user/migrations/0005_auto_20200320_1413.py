# Generated by Django 3.0.2 on 2020-03-20 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20200304_0930'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='activeTutor',
            new_name='active_tutor',
        ),
    ]