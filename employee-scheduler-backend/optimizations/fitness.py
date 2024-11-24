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

BREAK_PENALTY = 40


def calculate_fitness(employee_preferences, genes, shifts):
    fitness = 0
    shifts_per_employee = get_shifts_per_employee(shifts, genes)
    correct, faults = fitness_break_between_shifts(shifts_per_employee)
    fitness -= faults

    correct, faults = fitness_total_hours_per_employee(shifts_per_employee)
    fitness -= faults
    return fitness
    
def fitness_break_between_shifts(shifts_per_employee):
    faults = 0
    correct = 0
    for employee, schedule in shifts_per_employee.items():
        for i in range(len(schedule)-1):
            left_job = schedule[i][1]
            right_job = schedule[i+1][0]
            time_diff = abs(right_job - left_job)
            hours_diff = time_diff.total_seconds() / 3600
            if hours_diff < 10:
                faults += BREAK_PENALTY
            else:
                correct += BREAK_PENALTY
    return correct, faults

def fitness_qualification(shifts_per_employee, qualifications):
    # TODO
    pass

def fitness_total_hours_per_employee(shifts_per_employee):
    faults = 0
    correct = 0

    for employee, total_work_hours in get_total_work_hours_per_employee(shifts_per_employee).items():
        if total_work_hours < 32 or total_work_hours > 45:
            ff = abs(40-total_work_hours) * 0.5
            faults += ff
        else:
            correct += 1
    return correct, faults

