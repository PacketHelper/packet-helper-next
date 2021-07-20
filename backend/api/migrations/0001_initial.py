# Generated by Django 3.1.13 on 2021-07-19 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Hexes",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hex", models.CharField(max_length=1000)),
                ("like", models.IntegerField()),
                ("unlike", models.IntegerField()),
            ],
        ),
    ]
