from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
from datetime import datetime


app = Flask(__name__)
CORS(app)


@app.route('/api/data')
def hello_world():
    data = {'message': 'Hello from Flask!'}
    return jsonify(data)


@app.route('/api/create-schedule', methods=['POST'])
def run_optimization():
    data = request.json
    df = pd.DataFrame.from_dict(data["shifts"])
    df['date_start'] = pd.to_datetime(df['date_start'])
    df['date_end'] = pd.to_datetime(df['date_end'])

    print(df)
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