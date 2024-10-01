from django.urls import path
from main.views import home, about, courses


urlpatterns = [
    path('', home, name='home'),
    path('about-us', about, name='about'),
    path('courses', courses, name='courses'),
]
