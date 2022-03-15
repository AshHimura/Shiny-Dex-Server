# Generated by Django 4.0.3 on 2022-03-15 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shinydexapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='home_regions',
            field=models.ManyToManyField(through='shinydexapi.RegionPokemon', to='shinydexapi.region'),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='poke_items',
            field=models.ManyToManyField(through='shinydexapi.ItemPokemon', to='shinydexapi.item'),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='poke_types',
            field=models.ManyToManyField(through='shinydexapi.TypePokemon', to='shinydexapi.type'),
        ),
    ]
