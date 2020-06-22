# Notes this views.py only for registraion
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from Notification.serializers import testone, SendAddressBook
from .models import XYZ
from User.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from User.decorators import teacher_role, student_role



# @api_view(['GET', 'POST'])
# @csrf_exempt
# def send_message(request):
#     user = request.user
#     if request.method == 'GET':
#         data = XYZ.objects.filter(message_receivers=user)
#         serializer = testone(data, many=True)
#         return Response({'data': serializer.data}, 200)
#     elif request.method == 'POST':
#         message_sender = user
#         message_head = request.data.get('message_head')
#         message_body = request.data.get('message_body')
#         message_file = request.data.get('message_file')
#         message_receivers = request.data.get('message_receivers')
#         if (not message_head or not message_body or not message_receivers):
#             return Response({'error': 'invalid data'}, 403)
#         new_message = XYZ(message_sender=message_sender, message_head=message_head, message_body=message_body, message_file=message_file)
#         new_message.save()
#         for i in message_receivers:
#             sp_user = get_object_or_404(User, username=i)
#             new_message.message_receivers.add(sp_user)
#         return Response({'success': 'message sent successfully'}, 200)




@api_view(['GET', 'POST'])
@csrf_exempt
def send_message(request):
    user = request.user
    if request.method == 'GET':
        data = XYZ.objects.filter(message_receivers=user)
        serializer = testone(data, many=True)
        return Response({'data': serializer.data}, 200)
    elif request.method == 'POST':
        serializer = SendAddressBook(data=request.data)
        if serializer.is_valid():
            new_serializer = serializer.save(user)
            return Response({'success': 'message sent successfully'}, 200)
        return Response({'error': 'invalid data'}, 403)


@api_view(['POST'])
@csrf_exempt
def send_feedback(request):
    user = request.user
    feedback = request.data.get('feedback')
    comment = request.data.get('comment')
    send_mail('User FeedBack', 
    'User id {} with username {} : {} {}'.format(user.id, user.username, feedback, comment),
    settings.EMAIL_HOST_USER,
    ['feedback@unilearn.com.eg'],
    fail_silently=False)

    return HttpResponse('success')




@api_view(['GET'])
@csrf_exempt
@teacher_role
def list_students(request):
    # users = User.objects.filter(role='S')
    users = User.objects.all()
    usernames = []
    for i in users:
        usernames.append(i.username)
    return Response({'data': usernames}, 200)


@api_view(['GET'])
@csrf_exempt
# @student_role
def list_teachers(request):
    users = User.objects.filter(role='T')
    usernames = []
    for i in users:
        usernames.append(i.username)
    return Response({'data': usernames}, 200)