from django.urls import path
from main.views import (
    home, about, course_list, course_detail, article_detail, test_detail, 
    TestPassView, FinalTestDetailView, FinalTestPassView
)

urlpatterns = [
    path('', home, name='home'),
    path('about-us', about, name='about'),
    path('course_list', course_list, name='course_list'),
    path('course/<int:course_id>/', course_detail, name='course_detail'),
    path('course/<int:course_id>/article/<int:article_id>/', article_detail, name='article_detail'),
    path('course/<int:course_id>/article/<int:article_id>/tests/<int:test_id>/', test_detail, name='test_detail'),
    path('course/<int:course_id>/article/<int:article_id>/tests/<int:test_id>/pass/', TestPassView.as_view(), name='test_pass'),
    path('course/<int:course_id>/final-test/<int:test_id>/', FinalTestDetailView.as_view(), name='final_test_detail'),
    path('course/<int:course_id>/final-test/<int:test_id>/pass/', FinalTestPassView.as_view(), name='final_test_pass'),
]
