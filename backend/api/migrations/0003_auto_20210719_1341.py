# Generated by Django 3.1.13 on 2021-07-19 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_auto_20210719_1243"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hexes",
            name="like",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="hexes",
            name="unlike",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
