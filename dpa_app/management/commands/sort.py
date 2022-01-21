
import os
import json
from dpa_app.models import TimeSlot, PM, Group, Student
from django.core.management.base import BaseCommand
from datetime import datetime
from dvmn_projects_automation.settings import BASE_DIR
import networkx as nx
# Сортировка

G = nx.DiGraph()

slot1 = "18:00-18:30"
slot2 = "18:30-19:00"
slot3 = "19:00-19:30"
slot4 = "19:30-20:00"
slot5 = "20:00-20:30"
slot6 = "20:30-21:00"

slot_nums = [slot1,slot2,slot3,slot4,slot5,slot6]

capacities = {
    slot1:3,
    slot2:3,
    slot3:6,
    slot4:6,
    slot5:3,
    slot6:3
}

prefers = {
    'Student1':[slot3, slot4, slot6],
    'Student2':[slot3, slot4, slot6],
    'Student3':[slot5, slot4],
    'Student4':[slot2],
    'Student5':[slot1, slot4, slot5, slot6],
    'Student6':[slot3, slot4, slot6],
    'Student7':[slot4, slot6],
    'Student8':[slot3],
    'Student9':[slot1, slot2, slot3, slot4, slot5, slot6],
    'Student10':[slot1, slot2, slot3, slot4, slot5, slot6],
    'Student11':[slot2],
    'Student12':[slot2, slot3],
    'Student13':[slot5],
    'Student14':[slot5, slot6],
    'Student15':[slot1, slot2, slot3, slot4, slot5, slot6],
    'Student16':[slot1, slot4, slot6],
    'Student17':[slot2, slot4, slot6],
    'Student18':[slot5],
    'Student19':[slot3],
    'Student20':[slot2, slot4, slot6],
    'Student21':[slot2, slot4, slot6],
       }

def load_student_slots():
    prefs = {}
    students = Student.objects.all()
    for student in students:
        slots = student.best_time_slots.all()
        list_slots = []
        for slot in slots:
            print(slot.timeslot)
            list_slots.append(slot.timeslot)
        print('='*80)
    return prefs

def main() -> None:
    prefs=load_student_slots()

    persons_num = len(prefs)
    G.add_node('dest', demand=persons_num)
    A = []

    for person, time_slots in prefs.items():
        G.add_node(person, demand=-1)
        for i, time_slot in enumerate(time_slots):
            if i == 0:
                points = -100  # лучшее время
            elif i == 1:
                points = -80
            elif i == 2:
                points = -60
            elif i == 3:
                points = -40
            elif i == 4:
                points = -20
            else:
                points = -1  # худшее время
            G.add_edge(person, time_slot, capacity=1, weight=points)

    for time_slot, capacity in capacities.items():
            G.add_edge(time_slot, 'dest', capacity=capacity, weight=0)

    flowdict = nx.min_cost_flow(G)
    groups = {}
    for person in prefs:
        for time_slot, flow in flowdict[person].items():
            if flow:
                groups[time_slot] = groups.get(time_slot, []) + [person]

    print(groups)


class Command(BaseCommand):


    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        main()