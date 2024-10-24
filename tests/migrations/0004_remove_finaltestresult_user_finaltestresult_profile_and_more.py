# Generated by Django 5.1.1 on 2024-10-21 22:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_remove_question_test_remove_test_article_and_more"),
        ("tests", "0003_question_final_test_alter_question_test"),
        ("users", "0002_enrollment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="finaltestresult",
            name="user",
        ),
        migrations.AddField(
            model_name="finaltestresult",
            name="profile",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.profile",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="finaltest",
            name="course",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="ftest",
                to="main.course",
            ),
        ),
    ]
