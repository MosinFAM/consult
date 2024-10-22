# Generated by Django 5.1.1 on 2024-10-21 22:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0002_remove_finaltest_questions"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="final_test",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="tests.finaltest",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="test",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="tests.test",
            ),
        ),
    ]
