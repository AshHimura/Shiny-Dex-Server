# Generated by Django 4.0.3 on 2022-03-25 02:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shinydexapi', '0009_alter_pokemon_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pokemon',
            old_name='img',
            new_name='poke_img',
        ),
    ]