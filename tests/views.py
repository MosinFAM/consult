from django.shortcuts import render, get_object_or_404, redirect
from main.models import Course, Article
from .models import Test, Question, TestResult
from .forms import TestForm
from django.contrib.auth.decorators import login_required

@login_required
def test_welcome(request, course_id, article_id, test_id):
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=article_id, course=course)
    test = get_object_or_404(Test, id=test_id, article=article)
    question_count = test.questions.count()

    return render(request, 'tests/test_welcome.html', {
        'course': course,
        'article': article,
        'test': test,
        'question_count': question_count,
    })

@login_required
def test_detail(request, course_id, article_id, test_id):
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=article_id, course=course)
    test = get_object_or_404(Test, id=test_id, article=article)
    questions = test.questions.all()

    if request.method == 'POST':
        form = TestForm(request.POST, questions=questions)
        if form.is_valid():
            correct_answers = 0
            total_questions = questions.count()

            for question in questions:
                if question.question_type == Question.SINGLE_CHOICE:
                    selected_option = form.cleaned_data[f'question_{question.id}']
                    correct_option = question.options.get(is_correct=True)
                    if int(selected_option) == correct_option.id:
                        correct_answers += 1
                elif question.question_type == Question.MULTIPLE_CHOICE:
                    selected_options = form.cleaned_data[f'question_{question.id}']
                    correct_options = question.options.filter(is_correct=True)
                    if set(map(int, selected_options)) == set(correct_options.values_list('id', flat=True)):
                        correct_answers += 1
                elif question.question_type == Question.TEXT_ANSWER:
                    user_answer = form.cleaned_data[f'question_{question.id}']
                    # Проверка текстовых ответов может быть любой (например, полное совпадение или более сложная логика)

            score = correct_answers / total_questions
            is_passed = correct_answers >= (total_questions - 1)
            
            TestResult.objects.create(user=request.user, test=test, score=score, is_passed=is_passed)
            return redirect('test_result', course_id=course_id, article_id=article_id, test_id=test_id)
    else:
        form = TestForm(questions=questions)

    return render(request, 'tests/test_detail.html', {
        'course': course,
        'article': article,
        'test': test,
        'form': form,
    })

@login_required
def test_result(request, course_id, article_id, test_id):
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=article_id, course=course)
    test = get_object_or_404(Test, id=test_id, article=article)
    result = TestResult.objects.filter(user=request.user, test=test).order_by('-id').first()

    return render(request, 'tests/test_result.html', {
        'course': course,
        'article': article,
        'test': test,
        'result': result,
    })

@login_required
def course_final_test(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Логика для финального теста
    return render(request, 'tests/course_final_test.html', {'course': course})

@login_required
def final_test_result(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    # Логика отображения результата финального теста
    return render(request, 'tests/final_test_result.html', {'course': course})
