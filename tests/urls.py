from django.urls import path
from tests.views import (
    test_detail, test_results
    #   TestPassView, FinalTestDetailView, FinalTestPassView
)

 
urlpatterns = [
    path('course/<int:course_id>/article/<int:article_id>/tests/<int:test_id>/', test_detail, name='test_detail'),
    path('course/<int:course_id>/article/<int:article_id>/tests/<int:test_id>/results/', test_results, name='test_results'),
#     path('course/<int:course_id>/article/<int:article_id>/tests/<int:test_id>/pass/', TestPassView.as_view(), name='test_pass'),
#     path('course/<int:course_id>/final-test/<int:test_id>/', FinalTestDetailView.as_view(), name='final_test_detail'),
#     path('course/<int:course_id>/final-test/<int:test_id>/pass/', FinalTestPassView.as_view(), name='final_test_pass'),
]
