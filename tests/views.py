from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Article, Test, Question, Answer, TestResult, OpenAnswer, Profile

@login_required
def test_detail(request, course_id, article_id, test_id):
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=article_id, course=course)
    test = get_object_or_404(Test, id=test_id, article=article)
    
    profile, created = Profile.objects.get_or_create(user=request.user)
    questions = test.questions.all()

    if request.method == 'POST':
        correct_answers = 0
        total_questions = questions.count()

        for question in questions:
            if question.question_type == 'multiple_choice':
                selected_answers = request.POST.getlist(f'question_{question.id}')
                correct_choices = question.answers.filter(is_correct=True).values_list('id', flat=True)

                if set(map(int, selected_answers)) == set(correct_choices):
                    correct_answers += 1

            elif question.question_type == 'text':
                user_answer = request.POST.get(f'question_{question.id}')
                correct_words = set(question.text_task.lower().split())
                user_words = set(user_answer.lower().split())
                
                OpenAnswer.objects.create(question=question, user=request.user, answer_text=user_answer)

                # Проверка на совпадение хотя бы 70% слов
                similarity_score = len(correct_words & user_words) / len(correct_words)
                if similarity_score > 0.7:  
                    correct_answers += 1

        score = int((correct_answers / total_questions) * 100)
        passed = score >= 70

        test_result, created = TestResult.objects.get_or_create(profile=profile, test=test)
        test_result.score = score
        test_result.total_questions = total_questions
        test_result.passed = passed
        test_result.attempts += 1
        test_result.best_score = max(test_result.best_score, score)
        test_result.save()

        return redirect('test_results', course_id=course_id, article_id=article_id, test_id=test_id)

    return render(request, 'tests/test_detail.html', {'course': course, 'article': article, 'test': test, 'questions': questions})

@login_required
def test_results(request, course_id, article_id, test_id):
    course = get_object_or_404(Course, id=course_id)
    article = get_object_or_404(Article, id=article_id, course=course)
    test = get_object_or_404(Test, id=test_id, article=article)
    
    profile = get_object_or_404(Profile, user=request.user)
    test_result = get_object_or_404(TestResult, profile=profile, test=test)

    return render(request, 'tests/test_results.html', {
        'course': course,
        'article': article,
        'test': test,
        'test_result': test_result,
    })
