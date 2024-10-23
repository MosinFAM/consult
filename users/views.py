from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Profile, Enrollment
from main.models import Course
from tests.models import FinalTestResult
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
# from xhtml2pdf import pisa  # Библиотека для создания PDF
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.conf import settings
import os
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import fonts
from io import BytesIO
from reportlab.lib import colors



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт был создан! Войти сейчас!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
        }
    return render(request, 'users/register.html', context=context)


def logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')


@login_required
def profile(request):

    enrollments = Enrollment.objects.filter(user=request.user)
    courses = [enrollment.course for enrollment in enrollments]
    final_test_results = FinalTestResult.objects.filter(profile=request.user.profile, passed=True)

    context = {
        'u_form': ProfileUpdateForm(instance=request.user),
        'courses': courses,
        'final_test_results': final_test_results,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/edit_profile.html', context)


# Функция для автоматического переноса текста на несколько строк
def draw_wrapped_text(p, text, width, start_height, font_size, max_width):
    p.setFont("DejaVu", font_size)
    lines = []
    words = text.split(' ')
    current_line = []
    current_width = 0

    for word in words:
        word_width = pdfmetrics.stringWidth(word, "DejaVu", font_size)
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width + pdfmetrics.stringWidth(' ', "DejaVu", font_size)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width

    if current_line:
        lines.append(' '.join(current_line))

    for i, line in enumerate(lines):
        p.drawCentredString(width / 2, start_height - i * (font_size + 6), line)

    return start_height - len(lines) * (font_size + 6)

@login_required
def download_certificate(request, course_id):
    # Проверяем наличие имени и фамилии
    if not request.user.profile.first_name or not request.user.profile.last_name:
        return HttpResponse('Заполните имя и фамилию в профиле, чтобы получить сертификат.', status=400)
    try:
        final_test_result = FinalTestResult.objects.get(
            profile=request.user.profile,
            final_test__course_id=course_id,
            passed=True
        )
    except FinalTestResult.DoesNotExist:
        return HttpResponse('Сертификат недоступен. Вы не прошли финальный тест.', status=400)

    # Создаем PDF в памяти
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    # Путь к шрифту DejaVuSans.ttf
    font_path = os.path.join(settings.BASE_DIR, 'users', 'fonts', 'DejaVuSans.ttf')

    # Регистрация шрифта
    pdfmetrics.registerFont(TTFont('DejaVu', font_path))

    # Установка размеров страницы
    width, height = letter

    # Рисуем рамку
    p.setStrokeColor(colors.tan)
    p.setLineWidth(4)
    p.rect(40, 40, width - 80, height - 80)

    # Логотип или название организации
    p.setFont("DejaVu", 28)
    p.setFillColor(colors.tan)
    p.drawCentredString(width / 2, height - 100, "Интеллексиум")

    # Название сертификата
    p.setFont("DejaVu", 27)
    p.setFillColor(colors.black)
    p.drawCentredString(width / 2, height - 180, "Сертификат об окончании курса")

    # Имя пользователя
    p.setFont("DejaVu", 24)
    p.setFillColor(colors.black)
    p.drawCentredString(width / 2, height - 260, f"Вручён: {request.user.profile.first_name} {request.user.profile.last_name}")

    # Название курса и результат теста с автоматическим переносом текста
    draw_wrapped_text(p, f"Курс: {final_test_result.final_test.course.title}", width, height - 320, 20, width - 100)
    draw_wrapped_text(p, f"Результат: {final_test_result.score} из {final_test_result.total_questions} баллов", width, height - 380, 20, width - 100)

    # Дата выдачи
    from django.utils import timezone
    p.setFont("DejaVu", 18)
    p.drawCentredString(width / 2, height - 460, f"Дата выдачи: {timezone.now().strftime('%d.%m.%Y')}")

    # Завершаем работу с PDF
    p.showPage()
    p.save()

    # Перемещаем содержимое буфера в HTTP-ответ
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

@login_required
def generate_certificate(request, course_id):
    return download_certificate(request, course_id)