# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question, AnswerOption, StudentQuizAttempt, StudentAnswer
from .forms import QuizForm, QuestionFormSet, QuestionForm
from module_group.models import ModuleGroup
from datetime import datetime

def quiz_list(request):
    quizzes = Quiz.objects.all()
    module_groups = ModuleGroup.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes, 'module_groups':module_groups})

def quiz_create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False) 
            quiz.created_by = request.user  
            quiz.save()  
            return redirect('quiz:quiz_list')
    else:
        form = QuizForm()
    return render(request, 'quiz_create.html', {'form': form})

def quiz_delete(request, quiz_id):
    # Get the quiz object or return a 404 if not found
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == "POST":
        # Delete the quiz
        quiz.delete()
        
        # Redirect back to the quiz list after deletion
        return redirect('quiz:quiz_list')

    # Render a confirmation page if needed
    return render(request, 'quiz_delete.html', {'quiz': quiz})

def quiz_edit(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz:quiz_list')
    else:
        form = QuizForm(instance=quiz)
    
    return render(request, 'quiz_edit.html', {'form': form, 'quiz': quiz})



def quiz_question_list(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    
    return render(request, 'quiz_question_list.html', {'quiz': quiz, 'questions': questions})

def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question_types = ["Multiple Choice", "True/False"]  # Example types

    if request.method == "POST":
        question_id = request.POST.get('question_id')
        question_text = request.POST.get('question_text')
        question_type = request.POST.get('question_type')
        points = request.POST.get('points')

        # Validate that the Question ID is unique for this quiz
        if Question.objects.filter(quiz=quiz, id=question_id).exists():
            return render(request, 'quiz/add_question.html', {
                'quiz': quiz,
                'question_id': question_id,
                'question_types': question_types,
                'error': "Question ID must be unique."
            })

        # Create a new question instance
        Question.objects.create(
            quiz=quiz,
            id=question_id,  
            question_text=question_text,
            question_type=question_type,
            points=points
        )

        return redirect('quiz:quiz_question_list', quiz_id=quiz.id)

    context = {
        'quiz': quiz,
        'question_id': '',  # Start empty for user input
        'question_types': question_types,
    }

    return render(request, 'add_question.html', context)


def question_edit(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    question = get_object_or_404(Question, id=question_id)
    question_types = ["Multiple Choice", "True/False"]  # Replace with your actual question types

    if request.method == 'POST':
        new_question_id = request.POST.get('question_id')
        question_text = request.POST.get('question_text')
        question_type = request.POST.get('question_type')
        points = request.POST.get('points')

        # Validate that the Question ID is unique for this quiz
        if new_question_id != str(question.id) and Question.objects.filter(quiz=quiz, id=new_question_id).exists():
            return render(request, 'question_edit.html', {
                'quiz': quiz,
                'question': question,
                'question_types': question_types,
                'error': "Question ID must be unique."
            })

        # Update the question instance
        question.id = new_question_id  # Update ID if necessary
        question.question_text = question_text
        question.question_type = question_type
        question.points = points
        question.save()

        return redirect('quiz:quiz_question_list', quiz_id=quiz.id)

    # Pass the current question ID to the context for pre-filling
    context = {
        'quiz': quiz,
        'question': question,
        'question_types': question_types,
        'question_id': question.id,  # Pre-fill with existing ID
    }

    return render(request, 'question_edit.html', context)


def question_delete(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        question.delete()
        return redirect('quiz:quiz_question_list', quiz_id=question.quiz.id)

    return render(request, 'question_delete.html', {'question': question})


def answer_list(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = AnswerOption.objects.filter(question=question)

    return render(request, 'answer_list.html', {
        'question': question,
        'answers': answers,
    })

def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        answer_texts = request.POST.getlist('answer_text[]')
        is_corrects = request.POST.getlist('is_correct')  # Không thêm dấu [] ở đây

        for index, answer_text in enumerate(answer_texts):
            # Kiểm tra nếu câu trả lời tương ứng có được đánh dấu là đúng hay không
            is_correct = str(index) in is_corrects  # Kiểm tra nếu index nằm trong danh sách

            AnswerOption.objects.create(
                question=question,
                option_text=answer_text,
                is_correct=is_correct
            )

        return redirect('quiz:answer_list', question.id)

    return render(request, 'add_answer.html', {'question': question})

def answer_delete(request, answer_id):
    answer = get_object_or_404(AnswerOption, id=answer_id)
    question_id = answer.question.id  # Get the question ID for redirection
    answer.delete()  
    return redirect('quiz:answer_list', question_id=question_id)


def answer_edit(request, answer_id):
    answer = get_object_or_404(AnswerOption, id=answer_id)
    question_id = answer.question.id  # Get the question ID for redirection

    if request.method == 'POST':
        # Get data from the form
        option_text = request.POST.get('option_text')
        is_correct = request.POST.get('is_correct') == 'on'  # Checkbox value

        # Update the answer
        answer.option_text = option_text
        answer.is_correct = is_correct
        answer.save()

        # Redirect to the list of answers for the question
        return redirect('quiz:answer_list', question_id=question_id)

    # Return the template with the answer's data
    return render(request, 'answer_edit.html', {'answer': answer})


def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()

    # Track the start time of the quiz
    start_time = request.session.get(f'quiz_{quiz_id}_start_time')
    if not start_time:
        request.session[f'quiz_{quiz_id}_start_time'] = str(datetime.now())

    if request.method == "POST":
        # Calculate the time taken by the student
        start_time = datetime.fromisoformat(request.session.get(f'quiz_{quiz_id}_start_time'))
        time_taken = (datetime.now() - start_time).seconds // 60  # Time in minutes
        del request.session[f'quiz_{quiz_id}_start_time']  # Clear start time after submission

        # Create a new attempt
        attempt = StudentQuizAttempt.objects.create(
            user=request.user, 
            quiz=quiz, 
            score=0,  # Initial score
            time_taken=time_taken
        )

        # Loop through each question and save the answers
        for question in questions:
            selected_option_id = request.POST.get(f"question_{question.id}")
            selected_option = get_object_or_404(AnswerOption, id=selected_option_id)
            answer = StudentAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=selected_option
            )

        # Call the AI grading function (see below)
        score = grade_quiz(attempt)

        # Update the score for the attempt
        attempt.score = score
        attempt.save()

        # Redirect after completing the quiz
        return redirect('quiz:quiz_result', quiz_id=quiz.id, attempt_id=attempt.id)

    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions, 'time_limit': quiz.time_limit})


def grade_quiz(attempt):
    correct_answers = 0
    total_questions = attempt.studentanswer_set.count()

    for answer in attempt.studentanswer_set.all():
        if answer.selected_option.is_correct:
            correct_answers += 1

    # Calculate score (e.g., 1 point for each correct answer)
    return (correct_answers / total_questions) * 100 if total_questions > 0 else 0


def quiz_result(request, quiz_id, attempt_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempt = get_object_or_404(StudentQuizAttempt, id=attempt_id)
    student_answers = StudentAnswer.objects.filter(attempt=attempt)

    # Can add AI grading feedback if needed
    return render(request, 'quiz_result.html', {
        'quiz': quiz,
        'student_answers': student_answers,
        'attempt': attempt,
    })
