from django.core.management.base import BaseCommand

from dpa_app.models import TimeSlot, PM, Group, Student


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
    for slot_temp_id, student_ids in groups.items():
        slot_id, pm_name = temp_ids[slot_temp_id]
        slot = TimeSlot.objects.get(id=slot_id)
        print(slot.timeslot, pm_name)
        for student_id in student_ids:
            student = Student.objects.get(id=student_id)
            print(f'{student.f_name} {student.l_name} -- ({student.level})')
        print('')


def create_groups(groups, temp_ids):
    for slot_temp_id, student_ids in groups.items():
        if student_ids:
            slot_id, pm_name = temp_ids[slot_temp_id]
            slot = TimeSlot.objects.get(id=slot_id)
            groups_pm = PM.objects.get(name=pm_name)
            group, created = Group.objects.get_or_create(
                pm=groups_pm,
                time_slot=slot
            )
            for student_id in student_ids:
                student = Student.objects.get(id=student_id)
                student.group = group
                student.save()


def sort_students_for_groups(groups, temporary_ids_for_slots, students):

    for temp_id, (slot_id, pm_name) in temporary_ids_for_slots.items():
        students_in_group = []
        first_student_id_in_group = 0
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
            if first_student_id_in_group != 0:
                first_grupped_student_lvl = Student.objects.get(
                    id=first_student_id_in_group
                    ).level

        for student_id in students_in_group:
            del students[student_id]

        sorted_groups = groups
    return sorted_groups, temporary_ids_for_slots, students


def sort_students_by_secondary_slots(groups, temporary_ids_for_slots, student_id, pref_slots_ids):
    for temp_id, (slot_id, pm_name) in temporary_ids_for_slots.items():
        pass

    for group_temp_slot_id, student_ids in groups.items():
        if student_ids:
            first_groupped_student_lvl = Student.objects.get(id=student_ids[0]).level
            current_student_lvl = Student.objects.get(id=student_id).level
            if len(student_ids) < 3 and first_groupped_student_lvl == current_student_lvl:
                slot_id, groups_pm = temporary_ids_for_slots[group_temp_slot_id]
                if slot_id in pref_slots_ids:
                    groups[group_temp_slot_id].append(student_id)
                    return True
    return False


def main():
    available_time_slots = get_pms_time_slots()

    temporary_ids_for_slots = {}
    for num, slot in enumerate(available_time_slots):
        temporary_ids_for_slots[num] = slot

    students = load_student_slots()
    groups = {}
    sorted_groups, _, not_included_students = \
        sort_students_for_groups(groups, temporary_ids_for_slots, students)

    secondary_not_included_students = []
    for student_id, _ in not_included_students.items():
        students_secondary_slots = load_students_secondary_slots(student_id)
        if not sort_students_by_secondary_slots(groups,
                                         temporary_ids_for_slots,
                                         student_id,
                                         students_secondary_slots):
            secondary_not_included_students.append(student_id)

    for group_temp_slot_id, student_ids in groups.items():
        if len(student_ids) < 2:
            groups[group_temp_slot_id] = []
            secondary_not_included_students += student_ids

    create_groups(groups, temporary_ids_for_slots)
    print('Id студентов, не вошедших в группы:')
    print(secondary_not_included_students)



class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        main()