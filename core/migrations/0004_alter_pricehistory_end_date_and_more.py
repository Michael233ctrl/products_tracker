# Generated by Django 4.1.1 on 2022-09-19 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_pricehistory_end_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pricehistory",
            name="end_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="pricehistory",
            name="start_date",
            field=models.DateField(),
        ),
    ]
