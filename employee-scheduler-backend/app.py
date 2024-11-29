from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from optimizations.genetic_algorithm import GeneticAlgorithm
from optimizations.genetic_algorithm.genetic_algorithm_tabu import GeneticAlgorithmTabu
from shifts import get_shifts_per_employee, create_shifts_for_dates
from datetime import date
from dateutil.parser import parse
import random
from faker import Faker
import os
from employee_preference_generator import generate_employee_preferences, Preference, PreferenceType


if not os.path.exists("names.txt"):
    fake = Faker()
    with open("names.txt", "w", encoding="utf-8") as f:
        for n in range(100):
            f.write(fake.name() + "\n")

with open('names.txt', 'r') as f:
    all_names = f.read().splitlines()

def get_start_and_end_dates(data):
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')
    # Parse datetime strings with timezones
    start_datetime = parse(start_date_str)
    end_datetime = parse(end_date_str)
    # Extract date components, handling timezones
    start_date = start_datetime.date()
    end_date = end_datetime.date()
    assert start_date < end_date
    return start_date, end_date

def get_preferences(preferences_raw):
    if preferences_raw is None:
        return {}
    
    preferences = []
    for pref in preferences_raw:
        start_datetime = parse(pref["date_start"])
        end_datetime = parse(pref["date_end"])
        start_date = start_datetime.date()
        end_date = end_datetime.date()
        preferences.append(Preference(pref["employeeId"], start_date, end_date, PreferenceType(pref["preference"])))
    return preferences


app = Flask(__name__)
CORS(app)

@app.route('/api/employee/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = {
        "id": employee_id,
        "name": all_names[employee_id-1],
        "working_hours_per_day": 5
    }
    return jsonify(employee)

@app.route('/api/employees', methods=['GET'])
def get_employees():
    limit = request.args.get('limit', default=None, type=int)  # Get the limit parameter from the query string
    if limit:
        employees = [{
            "id": employee_id,
            "name": all_names[employee_id-1],
            "working_hours_per_day": 5
        } for employee_id in range(1, min(limit+1, len(all_names)+1))]
    else:
        employees = [{
            "id": employee_id,
            "name": all_names[employee_id-1],
            "working_hours_per_day": 5
        } for employee_id in range(1, len(all_names)+1)]

    return jsonify(employees)


@app.route('/api/generate-preferences', methods=['POST'])
def generate_preferences():
    data = request.get_json()
    start_date, end_date = get_start_and_end_dates(data)
    employee_count = int(data.get('employees'))


    preferences = generate_employee_preferences(employee_count, start_date, end_date)
    json_data = [
        {
            "employeeId": entry.employee_id,
            "date_start": entry.date_start.isoformat(), 
            "date_end": entry.date_end.isoformat(),
            "preference": entry.preference.value, 
        } for entry in preferences
    ]
    return jsonify(json_data)

@app.route('/api/get-schedule', methods=['POST'])
def get_schedule():
    data = request.get_json()

    employee_count = int(data.get('employees'))
    generations = int(data.get('generations', 100))
    cars_ktw = int(data.get("ktw_cars", 0))
    cars_rtw = int(data.get("rtw_cars", 0))
    cars_nef = int(data.get("nef_cars", 0))
    preferences = get_preferences(data.get("preferences", None))    
    
    start_date, end_date = get_start_and_end_dates(data)
    shifts = create_shifts_for_dates(start_date, end_date, ktw_cars=cars_ktw, rtw_cars=cars_rtw, nef_cars=cars_nef)

    ga = GeneticAlgorithmTabu(
        population_size=100,
        mutation_rate=0.01,
        crossover_rate=0.8,
        elitism=True,
        employees=employee_count,
        shifts=shifts,
        preferences=preferences,
    )

    best_chromosome, best_fitness, best_fitness_history = ga.evolve(
        generations=generations,
        target_fitness=0
    )
    schedule_by_employee = get_shifts_per_employee(ga.shifts, best_chromosome)
    result = []
    for employee, schedule in schedule_by_employee.items():
        sched = [
            {
                "employeeId": employee,
                "date_start": d[0].isoformat(), 
                "date_end": d[1].isoformat(), 
                "car_type": d.car_type.value,
                "hours": (d[1]-d[0]).total_seconds() / 3600,
            }
            for d in schedule
        ]
        result.extend(sched)
    print("Best fitness", best_fitness)
    print("Result", result)
    data = {'data': result, "fitness": best_fitness}
    return jsonify(data)


@app.route('/api/create-schedule', methods=['POST'])
def run_optimization():
    data = request.json
    df = pd.DataFrame.from_dict(data["shifts"])
    df['date_start'] = pd.to_datetime(df['date_start'])
    df['date_end'] = pd.to_datetime(df['date_end'])

    print(df)
    genetic_algorithm = GeneticAlgorithm()
    data_encoded = genetic_algorithm.evolve(10)
    print(data_encoded)
    return jsonify({"message": "Data received successfully"})
    """Run a job on the hybrid solver when the run button is clicked."""

    shifts = list(sched_df["props"]["data"][0].keys())
    shifts.remove("Employee")

    availability = utils.availability_to_dict(sched_df["props"]["data"])
    employees = list(availability.keys())

    isolated_days_allowed = True if 0 in checklist else False
    manager_required = True if 1 in checklist else False

    cqm = employee_scheduling.build_cqm(
        availability,
        shifts,
        *shifts_per_employee,
        *employees_per_shift,
        manager_required,
        isolated_days_allowed,
        consecutive_shifts + 1,
    )

    feasible_sampleset, errors = employee_scheduling.run_cqm(cqm)
    sample = feasible_sampleset.first.sample

    sched = utils.build_schedule_from_sample(sample, employees)

    return (
        utils.display_schedule(sched, availability),
        False,
        {"display": "flex"} if errors else {"display": "none"},
        errors_list(errors) if errors else no_update,
    )

if __name__ == '__main__':
    app.run(debug=True)