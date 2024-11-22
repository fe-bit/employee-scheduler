import pandas as pd
from datetime import datetime, date, timedelta, time
import calendar
import enum
import random

class CarType(enum.Enum):
    KTW_D = 1
    KTW_SW = 2
    RTW_D = 3
    RTW_SW = 4
    NEF_D = 5


def get_days_in_a_month(month, year):
    num_days = calendar.monthrange(year, month)[1]
    first_day = date(year, month, 1)
    days_in_month = [first_day + timedelta(days=i) for i in range(num_days)]
    return days_in_month

def get_dates_for(day:date, start_time:time, hours:time):
    start_date = datetime(day.year, day.month, day.day, start_time.hour, start_time.minute, start_time.second)
    end_date = start_date + timedelta(hours=hours.hour, minutes=hours.minute)
    return start_date, end_date


def create_shifts_of_month(date_start, date_end):
    shifts = []
    
    for n in range(int((date_end - date_start).days) + 1):
        day = date_start + timedelta(n)
        # KTW
        shifts.append((*get_dates_for(day, time(6), hours=time(8)), CarType.KTW_D))
        shifts.append((*get_dates_for(day, time(6), hours=time(8)), CarType.KTW_SW))
        shifts.append((*get_dates_for(day, time(14), hours=time(8)), CarType.KTW_D))
        shifts.append((*get_dates_for(day, time(14), hours=time(8)), CarType.KTW_SW))
        shifts.append((*get_dates_for(day, time(22), hours=time(8)), CarType.KTW_D))
        shifts.append((*get_dates_for(day, time(22), hours=time(8)), CarType.KTW_SW))
        # RTW
        shifts.append((*get_dates_for(day, time(6), hours=time(8)), CarType.RTW_D))
        shifts.append((*get_dates_for(day, time(6), hours=time(8)), CarType.RTW_SW))
        shifts.append((*get_dates_for(day, time(14), hours=time(8)), CarType.RTW_D))
        shifts.append((*get_dates_for(day, time(14), hours=time(8)), CarType.RTW_SW))
        shifts.append((*get_dates_for(day, time(22), hours=time(8)), CarType.RTW_D))
        shifts.append((*get_dates_for(day, time(22), hours=time(8)), CarType.RTW_SW))
        # NEF
        shifts.append((*get_dates_for(day, time(6), hours=time(8)), CarType.NEF_D))
        shifts.append((*get_dates_for(day, time(14), hours=time(8)), CarType.NEF_D))
        shifts.append((*get_dates_for(day, time(22), hours=time(8)), CarType.NEF_D))
    return shifts


def get_shifts_per_employee(shifts, genes):
    result = {}
    for shift, gene in zip(shifts, genes):
        if gene in result:
            result[gene].append(shift)
        else:
            result[gene] = [shift]
    for gene in result:
        result[gene] = sorted(result[gene], key=lambda x: x[0], reverse=False)

    return result


def get_total_work_hours_per_employee(shifts_per_employee):
    result = {}
    for employee, schedule in shifts_per_employee.items():
        work_hours = [abs(s[0] - s[1]).total_seconds() / 3600 for s in schedule]
        avg_work_hours = sum(work_hours)
        result[employee] = avg_work_hours
    return result