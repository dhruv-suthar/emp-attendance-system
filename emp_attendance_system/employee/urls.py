from django.urls import path

from .views import upcoming_emps_birthday, emp_login, emp_login_successfully


urlpatterns = [
    path('upcoming_emps_birthday/', upcoming_emps_birthday, name='upcoming_emps_birthday'),
    path('emp_login/', emp_login, name='emp_login'),
    path('emp_detail/', emp_login_successfully, name='emp_detail'),
]