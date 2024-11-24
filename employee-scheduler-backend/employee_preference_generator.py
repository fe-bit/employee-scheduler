import random
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class PreferenceType(Enum):
    PREFERRED = "preferred"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    

@dataclass
class Preference:
    employee_id: int
    date_start: datetime
    date_end: datetime
    preference: PreferenceType



def generate_employee_preferences(num_employees, date_start:datetime, date_end:datetime) -> list[Preference]:
    """
    Generate a month of employee shift data with varied preferences
    
    Args:
    - num_employees (int): Number of employees
    - month (int): Month to generate shifts for
    - year (int): Year to generate shifts for
    
    Returns:
    - List of shift dictionaries
    """
    shifts = []
    shift_types = [
        {"start": 6, "end": 14},
        {"start": 14, "end": 22},
        {"start": 22, "end": 6}
    ]
    
    # Create a list of days in the month
    days = [date_start + timedelta(n) for n in range(1, int((date_end - date_start).days) + 2)]

    for employee_id in range(1, num_employees + 1):
        for day in random.sample(days, int(len(days)/2)):
            shift_type = random.choice(shift_types)
            preference = random.choices(
                [PreferenceType.PREFERRED, PreferenceType.UNAVAILABLE], 
                weights=[0.5, 0.5]  # More weight to preferred/available
            )[0]
            
            shift = Preference(
                employee_id=employee_id, 
                date_start=datetime(day.year, day.month, day.day, shift_type["start"]),
                date_end=datetime(day.year, day.month, day.day, shift_type["end"]),
                preference=preference
            )
            shifts.append(shift)
    
    return shifts
