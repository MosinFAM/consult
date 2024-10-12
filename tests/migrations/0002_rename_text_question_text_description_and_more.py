# Generated by Django 5.1.1 on 2024-10-10 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="question",
            old_name="text",
            new_name="text_description",
        ),
        migrations.AddField(
            model_name="question",
            name="text_task",
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
