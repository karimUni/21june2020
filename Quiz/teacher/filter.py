# from django.shortcuts import render, redirect, get_object_or_404
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from User.decorators import teacher_role
# from Quiz.teacher.serializers import CreateNewQuiz, CreateMCQ, CreateQuestion, CreateTR, CreateRate
# from User.models import User, Teacher, Subject, ClassRoom
# from Quiz.models import Quiz
# from Question.models import Question, MCQ, TR, Rate
# import random



# # def filter(gradeID, topicID, addedBy, sortBy):
# #     questions = None
# #     if topicID != 'all' and addedBy != 'both' and sortBy != 'both':
# #         if addedBy == 'self' and sortBy == 'best':
# #             questions = Question.objects.filter(
# #                 question_grade=gradeID,
# #                 question_author=addedBy
# #             )


# if topicID != 'all' and addedBy != 'both' and sortBy != 'both' and qtype != 'both':
#         if addedBy == 'self' and sortBy == 'best':
#             questions = Question.objects.filter(
#                 question_grade=gradeID,
#                 question_author=teacher,
#                 question_topic=topicID,
#                 question_type=qtype,
#             )
#         elif addedBy == 'self' and sortBy == 'date':
#             questions = Question.objects.filter(
#                 question_grade=gradeID,
#                 question_author=teacher,
#                 question_topic=topicID,
#                 question_type=qtype,
#             ).order_by('-question_creation_time')
#         elif addedBy == 'school' and sortBy == 'best':
#             questions = Question.objects.filter(
#                 question_grade=gradeID,
#                 question_topic=topicID,
#                 question_type=qtype,
#             ).exclude(question_author=teacher)
#         else:
#             questions = Question.objects.filter(
#                 question_grade=gradeID,
#                 question_topic=topicID,
#                 question_type=qtype,
#             ).exclude(question_author=teacher).order_by('-question_creation_time')
#     elif topicID == 'all' and addedBy != 'both' and sortBy != 'both' and qtype != 'both':
#         if addedBy == 'self' and sortBy == 'best':
#             questions = Question.objects.filter(
#                 question_grade=gradeID,
#                 question_author=teacher,
#                 question_type=qtype,
#             )
#         elif addedBy == 'self' and sortBy == 'date':
#             questions = Question.objects.filter(
#                 question_grade=gradeID,
#                 question_author=teacher,
#                 question_type=qtype,
#             ).order_by('-question_creation_time')
#         elif addedBy == 'school' and sortBy == 'best':
#             questions = Question.objects.filter(
#                 question_grade=gradeID,
#                 question_type=qtype,
#             ).exclude(question_author=teacher)
#         else:
#             questions = Question.objects.filter(
#                 question_grade=gradeID,
#                 question_type=qtype,
#             ).exclude(question_author=teacher).order_by('-question_creation_time')
#     elif topicID == 'all' and addedBy != 'both' and sortBy != 'both' and qtype != 'both':