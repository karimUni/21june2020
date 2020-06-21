from django.urls import path
from Quiz.student.views import listAllStudentQuizs, quizResponse, checkQuizTime
from Quiz.teacher.views import newQuiz, appendQuestionsToQuiz, listQuestions, saveQuiz, launchQuiz, listLaunchedQuiz, listUnLaunchedQuiz, detailQuiz, createQuestion, createQuestion2, createRate, viewRates, listTeacherQuestions, listNotTeacherQuestions
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('quiz/student/quiz/list/', listAllStudentQuizs, name='quizStudentList'),
    path('quiz/student/quiz/checktime/<int:quiz_id>', checkQuizTime, name='checktime'),
    path('quiz/student/quiz/start/', quizResponse, name='quizstart'),
    # 
    path('quiz/teacher/create/', newQuiz, name='quizTeacherCreate'),
    path('quiz/teacher/questions/list/', listQuestions, name='QuestionsList'),
    path('quiz/teacher/append/', appendQuestionsToQuiz, name='quizTeacherAppend'),
    path('quiz/teacher/save/<int:quiz_id>/', saveQuiz, name='quizTeacherSave'),
    path('quiz/teacher/launch/<int:quiz_id>/<str:quiz_launch_time>/<str:quiz_class_room>/', launchQuiz, name='quizTeacherLaunch'),
    path('quiz/teacher/list/launched/', listLaunchedQuiz, name='quizTeacherListLaunched'),
    path('quiz/teacher/list/unlaunched/', listUnLaunchedQuiz, name='quizTeacherListUnLaunched'),
    path('quiz/teacher/perview/<int:quiz_id>/' ,detailQuiz, name='quizTeacherPerview'),
    # 
    path('questions/create/mcq/', createQuestion, name='qustionCreateMcq'),
    path('questions/create/tfq/', createQuestion2, name='questionCreateTR'),
    path('questions/review/create/<int:question_id>/', createRate, name='createReview'),
    path('questions/review/view/<int:question_id>/', viewRates, name='viewReviews'),
    path('questions/teacher/list/', listTeacherQuestions, name='listTeacherQuestions'),
    path('questions/Noteacher/list/', listNotTeacherQuestions, name='listNotTeacherQuestions'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
