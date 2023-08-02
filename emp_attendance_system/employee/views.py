from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from .models import Employee
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

# Create your views here.

def upcoming_emps_birthday(request):
    today = date.today()
    upcoming_employees = Employee.objects.filter(dob__gte=today).order_by('dob')
    context = {'upcoming_emps_bd': upcoming_employees}
    return render(request, 'emp_birthday_lists.html', context)

def emp_login(request):
   #store login time if not logged in 
   # if user already logged
   context = {}
   return render(request, 'emp_login.html', context)

def emp_login_successfully(request):
	employee = request.user 
	if employee:
		print(employee,"employee")
		context = {'employee':employee}
		return render(request, 'emp_login_success.html', context)
	return redirect('emp_login')	

def wish_birthday(request, pk):
  employee = get_object_or_404(Employee, pk=pk)
  employee_email = str(employee.email)
  employee_name = str(employee.name)
  subject = f"🎉 Happy Birthday, {employee_name}! 🎂 Let's Celebrate!"
  message = f"""
  Dear {employee_name},

  Wishing you a day filled with joy, laughter, and wonderful memories. 
  Happy Birthday, {employee_name}!

  Thanks."""
  from_email = settings.EMAIL_HOST_USER
  recipient_list = [employee_email]

  send_mail(subject, message, from_email, recipient_list)
  messages.success(request, f"Birthday wish sent to {employee.name}!")
  return redirect('admin:employee_employee_changelist')