<script>
export default{
    data() {
        return {
            items: [
                { id: 1, name: 'Alice', qualification: "RS" , hours_scheduled_this_month: 200},
                { id: 2, name: 'Bob' , qualification: "NEF", hours_scheduled_this_month: 160 },
                { id: 3, name: 'Charlie', qualification: "DR" , hours_scheduled_this_month: 80}
            ],
            data: null,
        };
    },
    methods: {
    async fetchData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/data');
        const data = await response.json();
        this.data = data;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    }
  },
}

</script>

<template>
    <div class="container py-3">
        <button @click="fetchData">Fetch Data</button>
        <p v-if="data">{{ data }}</p>
        
        <table class="table table-hover">
        <thead>
            <tr>
                <td>Name</td>
                <td>Qualification</td>
                <td>Hours scheduled this month</td>
            </tr>
        </thead>
        <tbody>
            <tr v-for="item in items" :key="item.id">
                <td>{{ item.name }}</td>
                <td>{{ item.qualification }}</td>
                <td>{{ item.hours_scheduled_this_month }}</td>
            </tr>
        </tbody>
    </table>
</div>
  
</template>

<style scoped>
</style>
