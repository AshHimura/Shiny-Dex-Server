# Generated by Django 4.0.3 on 2022-03-25 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shinydexapi', '0008_remove_post_image_url_remove_post_title_pokemon_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='img',
            field=models.ImageField(null=True, upload_to='image'),
        ),
    ]
