# Generated by Django 4.1.3 on 2023-06-28 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0004_alter_employee_firebase_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='firebase_id',
        ),
        migrations.RemoveField(
            model_name='employeeattendance',
            name='status',
        ),
    ]