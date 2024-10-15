from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Test, Question, TestResult, FinalTest, Answer, Course, Article



def test_detail(request, course_id, article_id, test_id):
    # Получаем курс, статью и тест
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=article_id)
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all()

    # Проверим, доступен ли тест (если есть предыдущий тест)
    if test.prerequisite_test and not TestResult.objects.filter(test=test.prerequisite_test, user=request.user, passed=True).exists():
        return redirect('test_locked')

    context = {
        'course': course,
        'article': article,
        'test': test,
        'questions': questions,
    }
    return render(request, 'tests/test_detail.html', context)




# Прохождение теста
def pass_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    questions = test.questions.all()
    user_answers = request.POST  # Получаем ответы пользователя из формы

    score = 0
    for question in questions:
        if question.question_type == Question.CHOICE or question.question_type == Question.MULTIPLE_CHOICE:
            selected_answer = user_answers.get(f'question_{question.id}')
            if selected_answer and Answer.objects.get(id=selected_answer).is_correct:
                score += 1
        elif question.question_type == Question.OPEN:
            # Логика проверки открытых ответов
            pass

    passed = score >= len(questions) * 0.7  # Условие прохождения
    result = TestResult.objects.create(user=request.user, test=test, score=score, passed=passed)

    # Обновляем лучшую попытку
    TestResult.objects.filter(user=request.user, test=test).update(best_attempt=False)
    result.best_attempt = True
    result.save()

    context = {
        'test': test,
        'score': score,
        'passed': passed,
        'best_attempt': result
    }
    return render(request, 'tests/test_result.html', context)

# Детали финального теста
class FinalTestDetailView(View):
    def get(self, request, course_id, test_id):
        final_test = get_object_or_404(FinalTest, id=test_id)
        # Проверяем, все ли предыдущие тесты пройдены
        for test in final_test.prerequisite_tests.all():
            if not TestResult.objects.filter(test=test, user=request.user, passed=True).exists():
                return redirect('test_locked')

        return render(request, 'tests/final_test_detail.html', {'final_test': final_test})

# Прохождение финального теста
class FinalTestPassView(View):
    def post(self, request, course_id, test_id):
        final_test = get_object_or_404(FinalTest, id=test_id)
        # Логика прохождения финального теста (аналогично обычным тестам)
        pass