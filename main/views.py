from django.shortcuts import render, get_object_or_404, redirect
from main.models import Course, Article, Category
from tests.models import Test, Question, TestResult
from users.models import Profile
from users.models import Enrollment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max



# Главная страница
def home(request):
    return render(request, 'main/home.html', {'title': 'Home'})


# Страница "О нас"
def about(request):
    return render(request, 'main/about.html', {'title': 'About Us'})


# Детали курса
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'main/course_detail.html', {'course': course})



# Детализация курса с логикой регистрации на курс
@login_required
def course_detail(request, course_id):
    profile = get_object_or_404(Profile, user=request.user)
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=course_id)
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    tests = Test.objects.filter(article=article) 
    passed_tests = TestResult.objects.filter(profile=profile, passed=True).values_list('test_id', flat=True)
    print("LEN OF PASSED:", len(passed_tests))
    passed_test_ids = set(passed_tests)


    max_order = Test.objects.filter(id__in=passed_tests).aggregate(Max('order'))['order__max'] or 0
    
    # Устанавливаем следующий доступный тест
    next_test_order = max_order + 1

    if request.method == 'POST':
        if 'enroll' in request.POST:
            Enrollment.objects.create(user=request.user, course=course)
            messages.success(request, f'Вы успешно записались на курс {course.title}')
        elif 'unenroll' in request.POST:
            Enrollment.objects.filter(user=request.user, course=course).delete()
            messages.success(request, f'Вы покинули курс {course.title}')
        return redirect('course_detail', course_id=course_id)

    context = {
        'course': course,
        'is_enrolled': is_enrolled, 
        'tests': tests,
        'passed_tests': passed_test_ids,
        'next_test_order': next_test_order,
    }   
    return render(request, 'main/course_detail.html', context)


# Детали статьи
def article_detail(request, course_id, article_id):
    article = get_object_or_404(Article, id=article_id, course_id=course_id)
    tests = Test.objects.filter(article=article) 
    return render(request, 'main/article_detail.html', {'article': article, 'tests': tests})


#Список категорий
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'main/category_list.html', {'categories': categories})


# Отображение курсов по категории
def courses_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    courses = Course.objects.filter(category=category)
    if not courses:
        message = "Курсов в этой категории пока нет."
    else:
        message = None
    return render(request, 'main/courses_by_category.html', {'category': category, 'courses': courses, 'message': message})

# def test_detail(request, course_id, article_id, test_id):
#     test = get_object_or_404(Test, id=test_id, article_id=article_id, course_id=course_id)
#     return render(request, 'main/test_detail.html', {'test': test})


def search_courses(request):
    query = request.GET.get('q')  # Получаем строку запроса
    courses = None
    message = None  # Сообщение для случая, если ничего не найдено

    if query:
        # Ищем курсы по названию или описанию (по частям слов)
        courses = Course.objects.filter(title__icontains=query) | Course.objects.filter(description__icontains=query)

        if not courses.exists():
            message = f'По запросу "{query}" ничего не найдено.'

    return render(request, 'main/home.html', {'courses': courses, 'message': message, 'query': query})
