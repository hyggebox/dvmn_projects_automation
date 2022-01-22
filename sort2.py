from pprint import pprint

slot1 = "18:00-18:30"
slot2 = "18:30-19:00"
slot3 = "19:00-19:30"
slot4 = "19:30-20:00"
slot5 = "20:00-20:30"
slot6 = "20:30-21:00"


slots = {
    slot1: [],
    slot2: [],
    slot3: [],
    slot4: [],
    slot5: [],
    slot6: [],
}

students = {
    'Student1': [slot3, slot4, slot6],
    'Student2': [slot3, slot4, slot6],
    'Student3': [slot5, slot4],
    'Student4': [slot2],
    'Student5': [slot1, slot4, slot5, slot6],
    'Student6': [slot3, slot4, slot6],
    'Student7': [slot4, slot6],
    'Student8': [slot3],
    'Student9': [slot1, slot2, slot3, slot4, slot5, slot6],
    'Student10': [slot1, slot2, slot3, slot4, slot5, slot6],
    'Student11': [slot2],
    'Student12': [slot2, slot3],
    'Student13': [slot5],
    'Student14': [slot5, slot6],
    'Student15': [slot1, slot2, slot3, slot4, slot5, slot6],
    'Student16': [slot1, slot4, slot6],
    'Student17': [slot2, slot4, slot6],
    'Student18': [slot5],
    'Student19': [slot3],
    'Student20': [slot2, slot4, slot6],
    'Student21': [slot2, slot4, slot6],
       }


groups = {}
pprint(slots)

for slot in slots:
    print(slot)
    students_in_group = []
    for student, student_answer in students.items():

        for choiced_slot in student_answer:

            if choiced_slot == slot and len(students_in_group) < 3:
                students_in_group.append(student)

            groups.update({slot: students_in_group})

    for student in students_in_group:
        del students[student]

print("Группы:")
pprint(groups)
print('')

print("Студенты не вошедшие в группы:")
pprint(students)
print('')
