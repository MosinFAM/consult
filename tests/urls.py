from django.urls import path
from . import views

urlpatterns = [
    path('course/<int:course_id>/article/<int:article_id>/tests/<int:test_id>/', views.test_detail, name='test_detail'),
    path('course/<int:course_id>/article/<int:article_id>/tests/<int:test_id>/results/', views.test_results, name='test_results'),
]
