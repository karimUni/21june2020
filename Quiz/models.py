from django.db import models
from Question.models import Question, MCQ, TR
from User.models import Teacher, ClassRoom, Student, Subject
from Report.models import ReportStudent, ReportStudentHeadMaster

class Quiz(models.Model):
    quiz_id = models.IntegerField()
    quiz_headline = models.CharField(max_length=100, null=True, blank=True)
    quiz_grade = models.CharField(max_length=50)
    quiz_questions = models.ManyToManyField(Question,related_name='quiz_questions')
    quiz_author = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    quiz_creation_time = models.DateTimeField(auto_now_add=True)
    quiz_launch_time = models.DateTimeField(null=True)
    quiz_real_time = models.IntegerField(null=True, blank=True)
    quiz_setion_time = models.IntegerField(null=True, blank=True)
    quiz_is_launched = models.BooleanField(default=False)
    quiz_class_room = models.ManyToManyField(ClassRoom , related_name='quiz_class')
    quiz_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def set_quiz_id(self, quiz_id):
        self.quiz_id = quiz_id

    def set_quiz_subject(self, quiz_subject):
        self.quiz_subject = quiz_subject

    def set_quiz_author(self, quiz_author):
        self.quiz_author = quiz_author

    def set_quiz_class_room(self, quiz_class_room):
        self.quiz_class_room = quiz_class_room

    # def get_quiz_id(self):
    #     return self.quiz_id

    def set_quiz_real_time(self, quiz_real_time):
        self.quiz_real_time = quiz_real_time

    def set_quiz_setion_time(self, quiz_setion_time):
        self.quiz_setion_time = quiz_setion_time

    def set_quiz_is_launched(self, quiz_is_launched):
        self.quiz_is_launched = quiz_is_launched

    def set_quiz_launch_time(self, quiz_launch_time):
        self.quiz_launch_time = quiz_launch_time



class Answers(models.Model):
    amswers_author = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_answers')
    answers_points = models.IntegerField()
    answer = models.CharField(max_length=100, blank=True, null=True)
    time_to_answer = models.IntegerField()
    answers_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE,related_name='quiz_answers')
    answers_questions = models.ManyToManyField(Question, related_name='question')
    answer_class_room = models.ManyToManyField(ClassRoom)
    answer_grade = models.CharField(max_length=10, null=True, blank=True)
    answer_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    answer_creation_time = models.DateTimeField(auto_now_add=True)
    
    def set_amswers_author(self, amswers_author):
        self.amswers_author = amswers_author

    def set_answers_questions(self, answers_questions):
        self.answers_questions = answers_questions

    def set_answers_quiz(self, answers_quiz):
        self.answers_quiz = answers_quiz

    def set_answer_class_room(self, answer_class_room):
        self.answer_class_room.add(answer_class_room)

    def set_answer_subject(self, answer_subject):
        self.answer_subject = answer_subject

    def set_answer_grade(self, answer_grade):
        self.answer_grade = answer_grade

    def set_answers_points(self, answers_points):
        self.answers_points = answers_points
