# Generated by Django 5.1.1 on 2024-10-09 22:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_question_answer_test_question_test"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="question",
            name="test",
        ),
        migrations.RemoveField(
            model_name="test",
            name="article",
        ),
        migrations.DeleteModel(
            name="Answer",
        ),
        migrations.DeleteModel(
            name="Question",
        ),
        migrations.DeleteModel(
            name="Test",
        ),
    ]
