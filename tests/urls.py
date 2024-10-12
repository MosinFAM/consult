from django.urls import path
from tests.views import test_detail, course_final_test, test_welcome, test_result


urlpatterns = [
    path('<int:course_id>/<int:article_id>/<int:test_id>/welcome/', test_welcome, name='test_welcome'),
    path('<int:course_id>/<int:article_id>/<int:test_id>/', test_detail, name='test_detail'),
    path('<int:course_id>/<int:article_id>/<int:test_id>/result/', test_result, name='test_result'),
    path('<int:course_id>/final/', course_final_test, name='course_final_test'),
]
