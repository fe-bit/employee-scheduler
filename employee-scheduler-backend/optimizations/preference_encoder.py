from employee_preference_generator import Preference, PreferenceType
from shifts import Shift
import numpy as np

def encode_preferences(preferences: list[Preference], employee_count:int, shifts:list[Shift]):
    encoded_prefs = np.zeros((employee_count, len(shifts)), dtype=int)
    for pref in preferences:

        match pref.preference:
            case PreferenceType.PREFERRED: pref_value = 4
            case PreferenceType.AVAILABLE: pref_value = 0
            case PreferenceType.UNAVAILABLE: pref_value = -4
        
        shifts_affected_idx = [
            i for i, shift in enumerate(shifts) 
            if shift.date_start == pref.date_start and shift.date_end == pref.date_end
        ]
        for affected_shift_idx in shifts_affected_idx:
            encoded_prefs[pref.employee_id-1][affected_shift_idx] = pref_value

    return encoded_prefs
