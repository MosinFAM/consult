# Generated by Django 5.1.1 on 2024-10-18 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tests", "0004_alter_test_options_test_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="testresult",
            name="answer_text",
            field=models.TextField(blank=True, default=" ", null=True),
        ),
    ]