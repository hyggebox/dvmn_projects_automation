from django.contrib import admin
from .models import TimeSlot, PM, Group, Student


class PMAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_time_slots')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'get_best_time_slots', 'get_ok_time_slots')


admin.site.register(PM, PMAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(TimeSlot)
admin.site.register(Group)
