from django.shortcuts import render , get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from User.decorators import teacher_role 
from User.models import Teacher ,Student , ClassRoom
from rest_framework import status
from Quiz.models import Quiz , Answers
from django.db.models import Count , Sum
from .serializers import getAllStudents, getAllClasses
from django.db.models import Q
from Question.models import MCQ, TR, Question


@api_view(['GET'])
@teacher_role
def get_all_students(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    students = Student.objects.filter(level=teacher.level)
    serializer = getAllStudents(students, many=True)
    return Response({'data': serializer.data}, 200)


@api_view(['GET'])
@teacher_role
def get_all_classes(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    quizes = Quiz.objects.all()
    serializer = getAllClasses(quizes, many=True)
    return Response({'data': serializer.data}, 200)


@api_view(['POST'])
@teacher_role
def genirate_student_report(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    studntID = request.data.get('id')
    timeFrom = request.data.get('time_from')
    timeTo = request.data.get('time_to')
    student = get_object_or_404(Student, id=studntID)
    quizs = Quiz.objects.filter(Q(quiz_creation_time__gte=timeFrom)|Q(quiz_creation_time__lte=timeTo), quiz_grade=student.grade, quiz_subject=teacher.subject)
    datalist = []
    datelist = []
    comulativeGrade = 0
    points = 0
    for quiz in quizs:
        theAnswer = Answers.objects.filter(amswers_author=student, answers_quiz=quiz)
        for answer in theAnswer:
            points += int(answer.answers_points)
        if theAnswer.count() < 1:
            comulativeGrade = 0
        else:
            comulativeGrade = (points * 100) / int(theAnswer.count())
        datelist.append(quiz.quiz_creation_time.date())
        datalist.append(comulativeGrade)
    return Response({'dates': datelist,
                    'marks': datalist,
                    'subject': teacher.subject.name,
                    'schoolid': teacher.uni_code,
                    'grade': student.class_room.name,
                    'time_from': timeFrom.split('T')[0],
                    'time_to': timeTo.split('T')[0]}, 200)


@api_view(['POST'])
@teacher_role
def genirate_class_report(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    quizId = request.data.get('id')
    className = request.data.get('class_name')
    class_room = get_object_or_404(ClassRoom, name=className)
    quiz = Quiz.objects.get(id=quizId, quiz_class_room=class_room)
    if not quiz:
        return Response({'detail': 'not found'}, 404)
    allStudentsInClass = Student.objects.filter(class_room=class_room)
    dataPerAllStudent = []
    for stud in allStudentsInClass:
        answers = Answers.objects.filter(amswers_author=stud)
        studentAns = []
        score = 0
        que = None
        comulativeGrade = 0
        for ans in answers:
            score += ans.answers_points
            quesData = None
            questtion = None
            if ans.answers_questions.all()[0].question_type == 'MCQ':
                questtion = get_object_or_404(MCQ, question=ans.answers_questions.all()[0])
                quesData = {
                    'question_type': ans.answers_questions.all()[0].question_type,
                    'choice_A': questtion.choice_A,
                    'choice_B': questtion.choice_B,
                    'choice_C': questtion.choice_C,
                    'choice_D': questtion.choice_D,
                    'question_answer': questtion.question_answer,
                    'student_answer': ans.answer,
                }
            else:
                questtion = get_object_or_404(TR, question=ans.answers_questions.all()[0])
                quesData = {
                    'question_type': ans.answers_questions.all()[0].question_type,
                    'question_answer': questtion.question_answer,
                    'student_answer': ans.answer,
                }
            studentAns.append(quesData)
        comulativeGrade = (score * 100) / int(quiz.quiz_questions.count())
        dataPerAllStudent.append({'student': stud.user.name,
        'score': comulativeGrade,
        'questions': studentAns})
    return Response({'data': dataPerAllStudent}, 200)
















# #get the student data from the teacher id and subject
# @api_view(['GET',])
# @teacher_role
# def get_student_report(request):
#     student_id = request.query_params.get('student_id',None)
#     start_date = request.query_params.get('start_date',None)
#     end_date = request.query_params.get('end_date',None)
#     user = request.user
#     teacher = get_object_or_404(Teacher,user=user)
#     subject = teacher.subject
#     if student_id and start_date and end_date:
#         student = get_object_or_404(Student , id=student_id)
#         # student_answares = Answers.objects.filter(answers_author=student, answer_creation_time__gte=start_date)
#         # student_quizes = Quiz.objects.filter(id__in=student_answares,quiz_author=teacher)
        
#         # student_quizes_grades = Answers.objects.filter(answers_author=student,answer_subject=subject,answer_creation_time__gte=start_date).values('answers_author__id','answers_author__user__username',
#         #                         'answer_subject__name','answers_quiz__id','answers_quiz__quiz_author__id','answers_points').annotate(Sum('answers_points'))
#         student_quizes_grades = Answers.objects.filter(answers_author=student,answer_subject=subject,answer_creation_time__gte=start_date).values('answers_author__id','answers_author__user__username',
#                                  'answer_subject__name','answers_author__class_room__name','answers_quiz__id','answers_quiz__quiz_author__id','answers_points').annotate(Sum('answers_points'))
        
#         OverallGrade = student_quizes_grades.aggregate(total_score=Sum('answers_points'))
#         print(OverallGrade)
#         # student_degress= []
#         # for degree in student_quizes_grades:
#         #     print(Sum(degree.answers_points))
        
#         # print(student_degress)
#         # query = Answers.objects.values('answers_points').annotate(Count('answers_points'))
       
#         #print(student_quizes)
#         return Response({'student_data':student_quizes_grades,'OverallGrade': OverallGrade})
#     else:
#         return Response({'Error' : 'Data not valid'},status=status.HTTP_400_BAD_REQUEST)


# # #get the teacher for class
# # @api_view(['GET',])
# # @teacher_role
# # def get_class_report(request):
# #     user = request.user
# #     teacher = get_object_or_404(Teacher,user=user)
# #     teacher_classes = Teacher.objects.get(id=teacher.id).class_rooms.all()


# #     mylist =[]
# #     for room in teacher_classes:
# #         classes = {}
# #         numbers = room.student_class.all().count()
# #         quizes = room.quiz_class.all()
# #         classes['class'] = room.name
# #         classes['Students']= numbers
# #         for quiz in quizes:
# #             # print(quiz.quiz_id)
# #             # print(quiz.quiz_creation_time)
# #             # print(quiz.quiz_questions)
# #             classes['quiz'] = quiz.quiz_id
# #             classes['Date'] = quiz.quiz_creation_time
# #             quiestions=quiz.quiz_questions.all().count()
# #             classes['questions'] = quiestions
# #         mylist.append(classes)
# #     # print(mylist)
# #     return Response(mylist)



# @api_view(['GET',])
# @teacher_role
# def get_class_quizes(request):
#     user = request.user
#     teacher = get_object_or_404(Teacher,user=user)
#     teacher_classes = teacher.class_rooms.all()
#     # quizes = Quiz.objects.filter(id__in=teacher_classes)
#     quizes = ClassRoom.objects.all()
#     serializer = ClassRoomSerilizer(teacher_classes,many=True)
#     # print(quizes)
#     return Response(serializer.data)

# @api_view(['GET',])
# @teacher_role
# def generate_report_class(request):
#     quiz_id = request.query_params.get('quiz_id',None)
#     user = request.user
#     teacher = get_object_or_404(Teacher,user=user)
#     if quiz:
#         quiz = Quiz.objects.get(quiz_id=quiz_id)
#         student_answers=quiz.quiz_answers.all()

#         student_quizes_grades = Answers.objects.filter(answers_quiz=quiz).values('answers_quiz__quiz_id','answers_author__user__username',
#                                     'answer_subject__name','answers_author__class_room__name','answers_points','answers_quiz__quiz_creation_time').annotate(Sum('answers_points'))

#         print(student_quizes_grades)
#     # serializer = AnswersSerilaizer(student_answers)
#     # print(serializer.data)
#         return Response({'class_data':student_quizes_grades})
#     # if quiz:
#     #     class_student = Answers.objects.filter(answers_quiz=1)
#     #     print(class_student)
#     #     return Response('working')
#     else:
#         return Response({'Error' : 'Data not valid'},status=status.HTTP_400_BAD_REQUEST)