from django.urls import path
from main.views import home, about, courses, course1, course2, course3


urlpatterns = [
    path('', home, name='home'),
    path('about-us', about, name='about'),
    path('courses/course1', course1, name='course1'),
    path('courses/course2', course2, name='course2'),
    path('courses/course3', course3, name='course3'),
    path('courses', courses, name='courses'),
]
