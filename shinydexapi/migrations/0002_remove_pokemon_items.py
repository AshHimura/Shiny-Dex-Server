# Generated by Django 4.0.3 on 2022-03-12 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shinydexapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='items',
        ),
    ]