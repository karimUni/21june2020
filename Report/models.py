from django.db import models
from User.models import Student, Teacher, HeadMaster, Subject


class ReportStudent(models.Model):
    # not completed yet
    report_id = models.IntegerField()
    report_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    report_creator = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    report_creation_time = models.DateTimeField(auto_now_add=True)
    report_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def set_author(self, report_creator):
        self.report_creator = report_creator

    def set_reciver(self, report_student):
        self.report_student = report_student

    def set_subject(self, report_subject):
        self.report_subject = report_subject

class ReportStudentHeadMaster(models.Model):
    report_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    report_creator = models.ForeignKey(HeadMaster, on_delete=models.CASCADE)
    report_creation_time = models.DateTimeField(auto_now_add=True)


class ReportTeacher(models.Model):
    report_head = models.CharField(max_length=150)
    report_body = models.CharField(max_length=500)
    report_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    report_creator = models.ForeignKey(HeadMaster, on_delete=models.CASCADE)
    report_creation_time = models.DateTimeField(auto_now_add=True)
