<script>
import axios from 'axios';


export default{
    data() {
        return {
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
    }
  },
}

</script>

<template>
    <div class="container py-3">
        <button @click="submitData">Sende Daten</button>
        
        <table class="table table-hover table-striped table-bordered">
        <thead>
            <tr>
                <td >Name</td>
                <td style="width: 14%">Monday</td>
                <td style="width: 14%">Tuesday</td>
                <td style="width: 14%">Wednesday</td>
                <td style="width: 14%">Thursday</td>
                <td style="width: 14%">Friday</td>
                <td style="width: 14%">Saturday</td>
                <td style="width: 14%">Sunday</td>
            </tr>
        </thead>
        <tbody>
            <tr v-for="item in items" :key="item.id">
                <td>{{ item.name }}</td>
                <td v-for="shift in item.shifts" :key="shift.id">
                    <span v-if="shift.time_start !== null">{{shift.time_start}} - {{shift.time_end}} ({{ shift.type }})</span>
                </td>
            </tr>
        </tbody>
    </table>
</div>
  
</template>

<style scoped>
</style>
