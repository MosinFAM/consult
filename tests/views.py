from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from main.models import Course, Article
from users.models import Profile
from .models import Test, Answer, TestResult, FinalTest, Enrollment
from django.contrib.auth.decorators import login_required
# Create your views here.

# Детали теста
# def test_detail(request, course_id, article_id, test_id):
#     course = get_object_or_404(Course, id=course_id)
#     article = get_object_or_404(Article, id=article_id, course=course)
#     test = get_object_or_404(Test, id=test_id, article=article)

def test_detail_ok(request, course_id, article_id, test_id):
    # test = Test.objects.get(id=article_id)
    test = get_object_or_404(Test, id=article_id)
    course = Test.objects.filter(id=course_id) 
    # article = get_object_or_404(Article, id=article_id, course=course)
    questions = test.questions.all().prefetch_related('answers')

    context = {
        'course': course,
        # 'article': article,
        'test': test,
        'questions': questions
    }
    return render(request, 'tests/test_detail.html', context)

def test_detail(request, course_id, article_id, test_id):
    article = Test.objects.filter(id=article_id) 
    course = Test.objects.filter(id=course_id) 
    test = get_object_or_404(Test, id=article_id)
    return render(request, 'main/course_detail.html', {
        'course': course,
        'article': article,
        'test': test
    })
    
@login_required
def test_detail(request, course_id, article_id, test_id):
    print(f"Querying Profile with course_id={course_id}, article_id={article_id}, test_id={test_id}")
    # course = Test.objects.filter(course=course) 
    # article = Test.objects.filter(article=article) 
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=article_id, course=course)
    test = get_object_or_404(Test, id=test_id, article=article)
    # profile = get_object_or_404(Profile, user=request.user)
    profile = get_object_or_404(Profile, id=course_id)
    questions = test.questions.all()

    if request.method == 'POST':
        score = 0
        total = questions.count()
        for question in questions:
            field_name = f'question_{question.id}'
            user_answer = request.POST.get(field_name)

            if question.question_type == 'multiple_choice':
                try:
                    selected_answer = Answer.objects.get(id=user_answer, question=question)
                    if selected_answer.is_correct:
                        score += 1
                except Answer.DoesNotExist:
                    pass  # Неверный выбор или не выбран ответ
            elif question.question_type == 'text':
                correct_answer = question.answers.filter(is_correct=True).first().text.strip().lower() 
                if user_answer == correct_answer:
                    score += 1

        passed = score >= (total - 1)  # Максимум 1 ошибка
        TestResult.objects.create(profile=profile, test=test, score=score, total_questions = total, passed=passed)
        
        return redirect('tests/test_detail.html', course_id=article.course.id)
    
    context = {
        'course_id': course.id,
        'article_id': article.id,
        'test_id': test.id,
        # other context data...
    }
    context2 = {
        'course': course,
        'article': article,
        'test': test,
        'questions': questions,
        # other context data...
    }

    return render(request, 'tests/test_detail.html', context2)

@login_required
def test_results(request, course_id, article_id, test_id):
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=article_id, course=course)
    test = get_object_or_404(Test, id=test_id, article=article)
    profile = get_object_or_404(Profile, user=request.user)

    # Получаем последний результат теста пользователя
    result = TestResult.objects.filter(profile=profile, test=test).order_by('-date_taken').first()

    context = {
        'course': course,
        'article': article,
        'test': test,
        'result': result,
    }

    return render(request, 'tests/test_results.html', context)

# Прохождение теста
class TestPassView(View):
    pass
    # def post(self, request, course_id, article_id, test_id):
    #     test = get_object_or_404(Test, id=test_id, article_id=article_id)
    #     # Логика прохождения теста
    #     return render(request, 'main/test_result.html', {'test': test})


# Детали финального теста
class FinalTestDetailView(View):
    pass
    # def get(self, request, course_id, test_id):
    #     final_test = get_object_or_404(FinalTest, id=test_id, course_id=course_id)
    #     return render(request, 'main/final_test_detail.html', {'final_test': final_test})


# Прохождение финального теста
class FinalTestPassView(View):
    pass
    # def post(self, request, course_id, test_id):
    #     final_test = get_object_or_404(FinalTest, id=test_id, course_id=course_id)
    #     # Логика прохождения финального теста
    #     return render(request, 'main/final_test_result.html', {'final_test': final_test})
