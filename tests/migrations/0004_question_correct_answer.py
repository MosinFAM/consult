# Generated by Django 5.1.1 on 2024-10-10 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0003_alter_test_article"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="correct_answer",
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
