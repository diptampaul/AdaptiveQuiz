from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Quiz
from questions.models import Question, Answer
from results.models import Result
from django.views.generic import ListView
from django.http import JsonResponse

# Create your views here.


def index(request):
    return render(request, 'home.htm', {})


def dashboard(request):
    user = request.user
    model = Quiz
    try:
        result_data = Result.objects.filter(user=user)[::-1]
        #d = []
        # for data in result_data:
        #    d.append(data.score)
    except:
        result_data = None

    return render(request, 'index.htm', {'user_auth': 'none', 'result_data': result_data})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Validating username and password from database, if wrong, then it will return None
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            # return render(request, 'quizes/main.htm')
            return redirect('quiz')
        else:
            messages.error(request, 'Invalid Credential')
            return redirect('login')

    else:
        return render(request, 'index.htm', {'user_auth': 'login'})
    # return render(request, 'index.htm', {'user_auth': 'login'})


def register(request):
    # If the user submit the form, the request will be POST
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if confrim password is matching or not
        if password2 == password:

            # check username exhists in database or not
            if User.objects.filter(username=username).exists():
                print('Username Exists')
                # But we need to send the error message to the front end too, so that the user can see it
                messages.info(request, 'Username Taken')
                # Return to register page if usrname is wrong
                return redirect('register')

            # Checking email exists or not
            elif User.objects.filter(email=email).exists():
                print('Email id exists')
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()

                # now redirect to the Home Page
                return redirect('login')

        else:
            messages.info(request, 'Password Ubmatched')
            print('Password not matched')
            return redirect('register')

    # Else it will be GET
    else:
        return render(request, 'index.htm')


def logout(request):
    auth.logout(request)
    return redirect('dashboard')


class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.htm'


def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.htm', {'obj': quiz})


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    info = Question.objects.all()
    difficulty = []
    correct_answer = []

    for i in info:
        # print(i)
        # Adding difficulty level
        difficulty.append(i.difficulty)

        # Adding correct answer
        # print(i.text)
        all_answers = Answer.objects.all()
        for a in all_answers:
            if a.correct:
                correct_answer.append(a.answer)
    correct_answer = correct_answer[:len(difficulty)]

    for q in quiz.get_question():
        answers = []
        for a in q.get_answer():
            answers.append(a.answer)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.time,
        'number_of_questions': quiz.number_of_questions,
        'difficulty': difficulty,
        'correct_answer': correct_answer,
    })


def save_quiz_view(request, pk):
    # print(request.POST)
    if request.is_ajax():
        questions = []
        data = request.POST
        data = dict(data.lists())
        data.pop('csrfmiddlewaretoken')
        for k in data.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        # print(questions)
        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_ans = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            # print(a_selected)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.answer:
                        if a.correct:
                            score += 1
                            correct_ans = a.answer
                    else:
                        if a.correct:
                            correct_ans = a.answer

                results.append(
                    {str(q): {'correct_answer': correct_ans, 'answered': a_selected}})

            else:
                results.append(
                    {str(q): {'correct_answer': correct_ans, 'answered': 'not answered'}})

        score_ = float("{:.2f}".format(score * multiplier))
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score:
            return JsonResponse({'passed': True, 'score': score_, 'results': results})
        else:
            return JsonResponse({'passed': False, 'score': score_, 'results': results})

    return JsonResponse({'passed': False, 'score': None, 'results': None})
