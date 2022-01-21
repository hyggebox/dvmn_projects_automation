"""
Import json data from JSON file to Datababse
"""
import os
import json
from dpa_app.models import TimeSlot, PM, Group, Student
from django.core.management.base import BaseCommand
from datetime import datetime
from dvmn_projects_automation.settings import BASE_DIR

import pprint


class Command(BaseCommand):
    def import_data_from_file(self):
        data_folder = os.path.join(BASE_DIR, 'dpa_app', 'media')
        print(os.path.join(BASE_DIR, 'dpa_app', 'media'))
        for data_file in os.listdir(data_folder):
            with open(os.path.join(data_folder, data_file), encoding='utf-8') as data_file:
                data = json.loads(data_file.read())
                for data_object in data:
                    if data_object == 'PM':
                        pms_data = data[data_object]
                        for pm_data in pms_data:
                            print('=' * 80)
                            print(pm_data, type(pm_data))
                            name_pm = pm_data.get('Name', None)
                            telegram_id_pm = pm_data.get('TelegramID', None)
                            time_slots_pm = pm_data.get('TimeSlots', None)
                            try:
                                pm, created = PM.objects.get_or_create(
                                    tg_id = telegram_id_pm,
                                    name = name_pm
                                )
                                if created:
                                    pm.save()
                                    display_format = "\nPM, {}, has been saved."
                                    print(display_format.format(pm))
                            except Exception as ex:
                                print(str(ex))
                                msg = "\n\nSomething went wrong saving this PM: {}\n{}".format(name_pm, str(ex))
                                print(msg)
                            print('=' * 80)
                    if data_object == 'Students':
                        students_data = data[data_object]
                        for student_data in students_data:
                            print('=' * 80)
                            print(student_data, type(student_data))
                            first_name_student = student_data.get('FirstName', None)
                            last_name_student = student_data.get('LastName', None)
                            level_student = student_data.get('Level', None)
                            telegram_id_student = student_data.get('TelegramID', None)
                            #time_slots_student = student_data.get('TimeSlots', None)
                            try:
                                student, created = Student.objects.get_or_create(
                                    tg_id = telegram_id_student,
                                    f_name =first_name_student,
                                    l_name = last_name_student
                                )
                                student.level = level_student
                                if created:
                                    student.save()
                                    display_format = "\nStudent, {}, has been saved."
                                    print(display_format.format(student))
                            except Exception as ex:
                                print(str(ex))
                                msg = "\n\nSomething went wrong saving this Student: {}\n{}".format(last_name_student, str(ex))
                                print(msg)
                            print('=' * 80)

                print('='*80)

    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.import_data_from_file()
