from django.db import models
from django.contrib.auth.models import AbstractUser
import os
from django.urls import reverse
from django.utils.html import format_html
from datetime import date

# Create your models here.


class TimeStampModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


USER_ROLES = [
    ('employee', 'employee'),
    ('admin', 'admin')
]

class Employee(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name''dob','role']


    class Meta:

        verbose_name = "Employee"
        verbose_name = "Employees"


    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100) 
    role = models.CharField(max_length=10, default ='employee',choices = USER_ROLES)
    dob = models.DateField()
    username = models.CharField(max_length=10,default="",null=True,blank=True)   
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.name} | {self.email} | {self.dob}"

    def wish_birthday(self):
        if self.dob == date.today():
            # url = reverse('admin:wish_birthday', args=[self.id])
            button_html = f'<a href="/admin/wish_birthday/{self.id}" class="button">Wish Birthday</a>'
            return format_html(button_html)
        else:
            return "-"
                        
class EmployeeAttendance(TimeStampModel):
    class Meta:
        verbose_name = "Employee Attendance"
       
    id = models.AutoField(primary_key=True)
    emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    login_datetime = models.DateTimeField()
    logout_datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.emp_id.name} | {self.login_datetime} | {self.logout_datetime}"






  