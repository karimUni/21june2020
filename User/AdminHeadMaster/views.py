from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from User.models import User, HeadMaster, Teacher, Subject , ClassRoom , Student , Parent
from rest_framework import status
from rest_framework.authtoken.models import Token
from User.AdminHeadMaster.serializers import (
     UserSerializer , TeacherSerializer , SubjectSerializer , ClassRoomSerializer,
     StudentSerializer , ParentSerializer
)
from User.decorators import headMaster_role

#add subject view
@api_view(['POST',])
@headMaster_role
def add_subject_view(request):
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        educational_type = head.educational_type
        if request.method == 'POST':
            serializer = SubjectSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(educational_type=educational_type)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'response' : 'you dont have permission to add subject'})

#list subject view
@api_view(['GET',])
@headMaster_role
def subject_list_view(request):
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        educational_type = head.educational_type
        subject = Subject.objects.filter(educational_type=educational_type)
        if request.method == 'GET':
            serializer = SubjectSerializer(subject , many=True)
            return Response(serializer.data)
    else:
        return Response({'response' : 'you dont have permission to list subjects data'})

#view specific subject 
@api_view(['GET',]) 
@headMaster_role
def subject_detail_view(request,id):
    subject = get_object_or_404(Subject,id=id)
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        if request.method == 'GET':
            serializer = SubjectSerializer(subject)
            return Response(serializer.data)
    else:
        return Response({'response' : 'you dont have permission to see specific subject'})


############################################################
        ###### class Room Views
# Add Class Room Serializer
@api_view(['POST',])
@headMaster_role
def add_class_room_view(request):
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        uni_code = head.uni_code
        if request.method == 'POST':
            serializer = ClassRoomSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(uni_code=uni_code)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'response' : 'you dont have permission to add class rooms in the school'})

# list all school class rooms view
@api_view(['GET',])
@headMaster_role
def class_list_view(request):
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        uni_code = head.uni_code
        class_room = ClassRoom.objects.filter(uni_code=uni_code)
        if request.method == 'GET':
            serializer = ClassRoomSerializer(class_room , many=True)
            return Response(serializer.data)
    else:
        return Response({'response' : 'you dont have permission to list school class rooms'})
    
# View Specefic Class Room in the school
@api_view(['GET',]) 
@headMaster_role
def class_room_detail_view(request,id):
    class_room = get_object_or_404(ClassRoom,id=id)
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        if request.method == 'GET':
            serializer = ClassRoomSerializer(class_room)
            return Response(serializer.data)
    else:
        return Response({'response' : 'you dont have permission to see class room data'})

################################################################
      ######### Teacher View Apis
#Add Teacher View Api
@api_view(['POST',])
@headMaster_role
def add_teacher_view(request):
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        uni_code = head.uni_code
        if request.method == 'POST':
            request.data['uni_code'] = uni_code
            serializer = TeacherSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'response' : 'you dont have permission to add teacher'})

#list Teacher View Api
@api_view(['GET',])
@headMaster_role
def list_teachers_view(request):
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        uni_code = head.uni_code
        teacher = Teacher.objects.filter(uni_code = uni_code)
        if request.method == 'GET':
            serializer = TeacherSerializer(teacher, many=True)
            return Response(serializer.data)
    else:
        return Response({'response' : 'you dont have permission to list teachers data'})

#show specific teacher data api
@api_view(['GET',]) 
@headMaster_role
def teacher_detail_view(request,id):
    teacher = get_object_or_404(Teacher,id=id)
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        if request.method == 'GET':
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
    else:
        return Response({'response' : 'you dont have permission to view teacher data'})

################################################################
      ######### Student View Apis
#Add Student View Api
@api_view(['POST',])
@headMaster_role
def add_student_view(request):
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        uni_code = head.uni_code
        if request.method == 'POST':
            request.data['uni_code'] = uni_code
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'response' : 'you dont have permission to add Student'})

#list students view
@api_view(['GET',])
@headMaster_role
def list_students_view(request):
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        uni_code = head.uni_code
        student = Student.objects.filter(uni_code = uni_code)
        if request.method == 'GET':
            serializer = StudentSerializer(student, many=True)
            return Response(serializer.data)
    else:
        return Response({'response' : 'you dont have permission to see Students'})

#show specific student data api
@api_view(['GET',]) 
@headMaster_role
def student_detail_view(request,id):
    student = get_object_or_404(Student,id=id)
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        if request.method == 'GET':
            serializer = StudentSerializer(student)
            return Response(serializer.data)
    else:
        return Response({'response' : 'you dont have permission to see Student data '})

################################################################
      ######### Parent View Apis
#Add Parent View Api
@api_view(['POST',])
@headMaster_role
def add_parent_view(request):
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        uni_code = head.uni_code
        if request.method == 'POST':
            request.data['uni_code'] = uni_code
            serializer = ParentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'response' : 'you dont have permission to add Parent'})

#view parents list view
@api_view(['GET',])
@headMaster_role
def list_parents_view(request):
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        uni_code = head.uni_code
        parent = Parent.objects.filter(uni_code = uni_code)
        if request.method == 'GET':
            serializer = ParentSerializer(parent, many=True)
            return Response(serializer.data)
    else:
        return Response({'response' : 'you dont have permission to see Parents data'})

#show specific parent data api
@api_view(['GET',]) 
@headMaster_role
def parent_detail_view(request,id):
    parent = get_object_or_404(Parent,id=id)
    user = request.user
    head = HeadMaster.objects.get(user=user)
    if head:
        if request.method == 'GET':
            serializer = ParentSerializer(parent)
            return Response(serializer.data)
    else:
        return Response({'response' : 'you dont have permission to see parent data '})