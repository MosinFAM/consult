from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from main.models import Course, Article
from users.models import Profile
from .models import Test, Answer, TestResult, FinalTest, OpenAnswer, FinalTestResult
from users.models import Enrollment
from django.contrib.auth.decorators import login_required


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





@login_required
def test_detail(request, course_id, article_id, test_id):
    print(f"Querying Profile with course_id={course_id}, article_id={article_id}, test_id={test_id}")
    
    # Получаем объекты курса, статьи, теста и профиля пользователя
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=article_id, course=course)
    test = get_object_or_404(Test, id=test_id, article=article)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Получаем все вопросы текущего теста
    questions = test.questions.all()

    if request.method == 'POST':
        score = 0
        total = questions.count()
        text_answers = {}

        # Проходим по каждому вопросу теста
        for question in questions:
            field_name = f'question_{question.id}'
            user_answer = request.POST.get(field_name)

            # Обрабатываем ответы на выборочные вопросы
            if question.question_type == 'multiple_choice':
                try:
                    selected_answer = Answer.objects.get(id=user_answer, question=question)
                    if selected_answer.is_correct:
                        score += 1
                except Answer.DoesNotExist:
                    pass  # Ответ неверный или не выбран

            # Обрабатываем текстовые ответы
            elif question.question_type == 'text':
                if user_answer:
                    text_answers[question.id] = user_answer.strip()  # Убираем лишние пробелы
                    score += 1  # По умолчанию добавляем балл, но это может изменяться в зависимости от требований

        # Сохраняем результат теста
        last_result = TestResult.objects.filter(profile=profile, test=test).order_by('-id').first()
        
        if last_result:
            # Если результат уже существует, обновляем его
            last_result.score = score
            last_result.total_questions = total
            last_result.passed = (score >= (total - 1))  # Порог прохождения теста (можно менять)
            last_result.save()
        else:
            # Если результата нет, создаем новый
            TestResult.objects.create(
                profile=profile,
                test=test,
                score=score,
                total_questions=total,
                passed=(score >= (total - 1))  # Условие прохождения теста
            )

        # Перенаправляем на страницу с результатами теста
        return redirect('test_results', course_id=course.id, article_id=article.id, test_id=test.id)

    print(f"Found test: {test}")
    return render(request, 'tests/test_detail.html', {
        'course': course,
        'article': article,
        'test': test,
        'questions': questions,
    })



 
@login_required
def test_results(request, course_id, article_id, test_id):
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=article_id, course=course)
    test = get_object_or_404(Test, id=test_id, article=article)
    # profile = get_object_or_404(Profile, user=request.user)

    profile, created = Profile.objects.get_or_create(user=request.user)

    # Получаем последний результат теста пользователя
    # result = TestResult.objects.filter(profile=profile, test=test).order_by('-date_taken').first()

    result = TestResult.objects.filter(profile=profile, test=test).first()

    # if result is None:
    #     print(f"No result found for profile {profile.id} and test {test.id}.")
    #     result = TestResult(score=0, total_questions=0, passed=True)
    

    context = {
        'course': course,
        'article': article,
        'test': test,
        'result': result,
    }

    return render(request, 'tests/test_results.html', context)


def final_test_detail_ok(request, course_id, article_id, test_id):
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
    return render(request, 'tests/final_test_detail.html', context)



@login_required
def final_test_detail(request, course_id):
    # Получаем курс по его ID
    course = get_object_or_404(Course, id=course_id)
    profile = get_object_or_404(Profile, user=request.user)
    
    # Предполагаем, что вы передаете test_id в URL
    ftest = get_object_or_404(FinalTest, course=course)  # Получаем тест для курса
    questions = ftest.questions.all()

    if request.method == 'POST':
        score = 0
        total = questions.count()
        text_answers = {}

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
                # Обработка текстовых ответов
                if user_answer:  # Убедимся, что ответ не пуст
                    text_answers[question.id] = user_answer.strip()  # Сохраняем текстовый ответ
                    # Дополнительная логика проверки правильности текстового ответа может быть здесь
                    score += 1
            
            for question_id, user_answer in text_answers.items():
                last_result = FinalTestResult.objects.filter(profile=profile, final_test=ftest).order_by('-id').first()
                # Вы можете создать отдельную модель для хранения текстовых ответов или
                # просто добавить текст ответа в TestResult
                if last_result:
            # Если результат уже существует, обновляем его
                    last_result.score = score
                    last_result.total_questions = total
                    last_result.passed = (score >= (total - 1))
                    last_result.save()  # Сохраняем изменения
                else:
                    # Если результата нет, создаем новый
                    FinalTestResult.objects.create(
                        profile=profile,
                        final_test=ftest,
                        score=score,
                        total_questions=total,
                        passed=(score >= (total*0.6))  # Логика прохождения теста
                    )
        

                # Переадресация на страницу с результатами теста
                return redirect('final_test_results', course_id=course.id)

    return render(request, 'tests/final_test_detail.html', {
        'course': course,
        'questions': questions,
        'ftest': ftest  # Возможно, стоит передать объект теста в шаблон
    })



@login_required
def final_test_results(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    test = get_object_or_404(FinalTest, course=course)
    # profile = get_object_or_404(Profile, user=request.user)

    profile, created = Profile.objects.get_or_create(user=request.user)

    # Получаем последний результат теста пользователя
    # result = TestResult.objects.filter(profile=profile, test=test).order_by('-date_taken').first()

    result = FinalTestResult.objects.filter(profile=profile, final_test=test).first()

    # if result is None:
    #     print(f"No result found for profile {profile.id} and test {test.id}.")
    #     result = TestResult(score=0, total_questions=0, passed=True)
    

    context = {
        'course': course,
        'result': result,
    }

    return render(request, 'tests/final_test_results.html', context)







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




