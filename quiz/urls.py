from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('quiz', views.QuizListView.as_view(), name='quiz'),
    path('quiz/<pk>/', views.quiz_view, name='quiz-id-view'),
    path('quiz/<pk>/save/', views.save_quiz_view, name='save_view'),
    path('quiz/<pk>/data/', views.quiz_data_view, name='quiz-data-view'),
]
