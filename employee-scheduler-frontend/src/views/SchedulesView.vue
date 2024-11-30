<script>
import { eachDayOfInterval, format } from 'date-fns';
import axios from 'axios';
import moment from 'moment';
import PreferenceTable from "../components/PreferenceTable.vue"


export default{
    data() {
        return {
            employeeCount: 22,
            generations: 100,
            populationSize: 100,
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
            preferences: null,
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
                if (this.preferences){
                    const serializedPrefs = this.preferences.map(item => {
                        return {
                        ...item,
                        date_start: item.date_start.toISOString(),
                        date_end: item.date_end.toISOString(),
                        };
                    });
                } else {
                    const serializedPrefs = null
                }
                

                const data = {
                employees: this.employeeCount,
                generations: this.generations,
                start_date: this.selectedDateStart.toISOString(),
                end_date: this.selectedDateEnd.toISOString(),
                ktw_cars: this.ktwCars,
                rtw_cars: this.rtwCars,
                nef_cars: this.nefCars,
                preferences: serializedPrefs,
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
                const updatedEmployeeSchedule = this.schedule.map(item => {
                    return {
                    ...item,
                    date_start: new Date(item.date_start),
                    date_end: new Date(item.date_end),
                    };
                });
                this.schedule = updatedEmployeeSchedule;
                
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
                this.preferences = responseData;
                const updatedPreferences = this.preferences.map(item => {
                    return {
                    ...item,
                    date_start: new Date(item.date_start),
                    date_end: new Date(item.date_end),
                    };
                });
                this.preferences = updatedPreferences;
                console.log(this.preferences[0])
                this.schedule = null;
                 
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
        filteredByDateAndEmployee(myList, day, employeeId) {
            let scheduleOfEmployee = this.filterByEmployeeId(myList, employeeId);
            if (scheduleOfEmployee === null){
                return null;
            }
            let x = scheduleOfEmployee.filter((scheduleItem) => this.isSameDay(scheduleItem.date_start, day));
            x.sort((a, b) => a.date_start - b.date_start);
            return x;
        },
        filterByEmployeeId(myList, employeeId){
            if(myList === null){ 
                return null
            }
            return myList.filter((scheduleItem) => scheduleItem.employeeId == employeeId)
        },
        totalWorkingHours(myList, employeeId){
            let scheduleOfEmployee = this.filterByEmployeeId(myList, employeeId);
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
            let deviation = 0.2;
            let total = this.totalWorkingHours(this.schedule, employeeId)
            let target = this.targetWorkingHours(employeeId)
            let targetLowerBound = target * (1-deviation);
            let targetUpperBound = target * (1+deviation);
            return (total >= targetLowerBound) && (total <= targetUpperBound)
        },
        accountForPreferences(shifts, preferences){
            if (shifts.length == 0){
                // Check if there was a wish for unavailable for that day
                for (let pref of preferences){
                    if (pref.preference == "unavailable"){
                        return true;
                    } else if (pref.preference == "preferred"){
                        return false;
                    }
                }
            } else if( shifts.length == 1){
                // Check if shift was preferred or not
                let shift = shifts[0];
                for (let pref of preferences){
                    if (shift.date_start.getTime() === pref.date_start.getTime() &&
                            pref.preference === "preferred"
                    ){
                        return true;
                    } else if (shift.date_start.getTime() !== pref.date_start.getTime()
                    )
                    {
                        if (pref.preference == "unavailable"){
                            return true;
                        } else if (pref.preference == "preferred"){
                            return false;
                        }
                    }
                }
                
            }
            
        },
        disregardPreferences(shifts, preferences){
            
            if (shifts.length == 0){
                // Check if there was a wish for unavailable for that day
                for (let pref of preferences){
                    if (pref.preference == "unavailable"){
                        return false;
                    } else if (pref.preference == "preferred"){
                        return true;
                    }
                }
            } else if( shifts.length == 1){
                // Check if shift was preferred or not
                let shift = shifts[0];
                for (let pref of preferences){
                    if (shift.date_start.getTime() === pref.date_start.getTime() &&
                            pref.preference === "unavailable"
                    ){
                        return true;
                    } else if (shift.date_start.getTime() !== pref.date_start.getTime()
                    )
                    {
                        if (pref.preference == "preferred"){
                            return true;
                        } else if (pref.preference == "unavailable"){
                            return false;
                        }
                    }
                }
                
            }
        }
    },
    watch: {
        employeeCount(newValue) {
            this.employeeCount = Math.max(1, newValue);
            this.employeeCount = Math.min(this.employeeCount, 100)
            this.getEmployeeData()
        }
    },
    mounted() {
        this.getEmployeeData();
    },

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
            <div class="col">
                <label for="popolation-size" class="form-label">Population Size</label>
                <input type="number" v-model="populationSize" class="form-control" id="popolation-size" placeholder="Population Size">
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
            <!-- <PreferenceTable v-if="!schedule" :employees="employees" />
            <ScheduleTable v-else /> -->
            <tr v-for="employee in this.employees" >
                <td class="text-center">{{ employee.id }} <br>
                    {{ employee.name }} <br>
                    (<span :class="{ 'text-success': isWithinTargetRange(employee.id), 'text-danger': !isWithinTargetRange(employee.id) }">
                    {{ totalWorkingHours(schedule, employee.id) }} / {{  targetWorkingHours(employee.id) }}
                </span>)</td>

                <td class="text-center" v-if="schedule" v-for="day in daysInSelectedRange" :key="day" :set="shifts=filteredByDateAndEmployee(schedule, day, employee.id)" 
                    :class="{ 'bg-danger': filteredByDateAndEmployee(schedule, day, employee.id) && filteredByDateAndEmployee(schedule, day, employee.id).length > 1,
                            'bg-success-subtle': accountForPreferences(filteredByDateAndEmployee(schedule, day, employee.id), filteredByDateAndEmployee(preferences, day, employee.id)),
                            'bg-danger-subtle': disregardPreferences(filteredByDateAndEmployee(schedule, day, employee.id), filteredByDateAndEmployee(preferences, day, employee.id)),
                    }"

                >
                    <p v-if="shifts" v-for="shift in shifts">
                        <span>
                            {{ shift.date_start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }} - {{ shift.date_end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }} <span v-if="!isSameDay(shift.date_start, shift.date_end)"><sup class="">+1</sup></span> ({{ shift.car_type }})
                        </span>
                        <hr>
                    </p>
                    <hr>
                    <p v-if="preferences" v-for="pref in filteredByDateAndEmployee(preferences, day, employee.id)">
                        <span :class="{'text-danger': pref.preference === 'unavailable', 'text-success': pref.preference === 'preferred'}">
                            {{ pref.date_start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }} - {{ pref.date_end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }} <span v-if="!isSameDay(pref.date_start, pref.date_end)"><sup class="">+1</sup></span>
                        </span>
                        <hr>
                    </p>
                </td>

                <td class="text-center" v-else-if="preferences" v-for="day in daysInSelectedRange" :set="empPreferences=filteredByDateAndEmployee(preferences, day, employee.id)">
                    <p v-if="empPreferences" v-for="pref in empPreferences">
                        <span :class="{'text-danger': pref.preference === 'unavailable', 'text-success': pref.preference === 'preferred'}">
                            {{ pref.date_start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }} - {{ pref.date_end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }} <span v-if="!isSameDay(pref.date_start, pref.date_end)"><sup class="">+1</sup></span>
                        </span>
                        <hr>
                    </p>
                </td>
                
                <td class="text-center" v-else v-for="day in daysInSelectedRange">
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
