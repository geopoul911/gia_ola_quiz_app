from django.urls import path, re_path

from quiz import views

app_name = 'quiz'

# Sub app level mapping for endpoints
urlpatterns = [
    path('quizzes/', views.QuizDetailView.as_view(), name='quizzes'), # Used to retrieve the quiz when user clicks Play
    path('my-quizzes/', views.MyQuizListView.as_view(), name='myquizzes'), # Used to load list of completed quizzes when user clicks History
    path('save-answer/', views.SaveUserAnswer.as_view()), # Used to save a submitted answer when user clicks Next
    re_path(r'quizzes/(?P<slug>[\w\-]+)/$', views.QuizInfoView.as_view()), # Used to get data for a selected quiz from History view
    re_path(r"quizzes/(?P<slug>[\w\-]+)/submit/$", views.SubmitQuizView.as_view()), # Used to submit the quiz when the final question is answered
]
