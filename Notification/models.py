from django.db import models
from User.models import User


# Create your models here.
class XYZ(models.Model):
    
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    message_head = models.CharField(max_length=255, null=True, blank=True)
    message_body = models.TextField()
    message_file = models.FileField(upload_to='documents', null=True, blank=True)
    message_receivers = models.ManyToManyField(User)
    message_creation_time = models.DateTimeField(auto_now_add=True)

    def set_author(self, message_sender):
        self.message_sender = message_sender