from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.security import APIKeyHeader
from ninja.responses import Response
from rest_framework.authtoken.models import Token
from ..models import Employee, EmployeeAttendance
from .schemas import *
from typing import List
from datetime import date, datetime

User = get_user_model()
router = Router()



def get_or_set_attendance(emp,do_logout=False):
    try:
        emp_attendance_obj = EmployeeAttendance.objects.get(emp_id=emp,login_datetime__date=date.today())
        print(emp_attendance_obj)
        if emp_attendance_obj:
            if do_logout == True and not emp_attendance_obj.logout_datetime:
                emp_attendance_dict = {
                    'logout_datetime': datetime.now()
                }
                emp_attendance_obj.logout_datetime = datetime.now()
                emp_attendance_obj.save()
        return emp_attendance_obj.login_datetime, emp_attendance_obj.logout_datetime        
    except Exception as e:
        emp_attendance_dict = {
                'emp_id': emp,
                'login_datetime': datetime.now(),
        }
        emp_attendance_obj = EmployeeAttendance.objects.create(**emp_attendance_dict) 
        return emp_attendance_obj.login_datetime, emp_attendance_obj.logout_datetime      

class AuthToken(APIKeyHeader):
    param_name = "Authorization"
    def authenticate(self, request, token):
        try:
            if token:
                return User.objects.get(auth_token=token)
        except Employee.DoesNotExist:
            print("does not exist")


class isSuperUser(APIKeyHeader):
    param_name = "Authorization"
    def authenticate(self, request, token):
        try:
            if token:
                return User.objects.get(auth_token=token).role == "admin"
        except Employee.DoesNotExist:
           print("not superuser")
           

@router.post("/login", tags=["Authentication"])
def emp_login(request, body: UserTokenSchema):

    employee = authenticate(request, email=body.email, password=body.password)
    if employee:
        login(request, employee)
        employee = get_object_or_404(User, email=body.email)
        token, created = Token.objects.get_or_create(user=employee)
        emp_login_time, emp_logout_time =  get_or_set_attendance(employee)
        return Response({"token": token.key,"emp_login_time": emp_login_time},status=200)
    else:
        return Response({"message":"invalid credentails"},status=400)    
      

@router.get("/logout",auth=AuthToken())
def emp_logout(request):
    logout(request)
    employee = request.auth
    emp_login_time, emp_logout_time =  get_or_set_attendance(employee,do_logout=True)
    return Response({'login_datetime':emp_login_time,'logout_datetime':emp_logout_time},status=200)



@router.get("/user/profile",auth=AuthToken(), response=UserSchema)
def get_user_profiledt(request):
    user = request.auth 
    attendance_record = EmployeeAttendance.objects.filter(emp_id=user,login_datetime__date=date.today()).last()
    login_datetime = attendance_record.login_datetime if attendance_record else None
    logout_datetime = attendance_record.logout_datetime if attendance_record else None
    user.login_datetime = login_datetime
    user.logout_datetime = logout_datetime
    return user


@router.patch("/user/profile",auth=AuthToken(), response=UserSchema)
def update_user_profiledt(request, user:UserSchema):
    user_obj = request.auth 
    user_dict = user.dict()
    user_obj.dob = user_dict.get('dob')
    user_obj.name = user_dict.get('name')
    user_obj.save()
    attendance_record = EmployeeAttendance.objects.filter(emp_id=user_obj,login_datetime__date=date.today()).last()
    login_datetime = attendance_record.login_datetime if attendance_record else None
    logout_datetime = attendance_record.logout_datetime if attendance_record else None
    user_obj.login_datetime = login_datetime
    user_obj.logout_datetime = logout_datetime
    return user_obj


@router.patch("/user/change_pwd",auth=AuthToken())
def update_user_password(request,userPassword:UserPasswordSchema):
    user_dict = userPassword.dict()
    print(user_dict)
    user = request.auth
    if not check_password(user_dict.get('current_password'),user.password):
      return Response({"message": "Current password is incorrect"},status=401)
    else:
        new_password = make_password(user_dict.get('new_password'))
        user.password = new_password
        user.save()
        return Response({"message": "password has been changed"},status=200)
   

@router.post('/user',auth=isSuperUser(),response=UserSchema)
def create_user(request,user:UserSchema):
    user_dict = user.dict()
    user_dict.update({
            'password' : make_password(user_dict.get('password')),
            'username': user_dict.get('email').split('@')[0]
        })
    user_dict.pop('login_datetime')
    user_dict.pop('logout_datetime')
    user_obj = Employee.objects.create(**user_dict)
    return user_obj

@router.get('/user',auth=isSuperUser(),response=List[UserSchema])
def get_users(request):
    return Employee.objects.filter(role='employee')


@router.delete('/user/{user_id}',auth=isSuperUser())
def delete_user(request,user_id:int):
    user_del_obj = Employee.objects.get(id=user_id)
    user_del_obj.delete()
    return Response({"message":"user deleted."},status=200)
