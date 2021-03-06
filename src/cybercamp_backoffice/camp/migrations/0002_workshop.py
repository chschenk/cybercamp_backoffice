# Generated by Django 3.1.7 on 2021-03-25 16:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('camp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(help_text='Eine Beschreibung für deinen Workshop', verbose_name='Beschreibung')),
                ('start_time', models.DateTimeField(help_text='Wann beginnt dein Workshop?', verbose_name='Start Zeit')),
                ('end_time', models.DateTimeField(help_text='Bis wann geht dein Workshop?', verbose_name='End Zeit')),
                ('location', models.TextField(blank=True, help_text='Wo findet dein Workshop statt? Falls du keine Ahnung hast wo du deinen Workshop statt finden lassen kannst, lass dieses Feld einfach leer, dann weisen wir dir einen Ort zu.', null=True, verbose_name='Ort')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
