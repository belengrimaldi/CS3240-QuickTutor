# Generated by Django 3.0.2 on 2020-04-10 17:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('location', models.CharField(blank=True, max_length=30)),
                ('year', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('classes_taken', models.TextField(blank=True, max_length=400)),
                ('help_needed', models.TextField(blank=True, max_length=300)),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('active_tutor', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_content', models.TextField(blank=True, max_length=400, verbose_name='message content')),
                ('created_at', models.TimeField(default=django.utils.timezone.now)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Fill_Out_Sheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_tutor_accepted', models.BooleanField(default=False, null=True)),
                ('has_tutor_rejected', models.BooleanField(default=False, null=True)),
                ('no_response', models.BooleanField(default=True, null=True)),
                ('class_desc', models.CharField(blank=True, max_length=30)),
                ('help_desc', models.TextField(blank=True, max_length=100)),
                ('meeting_places', models.CharField(choices=[('Alderman Library', 'Alderman Library'), ('Clark (Brown) Library', 'Clark (Brown) Library'), ('Clemmons Library', 'Clemmons Library'), ('Starbucks (Corner)', 'Starbucks (Corner)'), ('Starbucks (Newcomb)', 'Starbucks (Newcomb)'), ('Argo Tea', 'Argo Tea'), ('Einstein Bros (Rice)', 'Einstein Bros (Rice)'), ('15|15', '15|15')], default='15|15', max_length=200)),
                ('time_slot', models.CharField(choices=[('1', '5-15 minutes'), ('2', '15-30 minutes'), ('3', '30 minutes-1 hour'), ('4', 'More than 1 hour')], default='1', max_length=20)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
