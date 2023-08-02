from django.contrib import admin

from .models import Employee, EmployeeAttendance
# Register your models here.
import csv

from django.http import HttpResponse
import datetime

class EmployeeAttendanceAdmin(admin.ModelAdmin):
    list_display = ['emp_id','login_datetime','logout_datetime']
    list_filter = ['emp_id__name',]
    actions = ['export_as_csv',]
    model = EmployeeAttendance

    # class Meta:

    @admin.action(description="Generate Report")
    def export_as_csv(self, request, queryset):
        # Define the CSV file name


        excluded_fields = ['id','created_at','modified_at']

        current_date = datetime.datetime.now()
        current_month = current_date.month
        current_year = current_date.year

        employee_id = queryset.first().emp_id

        attendance_records = EmployeeAttendance.objects.filter(
            emp_id=employee_id,
            login_datetime__month = current_month,
            login_datetime__year = current_year 
        )

        filename = f"{employee_id.name}-attendance-report-{str(datetime.date.today())}.csv"
        # Set the response content type
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Create the CSV writer
        writer = csv.writer(response)

        # Write the header row
        writer.writerow([field.name for field in queryset.model._meta.fields if field.name not in excluded_fields])

        # Write the data rows
        for obj in attendance_records:
            writer.writerow([getattr(obj, field.name) for field in queryset.model._meta.fields if field.name not in excluded_fields])

        return response

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','dob','role','wish_birthday']
    fields = ['name','email','dob','role']

admin.site.register(Employee,EmployeeAdmin)    
admin.site.register(EmployeeAttendance,EmployeeAttendanceAdmin)
