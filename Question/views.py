from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Question, TR, MCQ
from User.models import Teacher
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import (
     QuestionSerializer ,  MCQSerializer
)


# Create your views here.
#add subject view
@api_view(['POST',])
# @permission_classes((IsAuthenticated,))
def add_question_view(request):
    user = request.user
    teacher = Teacher.objects.get(user=user)
    if teacher:
        question_author = teacher
        question_subject = teacher.subject
        if request.method == 'POST':
            serializer = QuestionSerializer(data=request.data)
            serializer2 = MCQSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                if serializer2.is_valid():
                    question = serializer.save()
                    data['question_type'] = user.question_type
                    data['question_author'] = question_author
                    data['question_grade'] = question.question_grade
                    data['question_subject'] = question_subject
                    data['question_topic'] = question.question_topic
                    mcq = serializer2.save(question)
                    data['question_head'] = mcq.question_head
                    data['question_body'] = mcq.question_body
                    data['choice_A'] = mcq.choice_A
                    data['choice_B'] = mcq.choice_B
                    data['choice_C'] = mcq.choice_C
                    data['choice_D'] = mcq.choice_D
                    data['question_answer'] = mcq.question_answer
                else:
                    data = serializer2.errors
            else:
                data = serializer.errors
            return Response(data)
    else:
        return Response({'response' : 'Teachers only have permissions to add questions'})
