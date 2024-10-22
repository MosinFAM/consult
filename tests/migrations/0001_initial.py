# Generated by Django 5.1.1 on 2024-10-21 21:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("main", "0006_remove_question_test_remove_test_article_and_more"),
        ("users", "0002_enrollment"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text_description", models.TextField()),
                ("text_task", models.TextField()),
                (
                    "question_type",
                    models.CharField(
                        choices=[
                            ("multiple_choice", "Multiple Choice"),
                            ("text", "Text"),
                        ],
                        max_length=17,
                    ),
                ),
            ],
            options={
                "verbose_name": "Вопрос",
                "verbose_name_plural": "Вопросы",
            },
        ),
        migrations.CreateModel(
            name="FinalTest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "course",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="main.course"
                    ),
                ),
                ("questions", models.ManyToManyField(to="tests.question")),
            ],
            options={
                "verbose_name": "Финальный тест",
                "verbose_name_plural": "Финальные тесты",
            },
        ),
        migrations.CreateModel(
            name="FinalTestResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("passed", models.BooleanField(default=False)),
                ("score", models.FloatField()),
                ("attempt_count", models.PositiveIntegerField(default=1)),
                (
                    "final_test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tests.finaltest",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Результат финального теста",
                "verbose_name_plural": "Результаты финальных тестов",
            },
        ),
        migrations.CreateModel(
            name="OpenAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answer_text", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        limit_choices_to={"question_type": "open"},
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tests.question",
                    ),
                ),
            ],
            options={
                "verbose_name": "Открытый ответ",
                "verbose_name_plural": "Открытые ответы",
            },
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=255)),
                ("is_correct", models.BooleanField(default=False)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="tests.question",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ответ",
                "verbose_name_plural": "Ответы",
            },
        ),
        migrations.CreateModel(
            name="Test",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("order", models.PositiveIntegerField(default=1)),
                (
                    "article",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tests",
                        to="main.article",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тест",
                "verbose_name_plural": "Тесты",
                "ordering": ["order"],
            },
        ),
        migrations.AddField(
            model_name="question",
            name="test",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="tests.test",
            ),
        ),
        migrations.CreateModel(
            name="Enrollment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("enrolled_at", models.DateTimeField(auto_now_add=True)),
                (
                    "article",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="main.article"
                    ),
                ),
                (
                    "test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tests.test"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TestResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.IntegerField()),
                ("total_questions", models.IntegerField()),
                ("passed", models.BooleanField(default=False)),
                ("answer_text", models.TextField(blank=True, default=" ", null=True)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.profile"
                    ),
                ),
                (
                    "test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="tests.test"
                    ),
                ),
            ],
            options={
                "verbose_name": "Результат теста",
                "verbose_name_plural": "Результаты тестов",
            },
        ),
    ]
