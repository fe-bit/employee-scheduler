from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from optimizations.genetic_algorithm import GeneticAlgorithm
from optimizations.genetic_algorithm.genetic_algorithm_tabu import GeneticAlgorithmTabu
from shifts import get_shifts_per_employee

app = Flask(__name__)
CORS(app)


@app.route('/api/data')
def hello_world():
    data = {'message': 'Hello from Flask!'}
    return jsonify(data)

@app.route('/api/get-schedule')
def get_schedule():
    ga = GeneticAlgorithmTabu(
        population_size=100,
        mutation_rate=0.01,
        crossover_rate=0.8,
        elitism=True,
        employees=22
    )
    best_chromosome, best_fitness, best_fitness_history = ga.evolve(
        generations=100,
        target_fitness=0
    )
    schedule_by_employee = get_shifts_per_employee(ga.shifts, best_chromosome)
    result = {}
    for employee, schedule in schedule_by_employee.items():
        sched = [
            {
                "date_start": d[0].isoformat(), 
                "date_end": d[1].isoformat(), 
                "hours": (d[1]-d[0]).total_seconds() / 3600,
            }
            for d in schedule
        ]
        result[employee] = sched
    data = {'data': result}
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