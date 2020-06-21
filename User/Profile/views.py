# this views.py for only users profiles

from User.models import User, Teacher, Student, Parent, Student, ClassRoom, Subject, HeadMaster
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from User.Profile.factfun import QuestionRank, ReviewRank, LaunchRank, ReportRank
from User.Profile.studfun import ClassRank
from User.serializers import CreateStudent, CreateTeacher, RegisterationSerializer, UpdateProfileSerializer
from User.decorators import student_role, teacher_role, headMaster_role
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from Notification.models import XYZ



@api_view(['GET'])
@csrf_exempt
def base(request):
    user=request.user
    all_not = XYZ.objects.filter(message_receivers=user).count()
    return Response({
        'username': user.username,
        'name': '{} {}'.format(user.first_name, user.last_name),
        'image_path': user.avatar.url,
        'num_notifications': all_not, 
    }, 200)


# teacher profile
@api_view(['GET'])
@csrf_exempt
def dashBoard(request):
    user=request.user
    if user.role == 'T':
        teacher = get_object_or_404(Teacher, user=user)
        data1 = CreateTeacher(teacher)
        data2 = QuestionRank(user=user.username, subject=teacher.subject.name)
        data3 = ReviewRank(user=user.username, subject=teacher.subject.name)
        data4 = LaunchRank(user=user.username, subject=teacher.subject.name)
        data5 = ReportRank(user=user.username, subject=teacher.subject.name)
        return Response({
                    'user': data1.data,
                    'questions': data2,
                    'reviews': data3,
                    'launchs': data4,
                    'reports': data5
                }, 200  
            )
    elif user.role == 'S':
        student = get_object_or_404(Student, user=user)
        data1 = CreateStudent(student)
        data2 = {}
        nested_data = []
        for a in student.subjects.all():
            nested_data.append(ClassRank(user=user.username, theclass=student.class_room.name, subject=a.name))

        return Response(
            {
                'user': data1.data,
                'ranks': nested_data
            }, 200
        )
    else:
        return Response({'error': 'user dose not exist'}, 403)


# student profile
@api_view(['GET'])
@csrf_exempt
def profile(request):
    user = request.user
    first_name = RegisterationSerializer(user).data['first_name']
    last_name = RegisterationSerializer(user).data['last_name']
    email = RegisterationSerializer(user).data['email']
    phone_number = RegisterationSerializer(user).data['phone_number']
    image_profile = RegisterationSerializer(user).data['avatar']
    address = RegisterationSerializer(user).data['address']
    subjects = None
    classs = None
    if user.role == 'T':
        teacher = get_object_or_404(Teacher, user=user)
        subjects = CreateTeacher(teacher).data['subject']
        classs = CreateTeacher(teacher).data['class_rooms']
    elif user.role == 'S':
        student = get_object_or_404(Student, user=user)
        subjects = CreateStudent(student).data['subjects']
        classs = CreateStudent(student).data['class_room']

    return Response(
        {
            'name': '{} {}'.format(first_name, last_name),
            'email': email,
            'mobile': phone_number,
            'image_profile': image_profile,
            'address': address,
            'subjects': subjects,
            'classes': classs
        }, 200
    )


#update profile
@api_view(['PUT'])
@csrf_exempt
def update_profile(request):
    user = request.user
    if request.method == 'PUT':
        __name = request.data.get('name')
        _name = __name.split(' ')
        data0 = {
            'phone_number': request.data.get('mobile'),
            'address': request.data.get('address'),
            'avatar': request.data.get('image_profile'),
            'first_name': _name[0],
            'last_name': _name[1],
        }
        serializer = UpdateProfileSerializer(data=data0, instance=user)
        if serializer.is_valid():
            new_serializer = serializer.save()
            return Response({'success': 'profile updated successfully'}, 201)
        else:
            return Response({'error': 'data invalid'}, 403)
    
