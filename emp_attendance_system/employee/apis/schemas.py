from ninja import Schema
from ..models import Employee, EmployeeAttendance
from datetime import date, datetime
from typing import List, Optional

class UserTokenSchema(Schema):
    email: str
    password: str
    

class UserSchema(Schema):
    id: Optional[int]
    name: str
    email: str
    password: str
    role: str = 'employee'
    dob: date 
    login_datetime: Optional[datetime] 
    logout_datetime: Optional[datetime] 
    # today_attendance_status: bool = False
    
    # def get_attendance_status(self,do_logout=False):
    #     emp_attendance_obj = EmployeeAttendance.objects.get_object_or_404(emp_id=self.id,login_datetime__date=date.today())
    #     if not emp_attendance_obj:
    #         emp_attendance_dict = {
    #             empid: self.id,
    #             login_datetime: datetime.now(),
    #             status: 'absent'
    #         }
    #         emp_attendance_obj = EmployeeAttendance.objects.create(**emp_attendance_dict)
    #     return emp_attendance_obj.login_datetime, emp_attendance_obj.logout_datetime, False if 'absent' == emp_attendance_obj.status else True

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     print("dsjfjdhfjdhjfhdjhfjhdj")
    #     # self.login_datetime, self.logout_datetime, self.today_attendance_status = self.get_login_time()

    class Config:
        model = Employee
        model_fields = "__all__"
        read_only_fields = ['id','email','password','role']
        orm_model = True    

class UserPasswordSchema(Schema):
    current_password: str
    new_password: str
  