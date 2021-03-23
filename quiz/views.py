from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Quiz
from django.views.generic import ListView

# Create your views here.


class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/main.htm'


def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'quizes/quiz.htm', {'obj': quiz})


def home(request):
    return render(request, 'index.htm', {'user_auth': 'none'})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #Validating username and password from database, if wrong, then it will return None
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            #return render(request, 'quizes/main.htm')
            return redirect('quiz')
        else:
            messages.error(request,'Invalid Credential')
            return redirect('login')

    else:
        return render(request, 'index.htm', {'user_auth': 'login'})
    #return render(request, 'index.htm', {'user_auth': 'login'})


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
    return redirect('/')
