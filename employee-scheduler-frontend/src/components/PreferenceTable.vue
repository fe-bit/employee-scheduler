<script>

export default{
    data() {
        return {
            schedule: null,
            preferences: null,
            employees: null,
        };
    },
}
</script>

<template>
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
</template>
