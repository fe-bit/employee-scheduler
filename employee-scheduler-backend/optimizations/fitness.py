# Evaluate: enough breaks between shifts (min 10h)
            # Group by Employee: Check shifts timedelta (sorted entries, Beware of keeping the shift idx)
        # Evaluate: enough hours for each employee: 
            # 

import pandas as pd
from datetime import datetime, date, timedelta, time
import calendar
import enum
import random
from shifts import create_shifts_for_dates, get_shifts_per_employee, CarType, get_total_work_hours_per_employee
from employee_preference_generator import Preference, PreferenceType
import numpy as np


BREAK_PENALTY = 40


def calculate_fitness(genes, shifts, preferences:np.array, work_hours_per_employee:int):
    fitness = 0
    shifts_per_employee = get_shifts_per_employee(shifts, genes)
    correct, faults, fault_count = fitness_break_between_shifts(shifts_per_employee)
    fitness -= faults

    correct, faults, count_hours = fitness_total_hours_per_employee(shifts_per_employee, work_hours_per_employee)
    fitness -= faults

    f, count_disregarded, count_accounted = fitness_preference(genes, preferences)
    fitness += f
    fitness_history = {
        "Fitness": fitness,
        "Break Violations": fault_count,
        "Hours Violations": count_hours,
        "Preferred Shifts Accounted": count_accounted,
        "Unavailable Shifts Disregarded": count_disregarded,
    }
    return int(fitness), fitness_history
    
def fitness_break_between_shifts(shifts_per_employee):
    faults = 0
    correct = 0
    count = 0
    for employee, schedule in shifts_per_employee.items():
        for i in range(len(schedule)-1):
            left_job = schedule[i][1]
            right_job = schedule[i+1][0]
            time_diff = abs(right_job - left_job)
            hours_diff = time_diff.total_seconds() / 3600
            if hours_diff < 10:
                faults += BREAK_PENALTY
                count += 1
            else:
                correct += BREAK_PENALTY
    return correct, faults, count

def fitness_qualification(shifts_per_employee, qualifications):
    # TODO
    pass

def fitness_total_hours_per_employee(shifts_per_employee, work_hours_per_employee):
    faults = 0
    count = 0
    correct = 0

    for employee, total_work_hours in get_total_work_hours_per_employee(shifts_per_employee).items():
        if total_work_hours < work_hours_per_employee*0.8 or total_work_hours > work_hours_per_employee*1.2:
            ff = abs(40-total_work_hours) * 0.5
            faults += ff
            count += 1
        else:
            correct += 1
    return correct, faults, count

def fitness_preference(genes, preferences:np.array):
    fitness = 0
    count_accounted = 0
    count_disregarded = 0
    for shift_id, g in enumerate(genes):
        p = preferences[g-1][shift_id]
        if p > 0:
            count_accounted += 1
        elif p < 0:
            count_disregarded += 1
        fitness += p
    return fitness, count_disregarded, count_accounted
