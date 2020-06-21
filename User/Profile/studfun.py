from User.models import User, Subject, Student, ClassRoom
from django.shortcuts import get_object_or_404
from Quiz.models import Quiz, Answers
from Question.models import Question
from Report.models import ReportStudent

def ClassRank(user, theclass, subject):
    response = {}
    student_user = get_object_or_404(User, username=user)
    if not student_user:
        response['response'] = 'user {} is not exist'.format(user)
    student = get_object_or_404(Student, user=student_user)
    if not student:
        response['response'] = 'student {} is not exist'.format(user)
    classRoom = get_object_or_404(ClassRoom, name=theclass)
    if not classRoom:
        response['response'] = 'student {} not listed at any classes'.format(user)
    specific_subject = get_object_or_404(Subject, name=subject)
    if not specific_subject:
        response['response'] = 'student {} has no subject named {}'.format(user, subject)
    userPoints = 0
    userAnswers = Answers.objects.filter(amswers_author=student, answer_subject=specific_subject)
    for ans in userAnswers:
        userPoints += ans.answers_points

    allStudentInSpecificClass = Student.objects.filter(class_room=classRoom)
    allStudentAnswersInSpecificClassWithSpecificSubject = Answers.objects.filter(answer_class_room=classRoom, answer_subject=specific_subject)
    listOfStudentPoints = []
    for stud in allStudentInSpecificClass:
        studentPoints = 0
        for ans in allStudentAnswersInSpecificClassWithSpecificSubject:
            if ans.amswers_author == stud:
                studentPoints += ans.answers_points
        listOfStudentPoints.append(str(studentPoints))

    allStudentInSpecificGrade = Student.objects.filter(grade=student.grade)
    allStudentAnswersInSpecificGradeWithSpecificSubject = Answers.objects.filter(answer_grade=student.grade, answer_subject=specific_subject)
    listOfStudentPointsR = []
    for stud in allStudentInSpecificGrade:
        studentPointsR = 0
        for ans in allStudentAnswersInSpecificGradeWithSpecificSubject:
            if ans.amswers_author == stud:
                studentPointsR += ans.answers_points
        listOfStudentPointsR.append(str(studentPoints))
    
    
    studentRankInClass = listOfStudentPoints.index(str(userPoints))
    studentRankInGrade = listOfStudentPointsR.index(str(userPoints))
    response['subject name'] = '{}'.format(subject)
    response['student_rank_in_class'] = '{}'.format(studentRankInClass + 1)
    response['student_rank_in_grade'] = '{}'.format(studentRankInGrade + 1)
    
    return response


    
    
        