from django.shortcuts import render


def home(request):
    context = {
        'title': 'Home page'
        }
    return render(request, 'main/home.html', context=context)


def about(request):
    return render(request, 'main/about.html')


def courses(request):
    return render(request, 'main/courses.html')
