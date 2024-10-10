from django.shortcuts import render, get_object_or_404
from django.views import View
from main.models import Course, Article
from .models import Test, FinalTest, Enrollment
# Create your views here.

# Детали теста
# def test_detail(request, course_id, article_id, test_id):
#     course = get_object_or_404(Course, id=course_id)
#     article = get_object_or_404(Article, id=article_id, course=course)
#     test = get_object_or_404(Test, id=test_id, article=article)

def test_detail(request, course_id, article_id, test_id):
    # test = get_object_or_404(Test, id=article_id, course_id=course_id)
    # enrollments = Enrollment.objects.filter(article=request.article)
    # context = {
    #     'article': article,
    #     'test': test
    #     # Добавляем другие переменные, которые могут понадобиться в шаблоне
    # }

    # # Возвращаем страницу с деталями статьи
    # return render(request, 'main/test_detail.html', context)
    
    test = Test.objects.get(id=article_id)
    course = Test.objects.filter(id=course_id) 
    # article = get_object_or_404(Article, id=article_id, course=course)
    questions = test.questions.all()

    context = {
        'course': course,
        # 'article': article,
        'test': test,
        'questions': questions
    }
    return render(request, 'tests/test_detail.html', context)
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=article_id, course=course)
    test = get_object_or_404(Test, id=test_id, article=article)

    '''
    # Получаем все вопросы для этого теста
    questions = test.questions.all()

    return render(request, 'tests/test_detail.html', {
        'course': course,
        'article': article,
        'test': test,
        'questions': questions
    })
'''

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
