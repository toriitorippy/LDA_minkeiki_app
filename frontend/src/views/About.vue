<template>
  <div class="about">
    <h1>This is an about page</h1>
    <Table/>
  </div>
</template>

<script>
import Table from '../components/LDA_Table.vue';

export default {
  name: 'about',
  components: {
    Table,
  },
}

</script>