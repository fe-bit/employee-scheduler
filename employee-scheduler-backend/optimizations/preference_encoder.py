from employee_preference_generator import Preference, PreferenceType
from shifts import Shift
import numpy as np

def encode_preferences(preferences: list[Preference], employee_count:int, shifts:list[Shift]):
    encoded_prefs = np.zeros((employee_count, len(shifts)), dtype=int)
    # encoded_prefs = np.full((employee_count, len(shifts)), fill_value=-1, dtype=int)
    for pref in preferences:

        match pref.preference:
            case PreferenceType.PREFERRED: pref_value = 1
            case PreferenceType.AVAILABLE: pref_value = 0
            case PreferenceType.UNAVAILABLE: pref_value = -4
            # case _: pref_value = -1
        for shift_idx, shift in enumerate(shifts):
            if shift.date_start == pref.date_start:
                encoded_prefs[pref.employee_id-1][shift_idx] = pref_value

    return encoded_prefs
