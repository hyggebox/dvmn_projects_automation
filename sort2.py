import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dvmn_projects_automation.settings")

import django
django.setup()

from dpa_app.models import TimeSlot, PM, Group, Student

from pprint import pprint

# Сейчас не используется
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


def get_pms_time_slots():
    '''Returns a tuple of available time_slots with PMs from DB'''
    pms = PM.objects.all()
    available_time_slots = []
    for pm in pms:
        time_slots = pm.time_slots.all()
        for slot in time_slots:
            available_time_slots.append((slot.id, pm.name))
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


def load_students_secondary_slots(student_id):
    '''Returns a list of student's possible time slots'''
    student = Student.objects.get(id=student_id)
    ok_slots = student.ok_time_slots.all()
    ok_slots_ids = [slot.id for slot in ok_slots]
    return ok_slots_ids


def print_groups(groups, temp_ids):
    print("groups", groups)
    for slot_temp_id, student_ids in groups.items():
        slot_id, pm_name = temp_ids[slot_temp_id]
        slot = TimeSlot.objects.get(id=slot_id)
        print(slot.timeslot, pm_name)
        for student_id in student_ids:
            student = Student.objects.get(id=student_id)
            print(f'{student.f_name} {student.l_name} -- ({student.level})')
        print('')


def sort_students_for_groups(groups, temporary_ids_for_slots, students):

    for temp_id, (slot_id, pm_name) in temporary_ids_for_slots.items():
        students_in_group = []
        for student_id, student_answer in students.items():

            student = Student.objects.get(id=student_id)
            students_level = student.level

            for chosen_slot in student_answer:

                if chosen_slot == slot_id \
                    and len(students_in_group) == 0:
                        students_in_group.append(student_id)
                        first_student_id_in_group = student_id

                elif chosen_slot == slot_id \
                    and len(students_in_group) < 3 \
                    and first_grupped_student_lvl == students_level:
                        students_in_group.append(student_id)
                        first_student_id_in_group = groups[last_id][0]

                groups.update({temp_id: students_in_group})
                last_id = temp_id

            first_grupped_student_lvl = Student.objects.get(
                id=first_student_id_in_group
                ).level

        for student_id in students_in_group:
            del students[student_id]

        sorted_groups = groups
    return sorted_groups, temporary_ids_for_slots, students


if __name__ == '__main__':
    available_time_slots = get_pms_time_slots()
    print(available_time_slots) # list of tuples (time_slot_id, PM)

    temporary_ids_for_slots = {}
    for num, slot in enumerate(available_time_slots):
        temporary_ids_for_slots[num] = slot
    print(temporary_ids_for_slots)

    students = load_student_slots()
    groups = {}
    sorted_groups, temporary_ids_for_slots, not_included_students = \
        sort_students_for_groups(groups, temporary_ids_for_slots, students)

    print("Группы:")
    # pprint(groups) # keys are temporary slot ids from temporary_ids_for_slots
    print_groups(sorted_groups, temporary_ids_for_slots)
    print('')

    print("Студенты не вошедшие в группы: (id студента: [id слотов])")
    pprint(not_included_students)
    print('')
