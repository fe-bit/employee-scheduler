# Employee Scheduler

This project uses a genetic algorithm to solve the employee scheduling problem that is inspired by my regional paramedic organization as it struggles with creating a proper schedule. The project has a frontend in vue.js that offers the scheduling page where one can experiment and simulate this process by adjusting parameters. One can also generate a random preference list that contains the preferences of each employee as they can unavailable or prefer the shift explicitly. The Schedule will be generated on the backend side where also constraints will be considered as part of the fitness function. It considers total working hours in the given time range (deviation from expected value should not be too high), break between shifts and also the preferences.

## Installation

**How to install your project:**

```bash
cd employee-scheduler-backend
pip install -r requirements.txt
```

Also install 

```bash
cd employee-scheduler-frontend
npm install
```

## Running the services
For the backend run the following:
```bash
python app.py
```

For the frontend run:
```bash
npm run dev
```

## Future Work
Adding other optimization algorithms such as a Quantum Annealer or adding a simple MILP-Solver. The project is currently only for experimentation. Making it more capable with a real database or entering real values can be added in the near future.

