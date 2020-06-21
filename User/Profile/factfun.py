from User.models import User, Subject, Teacher
from django.shortcuts import get_object_or_404
from Quiz.models import Quiz
from Question.models import Question, Rate
from Report.models import ReportStudent


# function to get teacher ranks in question
def QuestionRank(user, subject):
    teacher_user = get_object_or_404(User, username=user)
    response = {}
    listOfNumQues = []
    listOfNumQuesSchool = []
    if not teacher_user:
        response['response'] = 'user {} is not exist'.format(user)
    teacher = get_object_or_404(Teacher, user=teacher_user)
    if not teacher:
        response['response'] = 'teacher {} is not exist'.format(user)
    NumOfTQues = Question.objects.filter(question_author=teacher).count() #1 number of teacher questions
    if NumOfTQues < 1:
        response['teacher_questions'] = '0'
    response['teacher_questions'] = '{}'.format(NumOfTQues)
    teacher_subject = get_object_or_404(Subject, name=subject)
    if not teacher_subject:
        response['response'] = 'subject {} is not exist'.format(subject)
    NumOfSQues = Question.objects.filter(question_subject=teacher_subject).count() #2 number of subject questions 
    if NumOfSQues < 1:
        response['subject_questions'] = '0'
    response['subject_questions'] = '{}'.format(NumOfSQues)
    NumOfScQues = Question.objects.all().count() #3 number of school questions
    if NumOfScQues < 1:
        response['school_questions'] = '0'
    response['school_questions'] = '{}'.format(NumOfScQues)
    # Ranks is bellow
    teachers = Teacher.objects.all()
    for te in teachers:
        NumOfQuestions = Question.objects.filter(question_author=te, question_subject=teacher_subject).count()
        NumOfQuestionsSchool = Question.objects.filter(question_author=te).count()
        if NumOfQuestions < 1:
            listOfNumQues.append('0')
        listOfNumQues.append(str(NumOfQuestions))
        if NumOfQuestionsSchool < 1:
            listOfNumQuesSchool.append('0')
        listOfNumQuesSchool.append(str(NumOfQuestionsSchool))
    listOfNumQues.sort(reverse=True)
    listOfNumQuesSchool.sort(reverse=True)
    teacher_rank_in_subject = listOfNumQues.index(str(NumOfTQues))
    teacher_rank_in_school = listOfNumQuesSchool.index(str(NumOfTQues))
    response['in_subject_questions_rank'] = '{}'.format(teacher_rank_in_subject + 1)
    response['in_school_questions_rank'] = '{}'.format(teacher_rank_in_school + 1)

    return response


# function to get teacher ranks in review
def ReviewRank(user, subject):
    teacher_user = get_object_or_404(User, username=user)
    response = {}
    listOfNumQues = []
    listOfNumQuesSchool = []
    if not teacher_user:
        response['response'] = 'user {} is not exist'.format(user)
    teacher = get_object_or_404(Teacher, user=teacher_user)
    if not teacher:
        response['response'] = 'teacher {} is not exist'.format(user)
    NumOfTRate = Rate.objects.filter(author=teacher).count() #1 number of teacher reviews
    if NumOfTRate < 0:
        response['teacher_reviews'] = '0'
    response['teacher_reviews'] = '{}'.format(NumOfTRate)
    teacher_subject = get_object_or_404(Subject, name=subject)
    if not teacher_subject:
        response['response'] = 'subject {} is not exist'.format(subject)
    NumOfSRate = Rate.objects.filter(subject=teacher_subject).count() #2 number of school reviews
    if NumOfSRate < 1:
        response['subject_reviews'] = '0'
    response['subject_reviews'] = '{}'.format(NumOfSRate)
    NumOfScRate = Rate.objects.all().count() #3 number of school reviews
    if NumOfScRate < 1:
        response['school_reviews'] = '0'
    response['school_reviews'] = '{}'.format(NumOfScRate)
    # Ranks is bellow
    teachers = Teacher.objects.all()
    for te in teachers:
        NumOfQuestions = Rate.objects.filter(author=te, subject=teacher_subject).count()
        NumOfQuestionsSchool = Rate.objects.filter(author=te).count()
        if NumOfQuestions < 1:
            listOfNumQues.append('0')
        listOfNumQues.append(str(NumOfQuestions))
        if NumOfQuestionsSchool < 1:
            listOfNumQuesSchool.append('0')
        listOfNumQuesSchool.append(str(NumOfQuestionsSchool))
    listOfNumQues.sort(reverse=True)
    listOfNumQuesSchool.sort(reverse=True)
    teacher_rank_in_subject = listOfNumQues.index(str(NumOfTRate))
    teacher_rank_in_school = listOfNumQuesSchool.index(str(NumOfTRate))
    response['in_subject_reviews_rank'] = '{}'.format(teacher_rank_in_subject + 1)
    response['in_school_reviews_rank'] = '{}'.format(teacher_rank_in_school + 1)

    return response


# function to get teacher ranks in launch quiz
def LaunchRank(user, subject):
    teacher_user = get_object_or_404(User, username=user)
    response = {}
    listOfNumQues = []
    listOfNumQuesSchool = []
    if not teacher_user:
        response['response'] = 'user {} is not exist'.format(user)
    teacher = get_object_or_404(Teacher, user=teacher_user)
    if not teacher:
        response['response'] = 'teacher {} is not exist'.format(user)
    NumOfTLaunch = Quiz.objects.filter(quiz_author=teacher, quiz_is_launched=True).count() #1 number of teacher reviews
    if NumOfTLaunch < 0:
        response['teacher_launch'] = '0'
    response['teacher_launch'] = '{}'.format(NumOfTLaunch)
    teacher_subject = get_object_or_404(Subject, name=subject)
    if not teacher_subject:
        response['response'] = 'subject {} is not exist'.format(subject)
    NumOfSLaunch = Quiz.objects.filter(quiz_subject=teacher_subject, quiz_is_launched=True).count() #2 number of school reviews
    if NumOfSLaunch < 1:
        response['subject_launch'] = '0'
    response['subject_launch'] = '{}'.format(NumOfSLaunch)
    NumOfScLaunch = Quiz.objects.filter(quiz_is_launched=True).count() #3 number of school reviews
    if NumOfScLaunch < 1:
        response['school_launch'] = '0'
    response['school_launch'] = '{}'.format(NumOfScLaunch)
    # Ranks is bellow
    teachers = Teacher.objects.all()
    for te in teachers:
        NumOfQuestions = Quiz.objects.filter(quiz_author=te, quiz_subject=teacher_subject, quiz_is_launched=True).count()
        NumOfQuestionsSchool = Quiz.objects.filter(quiz_author=te, quiz_is_launched=True).count()
        if NumOfQuestions < 1:
            listOfNumQues.append('0')
        listOfNumQues.append(str(NumOfQuestions))
        if NumOfQuestionsSchool < 1:
            listOfNumQuesSchool.append('0')
        listOfNumQuesSchool.append(str(NumOfQuestionsSchool))
    listOfNumQues.sort(reverse=True)
    listOfNumQuesSchool.sort(reverse=True)
    teacher_rank_in_subject = listOfNumQues.index(str(NumOfTLaunch))
    teacher_rank_in_school = listOfNumQuesSchool.index(str(NumOfTLaunch))
    response['in_subject_launch_rank'] = '{}'.format(teacher_rank_in_subject + 1)
    response['in_school_launch_rank'] = '{}'.format(teacher_rank_in_school + 1)

    return response


# function to get teacher ranks in reports
def ReportRank(user, subject):
    teacher_user = get_object_or_404(User, username=user)
    response = {}
    listOfNumQues = []
    listOfNumQuesSchool = []
    if not teacher_user:
        response['response'] = 'user {} is not exist'.format(user)
    teacher = get_object_or_404(Teacher, user=teacher_user)
    if not teacher:
        response['response'] = 'teacher {} is not exist'.format(user)
    NumOfTLaunch = ReportStudent.objects.filter(report_creator=teacher).count() #1 number of teacher reviews
    if NumOfTLaunch < 0:
        response['teacher_report'] = '0'
    response['teacher_report'] = '{}'.format(NumOfTLaunch)
    teacher_subject = get_object_or_404(Subject, name=subject)
    if not teacher_subject:
        response['response'] = 'subject {} is not exist'.format(subject)
    NumOfSLaunch = ReportStudent.objects.filter(report_subject=teacher_subject).count() #2 number of school reviews
    if NumOfSLaunch < 1:
        response['subject_report'] = '0'
    response['subject_report'] = '{}'.format(NumOfSLaunch)
    NumOfScLaunch = ReportStudent.objects.all().count() #3 number of school reviews
    if NumOfScLaunch < 1:
        response['school_report'] = '0'
    response['school_report'] = '{}'.format(NumOfScLaunch)
    # Ranks is bellow
    teachers = Teacher.objects.all()
    for te in teachers:
        NumOfQuestions = ReportStudent.objects.filter(report_creator=te, report_subject=teacher_subject).count()
        NumOfQuestionsSchool = ReportStudent.objects.filter(report_creator=te).count()
        if NumOfQuestions < 1:
            listOfNumQues.append('0')
        listOfNumQues.append(str(NumOfQuestions))
        if NumOfQuestionsSchool < 1:
            listOfNumQuesSchool.append('0')
        listOfNumQuesSchool.append(str(NumOfQuestionsSchool))
    listOfNumQues.sort(reverse=True)
    listOfNumQuesSchool.sort(reverse=True)
    teacher_rank_in_subject = listOfNumQues.index(str(NumOfTLaunch))
    teacher_rank_in_school = listOfNumQuesSchool.index(str(NumOfTLaunch))
    response['in_subject_report_rank'] = '{}'.format(teacher_rank_in_subject + 1)
    response['in_school_report_rank'] = '{}'.format(teacher_rank_in_school + 1)

    return response