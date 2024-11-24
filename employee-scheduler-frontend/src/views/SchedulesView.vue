<script>
import { eachDayOfInterval, format } from 'date-fns';
import axios from 'axios';
import moment from 'moment';


export default{
    data() {
        return {
            employeeCount: 22,
            generations: 100,
            items: [
                { id: 1, name: 'Alice', shifts: [
                        {id: 1, time_start: "14:00", time_end: "22:00", type: "RS"},
                        {id: 2, time_start: null, time_end: null},
                        {id: 3, time_start: null, time_end: null},
                        {id: 4, time_start: null, time_end: null},
                        {id: 5, time_start: null, time_end: null},
                        {id: 6, time_start: null, time_end: null},
                        {id: 7, time_start: null, time_end: null},
                    ]
                },
                { id: 2, name: 'Bob' , shifts: [
                        {id: 1, time_start: "14:00", time_end: "22:00", type: "RS"},
                        {id: 2, time_start: null, time_end: null},
                        {id: 3, time_start: null, time_end: null},
                        {id: 4, time_start: null, time_end: null},
                        {id: 5, time_start: null, time_end: null},
                        {id: 6, time_start: null, time_end: null},
                        {id: 7, time_start: null, time_end: null},
                    ]
                },
                { id: 3, name: 'Charlie', shifts: [
                        {id: 1, time_start: null, time_end: null},
                        {id: 2, time_start: null, time_end: null},
                        {id: 3, time_start: null, time_end: null},
                        {id: 4, time_start: null, time_end: null},
                        {id: 5, time_start: null, time_end: null},
                        {id: 6, time_start: null, time_end: null},
                        {id: 7, time_start: null, time_end: null},
                    ]
                }
            ],
            data: null,
            schedule: null,
            fitness: null,

            employees: this.getEmployeeData(),
            
            selectedDateStart: new Date(new Date().getFullYear(), new Date().getMonth()+1, 1),
            selectedDateEnd: new Date(new Date().getFullYear(), new Date().getMonth()+1, 7),
            validationError: null,

            ktwCars: 1,
            rtwCars: 1,
            nefCars: 1,
        };
    },
    computed:{
        daysInSelectedRange(){
            return eachDayOfInterval({ start: this.selectedDateStart, end: this.selectedDateEnd });
        },
    },
    methods: {
        async postData() {
            try {
                const data = {
                employees: this.employeeCount,
                generations: this.generations,
                start_date: this.selectedDateStart.toISOString(),
                end_date: this.selectedDateEnd.toISOString(),
                ktw_cars: this.ktwCars,
                rtw_cars: this.rtwCars,
                nef_cars: this.nefCars,
                };

                const response = await fetch('http://127.0.0.1:5000/api/get-schedule', {
                method: 'POST', // Set method to POST
                headers: { 'Content-Type': 'application/json' }, // Set content type
                body: JSON.stringify(data), // Send data as JSON in the body
                });

                const responseData = await response.json();

                if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
                }

                this.fitness = responseData.fitness;
                this.schedule = responseData.data;

                // Update schedule dates as before
                for (let employee in this.schedule) {
                const updatedEmployeeSchedule = this.schedule.map(item => {
                    return {
                    ...item,
                    date_start: new Date(item.date_start),
                    date_end: new Date(item.date_end),
                    };
                });
                this.schedule = updatedEmployeeSchedule;
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async getEmployeePreferences() {
            try {
                const data = {
                    employees: this.employeeCount,
                    start_date: this.selectedDateStart.toISOString(),
                    end_date: this.selectedDateEnd.toISOString(),
                };

                const response = await fetch('http://127.0.0.1:5000/api/generate-preferences', {
                method: 'POST', // Set method to POST
                headers: { 'Content-Type': 'application/json' }, // Set content type
                body: JSON.stringify(data), // Send data as JSON in the body
                });

                const responseData = await response.json();

                if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
                }
                console.log(responseData)
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        async getEmployeeData() {
            try {
                const response = await axios.get('http://127.0.0.1:5000/api/employees', {
                    params: {
                        limit: this.employeeCount
                    }
                });
                this.employees = response.data
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        },
        getDaysInMonth(year, month, first_n_days) {
            const startDate = new Date(year, month, 1);
            const endDate = first_n_days ? new Date(year, month, first_n_days) : new Date(year, month + 1, 0);
            return eachDayOfInterval({ start: startDate, end: endDate });
        },
        getWeekDay(day){
            const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            return daysOfWeek[day.getDay()]
        },
        isSameDay(date1, date2) {
            return (
                date1.getFullYear() === date2.getFullYear() &&
                date1.getMonth() === date2.getMonth() &&
                date1.getDate() === date2.getDate()
            )
        },
        filteredSchedule(day, employeeId) {
            let scheduleOfEmployee = this.filterScheduleByEmployeeId(employeeId);
            if (scheduleOfEmployee === null){
                return null;
            }
            let x = scheduleOfEmployee.filter((scheduleItem) => this.isSameDay(scheduleItem.date_start, day));
            x.sort((a, b) => a.date_start - b.date_start);
            return x;
        },
        filterScheduleByEmployeeId(employeeId){
            if(this.schedule === null){ 
                return null
            }
            return this.schedule.filter((scheduleItem) => scheduleItem.employeeId == employeeId)
        },
        totalWorkingHours(employeeId){
            let scheduleOfEmployee = this.filterScheduleByEmployeeId(employeeId);
            if (scheduleOfEmployee === null){
                return 0;
            }
            if (scheduleOfEmployee.length > 0){
                return scheduleOfEmployee.map(item => item.hours).reduce((acc, val) => acc + val, 0)
            } else {
                return 0;
            }
        },
        targetWorkingHours(employeeId){
            const start = moment(this.selectedDateStart);
            const end = moment(this.selectedDateEnd);
            const days_between = end.diff(start, 'days') + 1;
            return days_between * this.employees.find(e => e.id == employeeId).working_hours_per_day
        },
        isWithinTargetRange(employeeId){
            let deviation = 0.1;
            let total = this.totalWorkingHours(employeeId)
            let target = this.targetWorkingHours(employeeId)
            let targetLowerBound = target * (1-deviation);
            let targetUpperBound = target * (1+deviation);
            return (total >= targetLowerBound) && (total <= targetUpperBound)
        },
    },
    watch: {
        employeeCount(newValue) {
            this.employeeCount = Math.max(1, newValue);
            this.getEmployeeData()
        }
    },
    mounted() {
        this.getEmployeeData();
    }

}

</script>

<template>
    <div class="container py-3">
        <div class="row g-2">
            <div class="col">
                <label for="start-date" class="form-label">Start Date</label>
                <VueDatePicker id="start-date" v-model="selectedDateStart" :enable-time-picker="false" :min-date="new Date()"></VueDatePicker>
            </div>
            <div class="col">
                <label for="start-date" class="form-label">End Date</label>
                <VueDatePicker id="start-date" v-model="selectedDateEnd" :enable-time-picker="false" :min-date="this.selectedDateStart"></VueDatePicker>
            </div>
            <div class="col">
                <label for="employee-count" class="form-label">Employee Count</label>
                <input type="number" v-model="employeeCount" class="form-control" id="employee-count" placeholder="Employees available">
            </div>
            <div class="col">
                <label for="generations" class="form-label">Generations</label>
                <input type="number" v-model="generations" class="form-control" id="generations" placeholder="Generations">
            </div>
        </div>
        <div class="row g-2">
            <h5>Shifts</h5>
            <div class="col">
                <label for="ktw-count" class="form-label">KTW Cars</label>
                <input type="number" v-model="ktwCars" class="form-control" id="ktw-count" placeholder="KTW Cars">
            </div>
            <div class="col">
                <label for="rtw-count" class="form-label">RTW Cars</label>
                <input type="number" v-model="rtwCars" class="form-control" id="rtw-count" placeholder="RTW Cars">
            </div>
            <div class="col">
                <label for="nef-count" class="form-label">KTW Cars</label>
                <input type="number" v-model="nefCars" class="form-control" id="nef-count" placeholder="NEF Cars">
            </div>
        </div>
        <div class="row g-2">
            <h5>Fitness Function</h5>
        </div>
        

        <button class="btn btn-primary" @click="postData">Get Data</button> <button class="btn btn-primary" @click="getEmployeePreferences">Get Employee preferences</button>
        <p>Fitness: {{ fitness }}</p>
        <div class="container">
        <table class="table table-hover table-striped table-bordered px-2">
        <thead>
            <tr>
                <td class="text-center">Name</td>
                <td style="width: 14%" v-for="day in daysInSelectedRange" :key="day" class="text-center">
                    {{ this.getWeekDay(day) }}<br>{{ day.toLocaleDateString() }}
                </td>
            </tr>
        </thead>
        <tbody>
            <tr v-for="employee in this.employees" >
                <td class="text-center">{{ employee.id }} <br>
                    {{ employee.name }} <br>
                    (<span :class="{ 'text-success': isWithinTargetRange(employee.id), 'text-danger': !isWithinTargetRange(employee.id) }">
                    {{ totalWorkingHours(employee.id) }} / {{  targetWorkingHours(employee.id) }}
                </span>)</td>
                <td class="text-center" v-for="day in daysInSelectedRange" :key="day" :set="shifts=filteredSchedule(day, employee.id)" :class="{ 'bg-danger': filteredSchedule(day, employee.id) && filteredSchedule(day, employee.id).length > 1 }">
                    <p v-if="shifts" v-for="shift in shifts">
                        <span>
                            {{ shift.date_start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }} - {{ shift.date_end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }} <span v-if="!isSameDay(shift.date_start, shift.date_end)"><sup class="">+1</sup></span> ({{ shift.car_type }})
                        </span>
                        <hr>
                    </p>
                </td>
            </tr>
        </tbody>
    </table>
</div>
</div>
  
</template>

<style scoped>
table {
  width: 90%;
  overflow-x: auto;
}
</style>
