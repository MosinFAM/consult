# Generated by Django 5.1.1 on 2024-10-18 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0003_enrollment"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="test",
            options={
                "ordering": ["order"],
                "verbose_name": "Тест",
                "verbose_name_plural": "Тесты",
            },
        ),
        migrations.AddField(
            model_name="test",
            name="order",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
