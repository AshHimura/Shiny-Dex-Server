# Generated by Django 4.0.3 on 2022-03-22 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shinydexapi', '0004_alter_pokemon_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='caught',
            old_name='isAlpha',
            new_name='is_alpha',
        ),
        migrations.RenameField(
            model_name='caught',
            old_name='isShiny',
            new_name='is_shiny',
        ),
    ]
