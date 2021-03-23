from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('quiz', views.QuizListView.as_view(), name='quiz'),
    path('quiz/<pk>/', views.quiz_view, name='quiz-id-view')
]
