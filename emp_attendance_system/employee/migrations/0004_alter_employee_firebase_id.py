# Generated by Django 4.1.3 on 2023-06-27 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_alter_employee_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='firebase_id',
            field=models.CharField(default='', editable=False, max_length=128),
        ),
    ]