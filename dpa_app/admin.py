from django.contrib import admin
from .models import TimeSlot, PM, Group, Student

admin.site.register(PM)
admin.site.register(Student)
admin.site.register(TimeSlot)
admin.site.register(Group)

# Register your models here.
