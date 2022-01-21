import os
import json
import networkx as nx

from dpa_app.models import TimeSlot, PM, Group, Student
from django.core.management.base import BaseCommand
from datetime import datetime
from dvmn_projects_automation.settings import BASE_DIR


def get_capacities():
    time_slots = TimeSlot.objects.all()
    capacities = {slot.id: (slot.pms.all().count() * 3) for slot in time_slots}
    return capacities


def load_student_slots():
    prefs = {}
    students = Student.objects.all()

    for student in students:
        best_slots = student.best_time_slots.all()
        ok_slots = student.ok_time_slots.all()
        list_slots = [slot.id for slot in best_slots]
        for slot in ok_slots:
            list_slots.append(slot.id)

        prefs[student.id] = list_slots
    return prefs


def print_groups(groups_dict):
    for slot_id, students_ids in groups_dict.items():
        try:
            print(f'\nВремя {TimeSlot.objects.get(id=slot_id)}:')
        except ValueError:
            pass
        else:
            for num, student_id in enumerate(students_ids):
                student = Student.objects.get(id=student_id)
                print(num+1, student.f_name, student.l_name)


def main() -> None:
    graph = nx.DiGraph()
    prefs = load_student_slots()

    persons_num = len(prefs)
    graph.add_node('dest', demand=persons_num)

    for person, time_slots in prefs.items():
        graph.add_node(person, demand=-1)
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
            graph.add_edge(person, time_slot, capacity=1, weight=points)

    for time_slot, capacity in get_capacities().items():
            graph.add_edge(time_slot, 'dest', capacity=capacity, weight=0)

    flowdict = nx.min_cost_flow(graph)
    groups = {}
    for person in prefs:
        for time_slot, flow in flowdict[person].items():
            if flow:
                groups[time_slot] = groups.get(time_slot, []) + [person]

    print_groups(groups)


class Command(BaseCommand):

    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        main()