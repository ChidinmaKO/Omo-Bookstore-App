<template>
  <div>
    <p>{{ msg }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'Ping',
  data() {
    return {
      msg: 'Hello World Class Engineer!',
    };
  },
  methods: {
    getMessage() {
      const path = 'http://127.0.0.1:4000/ping';
      axios.get(path).then((response) => {
        this.msg = response.data;
      }).catch((error) => {
        // eslint-disable-next-line
        console.error(error);
      });
    },
  },
  created() {
    this.getMessage();
  },
};
</script>

<style scoped>

</style>
