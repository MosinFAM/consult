from django.shortcuts import render, get_object_or_404, redirect
from main.models import Course, Article, Category
from tests.models import Test, Question
from users.models import Enrollment
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=course_id)
    is_enrolled = Enrollment.objects.filter(user=request.user, course=course).exists()
    tests = Test.objects.filter(article=article) 

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
        'tests': tests
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