<script>
import axios from 'axios';
import { eachDayOfInterval, format } from 'date-fns';


export default{
    data() {
        return {
            employeeCount: 22,

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
            days: this.getDaysInMonth(2024, 11, 7),
        };
    },
    methods: {
        async submitData() {
      const data = {
        shifts: [
            {employee_id: 1, date_start: "2024-12-20 06:00:00", date_end: "2024-12-20 14:00:00", preference: "preferred"},
            {employee_id: 2, date_start: "2024-12-01 06:00:00", date_end: "2024-12-01 14:00:00", preference: "preferred"},
        ],
      };

      try {
        const response = await axios.post('http://127.0.0.1:5000/api/create-schedule', data);
        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    },

    async getData(){
        try {
            const params = new URLSearchParams({
                employees: this.employeeCount
            });
            const response = await fetch(`http://127.0.0.1:5000/api/get-schedule?${params.toString()}`);
            const data = await response.json();
            this.schedule = data.data;
            for (let employee in this.schedule) {
                const updatedEmployeeSchedule = this.schedule[employee].map(item => {
                    return {
                    ...item,
                    date_start: new Date(item.date_start),
                    date_end: new Date(item.date_end),
                    };
                });
                this.schedule[employee] = updatedEmployeeSchedule;
            }
            // for (let employee in this.schedule){
            //     for (let i = 0; i < this.schedule[employee].length; i++) {
            //         this.schedule[employee][i]["date_start"] = new Date(this.schedule[employee][i]["date_start"])
            //         this.schedule[employee][i]["date_end"] = new Date(this.schedule[employee][i]["date_end"])
            //     }
            // }
            
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

    filteredSchedule(day, i) {
        if(this.schedule === null){ 
            return null
        }
        if(this.schedule[i] == null){
            return null
        }
        // console.log(this.schedule[i][0].date_start)
      let x = this.schedule[i].filter((scheduleItem) => this.isSameDay(scheduleItem.date_start, day));
      return x;
    },
    
    totalWorkingHours(employee){
        if (this.schedule && this.schedule[employee] && this.schedule[employee].length > 0){
            return this.schedule[employee].map(item => item.hours).reduce((acc, val) => acc + val, 0)
        } else {
            return 0;
        }
    }
  },
}

</script>

<template>
    <div class="container py-3">
        <input type="number" v-model="employeeCount">
        <p>Employee value: {{ employeeCount }}</p>
        <button @click="getData">Get Data</button>
        <table class="table table-hover table-striped table-bordered">
        <thead>
            <tr>
                <td >Name</td>
                <td style="width: 14%" v-for="day in days">
                    {{ this.getWeekDay(day) }}<br>{{ day.toLocaleDateString() }}
                </td>
            </tr>
        </thead>
        <tbody>
            <tr v-if="schedule" v-for="i in Object.keys(schedule)" >
                <td>{{ i }} ({{ totalWorkingHours(i) }})</td>
                <td v-for="day in days" :key="day" :set="shifts=filteredSchedule(day, i)">
                    <p v-for="shift in shifts">
                        <span>
                            {{ shift.date_start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }} - {{ shift.date_end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) }}
                        </span>
                </p>
                </td>
            </tr>
        </tbody>
    </table>
</div>
  
</template>

<style scoped>
</style>
