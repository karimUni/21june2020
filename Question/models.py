from django.db import models
from User.models import User, Teacher ,Subject , ClassRoom
from PIL import Image


TYPE = (
    ('MCQ' , 'MCQ'),
    ('TR', 'TR'),
)

class Question(models.Model):
    question_id = models.IntegerField()
    question_type = models.CharField(max_length=50)
    question_author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    question_creation_time = models.DateTimeField(auto_now_add=True)
    question_real_time = models.IntegerField(default=10)
    question_customization_time = models.IntegerField()
    question_points = models.IntegerField(default=1)
    question_grade = models.CharField(max_length=50)
    question_level = models.CharField(max_length=50)
    question_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question_topic = models.CharField(max_length=150)

    def set_question_id(self, question_id):
        self.question_id = question_id

    def set_question_author(self, question_author):
        self.question_author = question_author

    def set_question_subject(self, question_subject):
        self.question_subject = question_subject

    def set_level(self, question_level):
        self.question_level = question_level

    def set_time(self, question_real_time):
        self.question_real_time = question_real_time

    #save custom_time now with real time untile the system is calculate the time auomatically
    def save(self , *args , **kwargs):
        self.question_customization_time = self.question_real_time
        super(Question,self).save(*args,**kwargs)


class MCQ(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    question_head = models.CharField(max_length=255, blank=True, null=True)
    question_head_avatar = models.ImageField(upload_to='questions', default='questions/add-image.png')
    question_body = models.CharField(max_length=250, null=False, blank=False)
    choice_A = models.CharField(max_length=100, blank=False, null=False)
    choice_B = models.CharField(max_length=100, blank=False, null=False)
    choice_C = models.CharField(max_length=100, blank=False, null=False)
    choice_D = models.CharField(max_length=100, blank=False, null=False)
    question_answer = models.CharField(max_length=100, blank=False, null=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.question_head_avatar:
            img = Image.open(self.question_head_avatar.path)

            if img.width > 600 or img.height > 600:
                output_size = (600, 600)
                img.thumbnail(output_size)
                img.save(self.question_head_avatar.path)
        pass

    def set_question(self, question):
        self.question = question


class TR(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    question_body = models.CharField(max_length=250, null=False, blank=False)
    question_answer = models.CharField(max_length=100, null=False, blank=False)

    def set_question(self, question):
        self.question = question

class Rate(models.Model):
    stars =  models.CharField(max_length=10 , null=False , blank=False )
    comment = models.CharField(max_length=250 , null=True , blank= True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='reviews')
    author = models.ForeignKey(Teacher ,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    creation_time = models.DateTimeField(auto_now_add=True)

    def set_question(self, question):
        self.question = question

    def set_author(self, author):
        self.author = author

    def set_subject(self, subject):
        self.subject = subject

    

