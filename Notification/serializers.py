from rest_framework import serializers
from rest_framework.response import Response
from User.models import User
from django.shortcuts import get_object_or_404
from Notification.models import XYZ
from User.models import User


class testone(serializers.ModelSerializer):
    
    class Meta:
        model = XYZ
        fields = ['message_sender', 'message_head', 'message_body', 'message_file', 'message_creation_time']


class SendAddressBook(serializers.ModelSerializer):
    message_receivers = serializers.CharField(max_length=255)
    class Meta:
        model = XYZ
        fields = ['id', 'message_head', 'message_body', 'message_file', 'message_receivers']
        read_only_fields = ['id']

    def save(self, sender, **kwargs):
        new_message = XYZ(
            message_head = self.validated_data['message_head'],
            message_body = self.validated_data['message_body'],
            message_file = self.validated_data['message_file'],
        )
        new_message.set_author(sender)
        new_message.save()
        message_receivers = self.validated_data['message_receivers'].split(' ')
        for i in message_receivers:
            sp_user = get_object_or_404(User, username=i)
            new_message.message_receivers.add(sp_user)
            new_message.save()
        return new_message