from django.urls import path
from .views import home, about, course_detail, article_detail, category_list, courses_by_category


urlpatterns = [
    path('', home, name='home'),
    path('about-us', about, name='about'),
    path('categories/', category_list, name='category_list'),  
    path('categories/<int:category_id>/courses/', courses_by_category, name='courses_by_category'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('course/<int:course_id>/article/<int:article_id>/', article_detail, name='article_detail'),
]
