import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dvmn_projects_automation.settings")

import django
django.setup()

from dpa_app.models import TimeSlot, PM, Group, Student

from pprint import pprint

def get_time_slots():
    '''Returns a list of available time_slots from DB'''
    pms = PM.objects.all()
    available_time_slots = []
    for pm in pms:
        time_slots = pm.time_slots.all()
        for slot in time_slots:
            available_time_slots.append(slot.id) # returns ids of slots
            # available_time_slots.append(slot.timeslot) # returns slots
    return available_time_slots


def load_student_slots():
    '''Returns a dict of student ids with preferred time slots'''
    prefs = {}
    students = Student.objects.all()
    for student in students:
        best_slots = student.best_time_slots.all()
        list_slots = [slot.id for slot in best_slots]
        prefs[student.id] = list_slots
    return prefs

# slot1 = "18:00-18:30"
# slot2 = "18:30-19:00"
# slot3 = "19:00-19:30"
# slot4 = "19:30-20:00"
# slot5 = "20:00-20:30"
# slot6 = "20:30-21:00"
#
#
# slots = {
#     slot1: [],
#     slot2: [],
#     slot3: [],
#     slot4: [],
#     slot5: [],
#     slot6: [],
# }

# students = {
#     'Student1': [slot3, slot4, slot6],
#     'Student2': [slot3, slot4, slot6],
#     'Student3': [slot5, slot4],
#     'Student4': [slot2],
#     'Student5': [slot1, slot4, slot5, slot6],
#     'Student6': [slot3, slot4, slot6],
#     'Student7': [slot4, slot6],
#     'Student8': [slot3],
#     'Student9': [slot1, slot2, slot3, slot4, slot5, slot6],
#     'Student10': [slot1, slot2, slot3, slot4, slot5, slot6],
#     'Student11': [slot2],
#     'Student12': [slot2, slot3],
#     'Student13': [slot5],
#     'Student14': [slot5, slot6],
#     'Student15': [slot1, slot2, slot3, slot4, slot5, slot6],
#     'Student16': [slot1, slot4, slot6],
#     'Student17': [slot2, slot4, slot6],
#     'Student18': [slot5],
#     'Student19': [slot3],
#     'Student20': [slot2, slot4, slot6],
#     'Student21': [slot2, slot4, slot6],
#        }




if __name__ == '__main__':
    available_time_slots = get_time_slots()
    print(available_time_slots)

    temporary_ids_for_slots = {}
    for num, slot in enumerate(available_time_slots):
        temporary_ids_for_slots[num] = slot
    print(temporary_ids_for_slots)

    students = load_student_slots()
    groups = {}

    for temp_id, slot_id in temporary_ids_for_slots.items():
        print(temp_id, slot_id)
        students_in_group = []
        for student, student_answer in students.items():

            for choiced_slot in student_answer:

                if choiced_slot == slot_id and len(students_in_group) < 3:
                    students_in_group.append(student)

                groups.update({temp_id: students_in_group})

        for student in students_in_group:
            del students[student]


    print("Группы:")
    pprint(groups) # keys are temporary slot ids from temporary_ids_for_slots
    print('')

    print("Студенты не вошедшие в группы:")
    pprint(students)
    print('')

